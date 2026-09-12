#!/usr/bin/env node
/**
 * Railway start: serve dist on 0.0.0.0:PORT so the proxy can reach the app.
 * PORT is set by Railway; target port in Networking must match this value.
 */
const { spawn } = require('child_process');
const path = require('path');

const port = process.env.PORT || '3000';
const dist = path.join(__dirname, 'dist');

const child = spawn(
  'npx',
  ['serve', '-s', dist, '-l', `tcp://0.0.0.0:${port}`],
  { stdio: 'inherit', env: process.env, cwd: __dirname }
);

child.on('exit', (code) => process.exit(code != null ? code : 0));
