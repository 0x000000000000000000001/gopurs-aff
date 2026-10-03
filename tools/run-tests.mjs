import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const result = spawnSync('./output/go_test_app', [], {
  encoding: 'utf8', timeout: 120000, maxBuffer: 16 * 1024 * 1024,
});
writeFileSync('output/test.stdout', result.stdout ?? '');
writeFileSync('output/test.stderr', result.stderr ?? '');
process.stdout.write(result.stdout ?? '');
process.stderr.write(result.stderr ?? '');
if (result.error) throw result.error;
assert.equal(result.status, 0, `Go tests failed (${result.signal ?? result.status}); see output/test.stderr`);
assert.equal(result.stderr, '', 'Go tests wrote unexpected stderr');
const lines = text => text.trimEnd().split(/\r?\n/).sort();
assert.deepEqual(lines(result.stdout), lines(readFileSync('test/expected-main.stdout', 'utf8')),
  'Tests did not print every expected check; see output/test.stdout');
