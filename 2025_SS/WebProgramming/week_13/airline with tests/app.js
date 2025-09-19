// app.js
const express = require('express');

// Import your DB helpers
const {
    loadDB,
    getAllFlights,
    getPassengers,
    getFlight
} = require('./db');


const SCHEMA = 'flights_schema.sql';

const app = express();

// JSON + static files
app.use(express.json());
app.use(express.static('public'));



app.get(
    '/api/flights',
    async (req, res) => {
        res.json(await getAllFlights());
    }
);


app.get(
    '/api/flights/:id',
    async (req, res) => {
        try {
            const flightId = parseInt(req.params.id);
            // 1) Flight info
            const flight = await getFlight(flightId);            
            // check if flight exists
            if (!flight) {
                res.sendStatus(404);
            } else {
                // 2) Assigned passengers (persons)
                const passengers = await getPassengers(flightId);
                res.json({
                    id: flight.id,
                    origin: flight.origin,
                    destination: flight.destination,
                    duration: flight.duration,
                    passengers: passengers
                });
            }
        } catch (err) {
            res.status(500).json({ message: err.message });
        }
    }
);


module.exports = app;
