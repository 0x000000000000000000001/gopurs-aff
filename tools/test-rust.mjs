// Run this checkout's PureScript tests through the sibling Purust backend.
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { accessSync, constants, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { delimiter, dirname, isAbsolute, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { prepareRustFfi } from './rust-ffi/prepare.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
if (args.includes('--help')) {
  console.log('Usage: GOPURS_RUST=1 ./bin/test [-c|--clean]\nRun gopurs-aff with Purust. PURUST_JS=1 selects the JavaScript compiler.\n-c rebuilds the selected Purust compiler. PURUST_DIR selects its checkout; PURS selects the typed frontend.');
  process.exit(0);
}
assert(args.every(arg => ['-c', '--clean'].includes(arg)), 'Usage: GOPURS_RUST=1 ./bin/test [-c|--clean]');
const clean = args.length > 0;
const purust = resolve(process.env.PURUST_DIR ?? join(root, '../../purust/purust'));
const { findTypedCompiler, verifyTypedOutput } = await import(pathToFileURL(join(purust, 'tools/native-workspace.mjs')).href);
const configured = process.env.PURS ?? process.env.PURUST_PURS;
const configuredPath = configured && (isAbsolute(configured) || configured.includes('/') ? resolve(configured)
  : execFileSync('/bin/sh', ['-c', 'command -v "$1"', 'sh', configured], { encoding: 'utf8' }).trim());
const purs = findTypedCompiler(purust, configuredPath);
const spago = join(purust, 'node_modules/.bin/spago');
accessSync(spago, constants.X_OK);
const env = { ...process.env, PURUST_PURS: purs,
  PATH: [dirname(purs), join(purust, 'node_modules/.bin'), process.env.PATH ?? ''].join(delimiter),
  GHCRTS: process.env.GHCRTS ?? '-N2',
  CARGO_BUILD_JOBS: process.env.CARGO_BUILD_JOBS ?? '8',
  CARGO_PROFILE_DEV_DEBUG: process.env.CARGO_PROFILE_DEV_DEBUG ?? '0',
  CARGO_INCREMENTAL: process.env.CARGO_INCREMENTAL ?? '0',
  CARGO_TARGET_DIR: resolve(root, process.env.CARGO_TARGET_DIR ?? '.cache/purust-target'),
};
function run(label, command, args, cwd = root, commandEnv = env) {
  console.log(`=== ${label} ===`);
  const result = spawnSync(command, args, { cwd, env: commandEnv, stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
if (clean) {
  // The compiler bootstrap owns a separate Cargo workspace and expects its
  // executable there; the application's shared target directory is unrelated.
  const compilerEnv = { ...env };
  delete compilerEnv.CARGO_TARGET_DIR;
  run('Recompiling purust', 'npm', ['run', env.PURUST_JS === '1' ? 'build' : 'build:native'], purust, compilerEnv);
  for (const name of ['.spago', '.cache']) rmSync(join(root, name), { recursive: true, force: true });
}
accessSync(join(purust, 'bin', env.PURUST_JS === '1' ? 'purust.js' : 'purust-native'), constants.R_OK);
for (const name of ['output', '.purmeta']) rmSync(join(root, name), { recursive: true, force: true });
rmSync(join(root, 'spago.yaml'), { force: true });
symlinkSync('spago.go.yaml', join(root, 'spago.yaml'));
run('Building gopurs-aff TAST', spago, ['build']);
const output = join(root, 'output');
const tast = verifyTypedOutput(output);
console.log(`Typed input: ${tast.modules} modules / ${tast.types} types`);
prepareRustFfi(output, dirname(purust), join(output, 'rust-ffi'));
run(`Generating Rust code with purust (${env.PURUST_JS === '1' ? 'JavaScript' : 'native Rust'})`,
  join(purust, 'bin/purust'), ['--main', 'Test.Main', '--threaded', '--source', 'output',
    '--out', 'output/purust_output', '--ffi-dir', 'output/rust-ffi']);
run('Compiling Rust test binary', 'cargo', ['build', '--manifest-path', 'output/purust_output/Cargo.toml']);
console.log('=== Running Rust tests ===');
const binary = join(env.CARGO_TARGET_DIR, 'debug', process.platform === 'win32' ? 'purust_output.exe' : 'purust_output');
const result = spawnSync(binary, [], { cwd: root, env, encoding: 'utf8', timeout: 120000, maxBuffer: 16 * 1024 * 1024 });
mkdirSync(output, { recursive: true });
writeFileSync(join(output, 'rust-test.stdout'), result.stdout ?? '');
writeFileSync(join(output, 'rust-test.stderr'), result.stderr ?? '');
process.stdout.write(result.stdout ?? '');
process.stderr.write(result.stderr ?? '');
if (result.error) throw result.error;
assert.equal(result.status, 0, `Rust tests failed (${result.signal ?? result.status}); see output/rust-test.stderr`);
assert.equal(result.stderr, '', 'Rust tests wrote unexpected stderr');
const lines = text => text.trimEnd().split(/\r?\n/).sort();
assert.deepEqual(lines(result.stdout), lines(readFileSync(join(root, 'test/expected-main.stdout'), 'utf8')),
  'Rust tests did not print every expected check; see output/rust-test.stdout');
console.log('\n✅ Tests passed successfully! (Rust, 45 Aff checks and AVar stress)');
