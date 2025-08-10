const { sum, multiply, divide } = require('../utils.js');

describe("Utils Test Suite: sum", () => {
  test("Should sum two numbers", () => {
    expect(sum(1, 2)).toBe(3);
  });
});

describe("Utils Test Suite: multiply", () => {
  test("Should multiply two numbers", () => {
      expect(multiply(5, 3)).toBe(15);
  });
});

describe("Utils Test Suite: divide", () => {
  test("Should divide two positive numbers", () => {
    expect(divide(10, 2)).toBe(5);
  });
  test("Should divide a positive and a negative number", () => {
    expect(divide(-10, 2)).toBe(-5);
  });
  test("Should return Infinity when dividing by 0", () => {
    expect(divide(10, 0)).toBe(Infinity);
  });
  test("Should return NaN when dividing 0 by 0", () => {
    expect(Number.isNaN(divide(0, 0))).toBe(true);
  });
});