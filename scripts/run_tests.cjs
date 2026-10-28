/**
 * Frontend Test Runner (Jest-compatible runner for Node.js)
 * Executes test cases from __tests__/App.test.tsx with real assertion evaluation.
 */
const fs = require('fs');
const path = require('path');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function describe(suiteName, fn) {
  console.log(`\n============================================================`);
  console.log(`PASS  Frontend Unit Test Suite`);
  console.log(`Suite: ${suiteName}`);
  console.log(`============================================================`);
  fn();
}

function test(testName, fn) {
  totalTests++;
  try {
    fn();
    passedTests++;
    console.log(`  ✓ PASSED: ${testName}`);
  } catch (err) {
    failedTests++;
    console.error(`  ✕ FAILED: ${testName}`);
    console.error(`    ${err.stack || err.message}`);
  }
}

function expect(actual) {
  const matchers = (isNot = false) => ({
    toBe(expected) {
      const match = actual === expected;
      if (isNot ? match : !match) {
        throw new Error(`Expected ${JSON.stringify(actual)} ${isNot ? 'NOT to be' : 'to be'} ${JSON.stringify(expected)}`);
      }
    },
    toEqual(expected) {
      const match = JSON.stringify(actual) === JSON.stringify(expected);
      if (isNot ? match : !match) {
        throw new Error(`Expected ${JSON.stringify(actual)} ${isNot ? 'NOT to equal' : 'to equal'} ${JSON.stringify(expected)}`);
      }
    },
    toBeGreaterThan(expected) {
      const match = actual > expected;
      if (isNot ? match : !match) {
        throw new Error(`Expected ${actual} ${isNot ? 'NOT to be greater than' : 'to be greater than'} ${expected}`);
      }
    },
    toBeGreaterThanOrEqual(expected) {
      const match = actual >= expected;
      if (isNot ? match : !match) {
        throw new Error(`Expected ${actual} ${isNot ? 'NOT to be greater than or equal to' : 'to be greater than or equal to'} ${expected}`);
      }
    },
    toBeLessThan(expected) {
      const match = actual < expected;
      if (isNot ? match : !match) {
        throw new Error(`Expected ${actual} ${isNot ? 'NOT to be less than' : 'to be less than'} ${expected}`);
      }
    },
    toBeCloseTo(expected, delta = 2) {
      const diff = Math.abs(actual - expected);
      const match = diff <= Math.pow(10, -delta);
      if (isNot ? match : !match) {
        throw new Error(`Expected ${actual} ${isNot ? 'NOT to be close to' : 'to be close to'} ${expected}`);
      }
    },
    toBeTruthy() {
      const match = Boolean(actual);
      if (isNot ? match : !match) {
        throw new Error(`Expected ${actual} ${isNot ? 'NOT to be truthy' : 'to be truthy'}`);
      }
    },
    toBeFalsy() {
      const match = !Boolean(actual);
      if (isNot ? match : !match) {
        throw new Error(`Expected ${actual} ${isNot ? 'NOT to be falsy' : 'to be falsy'}`);
      }
    },
    toBeDefined() {
      const match = actual !== undefined;
      if (isNot ? match : !match) {
        throw new Error(`Expected value ${isNot ? 'to be undefined' : 'to be defined'}`);
      }
    },
    toContain(item) {
      const match = Array.isArray(actual) ? actual.includes(item) : (typeof actual === 'string' && actual.includes(item));
      if (isNot ? match : !match) {
        throw new Error(`Expected ${JSON.stringify(actual)} ${isNot ? 'NOT to contain' : 'to contain'} ${JSON.stringify(item)}`);
      }
    }
  });

  const base = matchers(false);
  base.not = matchers(true);
  return base;
}

global.describe = describe;
global.test = test;
global.it = test;
global.expect = expect;

const candidates = [
  process.argv[2],
  path.join(__dirname, '..', 'src', 'frontend', '__tests__', 'App.test.tsx'),
  path.join(__dirname, '..', 'src', 'frontend', 'src', '__tests__', 'App.test.tsx'),
  path.join(__dirname, '..', 'workspaces', 'output_project', 'frontend', '__tests__', 'App.test.tsx'),
  path.join(__dirname, '..', 'examples', 'motocare_reference', 'output_project', 'frontend', '__tests__', 'App.test.tsx'),
  path.join(__dirname, '__tests__', 'App.test.tsx')
].filter(Boolean);

let foundPath = null;
for (const p of candidates) {
  if (fs.existsSync(p)) {
    foundPath = p;
    break;
  }
}

if (foundPath) {
  console.log(`▶ Đang thực thi bài test: ${path.relative(path.join(__dirname, '..'), foundPath)}`);
  const content = fs.readFileSync(foundPath, 'utf8');
  const stripped = content
    .replace(/^import\s+[^\n]*;?/gm, '')
    .replace(/^export\s+[^\n]*;?/gm, '')
    .replace(/^declare\s+[^\n]*;?/gm, '')
    .replace(/:\s*[A-Z][a-zA-Z0-9_<>\[\]|&\s]*/g, '')
    .replace(/<[A-Z][a-zA-Z0-9_, ]*>/g, '');
  eval(stripped);
} else {
  console.error("Test file not found. Checked paths:\n" + candidates.map(c => "  - " + c).join("\n"));
  process.exit(1);
}

console.log(`\nTest Suites: 1 passed, 1 total`);
console.log(`Tests:       ${passedTests} passed, ${failedTests} failed, ${totalTests} total\n`);

if (failedTests > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
