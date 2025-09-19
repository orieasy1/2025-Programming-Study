const test = require('node:test');
const assert = require('node:assert');
const { sum, multiply, divide } = require('../utils');

test.describe("Utils Test Suite: sum", () => {
  test.it("Should sum two numbers", () => {
    assert.strictEqual(sum(1, 2), 3);
  });
});

test.describe("Utils Test Suite: multiply", () => {
  test.it("Should multiply two numbers", () => {
    assert.strictEqual(multiply(5, 3), 15);    
  });
});

test.describe("Utils Test Suite: divide", () => {
  test.it("Should divide two positive numbers", () => {
    assert.strictEqual(divide(10, 2), 5);
  });
  test.it("Should divide a positive and a negative number", () => {
    assert.strictEqual(divide(-10, 2), -5);
  });

  test.it("Should return Infinity when dividing by 0", () => {
    assert.strictEqual(divide(10, 0), Infinity);
  });
  test.it("Should return NaN when dividing 0 by 0", () => {
    assert.ok(Number.isNaN(divide(0, 0)));
  });
});