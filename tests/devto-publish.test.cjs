const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');

const source = fs.readFileSync(path.join(__dirname, '../content/devto/2026-03/devto-publish.js'), 'utf8');
function harness(env = {}, status = 201) {
  const result = { calls: [], reads: [], logs: [], process: { env, argv: [], exitCode: 0 } };
  const response = new EventEmitter();
  response.statusCode = status;
  response.resume = () => { result.discarded = true; };
  const request = new EventEmitter();
  request.setTimeout = (ms, callback) => { result.timeout = ms; result.onTimeout = callback; };
  request.destroy = (error) => request.emit('error', error);
  request.end = (payload) => { result.payload = JSON.parse(payload); response.emit('end'); };
  const modules = {
    fs: { readFileSync: (file) => { result.reads.push(file); return '# synthetic article'; } },
    https: { request: (options, callback) => { result.calls.push(options); callback(response); return request; } }
  };
  const requireStub = (name) => { assert.ok(name in modules); return modules[name]; };
  const module = { exports: {} };
  const context = { require: requireStub, module, process: result.process, Buffer,
    console: { log: (...args) => result.logs.push(args.join(' ')), error: (...args) => result.logs.push(args.join(' ')) } };
  vm.runInNewContext(source, context);
  return Object.assign(result, { run: module.exports.main, modules, request, response });
}

test('import performs no file read or HTTP request', () => {
  const h = harness();
  assert.equal(h.calls.length, 0);
  assert.equal(h.reads.length, 0);
});
test('missing key fails before file read or request', () => {
  const h = harness(); h.run([]);
  assert.equal(h.process.exitCode, 1);
  assert.equal(h.calls.length, 0);
  assert.equal(h.reads.length, 0);
});
test('legacy command-line key is rejected without logging it', () => {
  const h = harness({ DEVTO_API_KEY: 'synthetic-env-only' });
  h.run(['article.md', 'synthetic-argument-key']);
  assert.equal(h.calls.length, 0);
  assert.equal(h.process.exitCode, 1);
  assert.ok(!h.logs.join('\n').includes('synthetic-argument-key'));
});
test('environment key, HTTPS, timeout, response redaction', () => {
  const h = harness({ DEVTO_API_KEY: 'synthetic-env-only' }); h.run(['article.md']);
  assert.equal(h.calls[0].headers['api-key'], 'synthetic-env-only');
  assert.equal(h.calls[0].hostname, 'dev.to');
  assert.equal(h.timeout, 30000);
  assert.equal(h.payload.article.published, true);
  assert.equal(h.discarded, true);
  assert.deepEqual(h.logs, ['Status: 201']);
});
test('HTTP error sets failure exit code without response body', () => {
  const h = harness({ DEVTO_API_KEY: 'synthetic-env-only' }, 401); h.run([]);
  assert.equal(h.process.exitCode, 1);
  assert.deepEqual(h.logs, ['Status: 401']);
});
test('network errors and timeouts never log exception details', () => {
  const h = harness({ DEVTO_API_KEY: 'synthetic-env-only' }); h.run([]);
  h.request.emit('error', new Error('synthetic-env-only'));
  h.onTimeout();
  assert.equal(h.process.exitCode, 1);
  assert.ok(!h.logs.join('\n').includes('synthetic-env-only'));
});
test('file errors prevent HTTP and hide private path', () => {
  const h = harness({ DEVTO_API_KEY: 'synthetic-env-only' });
  h.modules.fs.readFileSync = () => { throw new Error('synthetic-private-path'); };
  h.run(['article.md']);
  assert.equal(h.calls.length, 0);
  assert.equal(h.process.exitCode, 1);
  assert.ok(!h.logs.join('\n').includes('synthetic-private-path'));
});
