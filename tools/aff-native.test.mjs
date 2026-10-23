import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';

test('native Aff catches synchronous exceptions and releases bracket resources', t => {
  const directory = mkdtempSync(join(tmpdir(), 'gopurs-aff-native-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  writeFileSync(join(directory, 'go.mod'), 'module gopurs/output\n\ngo 1.23\n');
  // Compile the actual FFI unchanged apart from its generated package clause.
  writeFileSync(join(directory, 'Aff.go'), 'package affprobe\n\n' +
    readFileSync(new URL('../src/Effect/Aff.go', import.meta.url), 'utf8'));
  copyFileSync(new URL('./aff-native_test.go', import.meta.url), join(directory, 'aff_test.go'));
  mkdirSync(join(directory, 'gopurs_runtime'));
  copyFileSync(new URL('../../gopurs/runtime/runtime.go', import.meta.url),
    join(directory, 'gopurs_runtime/runtime.go'));
  const result = spawnSync('go', ['test', '-race', '-count=1', '-timeout=30s', '-v', '.'], {
    cwd: directory, env: { ...process.env, GOWORK: 'off' }, encoding: 'utf8', timeout: 60000,
  });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stdout + result.stderr);
  t.diagnostic(result.stdout);
});
