// Reuse the Purust library implementations, adapting the gopurs library ABI.
// These adapters were qualified on the shared gopurs-aff Go/Rust corpus.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { unusedFfi } from './unused.mjs';

const hash = bytes => createHash('sha256').update(bytes).digest('hex');
function walk(directory) {
  if (!existsSync(directory)) return [];
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? walk(path) : entry.isFile() ? [path] : [];
  });
}
const replace = (source, before, after) => {
  assert.equal(source.split(before).length, 2, `Rust ABI adapter no longer matches: ${before}`);
  return source.replace(before, after);
};
export function prepareRustFfi(output, libraries, directory) {
  const ports = new Map();
  for (const name of readdirSync(libraries).filter(name => name.startsWith('purust-')).sort()) {
    const source = join(libraries, name, 'src');
    for (const file of walk(source).filter(file => file.endsWith('.rs'))) {
      const module = relative(source, file).slice(0, -3).split('/').join('.');
      ports.set(module, [...(ports.get(module) ?? []), file]);
    }
  }
  mkdirSync(directory, { recursive: true });
  const records = [];
  for (const name of readdirSync(output).sort()) {
    const path = join(output, name, 'corefn.json');
    if (!existsSync(path)) continue;
    const module = JSON.parse(readFileSync(path, 'utf8'));
    const candidates = ports.get(name) ?? [];
    const packageName = module.modulePath.match(/(?:^|\/)(gopurs-[^/]+)\//)?.[1]?.replace(/^gopurs-/, 'purust-');
    const preferred = candidates.filter(path => packageName && path.includes('/' + packageName + '/'));
    const choices = preferred.length ? preferred : candidates;
    assert(choices.length < 2 || new Set(choices.map(path => hash(readFileSync(path)))).size === 1,
      `Ambiguous Rust FFI for ${name}: ${choices.join(', ')}`);
    const port = choices[0], target = join(directory, name + '.rs');
    if (!port) {
      if (module.foreign.length) {
        const source = unusedFfi[name];
        assert(source, `Missing Rust FFI for ${name}`);
        writeFileSync(target, source);
        records.push({ module: name, path: target, sha256: hash(source), unused_trap: true });
      }
      continue;
    }
    const original = readFileSync(port, 'utf8');
    let source = original;
    switch (name) {
      case 'Effect.Aff':
        source = replace(source, `    fn new(value: AffValue) -> Self {
        Self {
            is_left: value.get_isLeft(),
            from_left: value.get_fromLeft(),
            from_right: value.get_fromRight(),
            left: value.get_left(),
            right: value.get_right(),
        }
    }`, '    fn new(_value: AffValue) -> Self { gopurs_aff_util() }');
        source = source.replaceAll('Effect_Aff__makeSupervisedFiber', 'gopurs_base_makeSupervisedFiber')
          .replaceAll('Effect_Aff_makeAff', 'gopurs_base_makeAff');
        source += '\n' + readFileSync(new URL('./aff-compat.rs', import.meta.url), 'utf8');
        break;
      case 'Effect.AVar':
        for (const name of ['putVar', 'takeVar', 'readVar', 'killVar', 'tryPutVar', 'tryTakeVar', 'tryReadVar', 'status'])
          source = source.replaceAll('Effect_AVar__' + name, 'gopurs_base_AVar__' + name);
        source = source.replace(/util\.get_(\w+)\(\)/g, (_, field) => `gopurs_avar_field(&util, "${field}")`);
        source += '\n' + readFileSync(new URL('./avar-compat.rs', import.meta.url), 'utf8');
        break;
      case 'Data.Array.ST':
        source = source.replaceAll('Data_Array_ST_new()', 'Data_Array_ST_newImpl()'); break;
      case 'Control.Monad.ST.Internal':
        source = source.replaceAll('Control_Monad_ST_Internal_for(', 'Control_Monad_ST_Internal_forImpl(')
          .replaceAll('Control_Monad_ST_Internal_new(', 'Control_Monad_ST_Internal_newImpl('); break;
      case 'Data.Traversable':
        source = replace(source, '    pure: TraversalFunction,\n    function:',
          '    pure: TraversalFunction,\n    _append: TraversalApply,\n    function:'); break;
      case 'Effect.Ref':
        source += `
pub fn Effect_Ref_modify_(update: purust_core::Func1<crate::UnknownType, crate::UnknownType>, reference: crate::UnknownType) -> crate::UnknownType {
    purust_ref_effect(move || {
        let mut guard = reference.unwrap_class::<PurustRef>().lock();
        *guard = update(guard.clone());
        crate::Value::Unit
    })
}
`; break;
    }
    writeFileSync(target, source);
    const record = { module: name, origin: port, original_sha256: hash(original), path: target, sha256: hash(source) };
    if (existsSync(port + '.cargo.json')) {
      copyFileSync(port + '.cargo.json', target + '.cargo.json');
      record.cargo_sha256 = hash(readFileSync(target + '.cargo.json'));
    }
    records.push(record);
  }
  writeFileSync(join(directory, 'manifest.json'), JSON.stringify(records, null, 2) + '\n');
  console.log(`Rust FFI: ${records.length} modules prepared from ${libraries}`);
}
