const request = require('supertest');
const app = require('../app'); 

// Mock your database functions
jest.mock('../db'); 

const { getFlight, getPassengers } = require('../db');

describe('GET /api/flights/:id', () => {
  it('should return 404 if flight not found', async () => {
    getFlight.mockResolvedValue(null); // simulate no flight found

    const res = await request(app).get('/api/flights/999');
    expect(res.statusCode).toBe(404);
  });

  it('should return flight with passengers', async () => {
    getFlight.mockResolvedValue({
      id: 1,
      origin: 'Seoul',
      destination: 'Tokyo',
      duration: 120
    });

    getPassengers.mockResolvedValue([
      { id: 1, first: 'Alice', last: 'Kim' },
      { id: 2, first: 'Bob', last: 'Lee' }
    ]);

    const res = await request(app).get('/api/flights/1');

    expect(res.statusCode).toBe(200);
    expect(res.body).toEqual({
      id: 1,
      origin: 'Seoul',
      destination: 'Tokyo',
      duration: 120,
      passengers: [
        { id: 1, first: 'Alice', last: 'Kim' },
        { id: 2, first: 'Bob', last: 'Lee' }
      ]
    });
  });

  it('should return 500 on error', async () => {
    getFlight.mockImplementation(() => {
      throw new Error('DB failed');
    });

    const res = await request(app).get('/api/flights/1');
    expect(res.statusCode).toBe(500);
    expect(res.body).toHaveProperty('message', 'DB failed');
  });
});

describe("GET /api/flights", () => {
        it.todo("Should return an empty array when there's no flights data")
        it.todo("Should return all the flights")
    })