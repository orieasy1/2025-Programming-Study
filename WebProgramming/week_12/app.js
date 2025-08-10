const express = require('express');

const {
    getAllFlights,
    getPassengers,
    getFlight
} = require('./db.js');


const PORT =8080;

const app = express();

app.use(express.json())
app.use(express.static('public'));

//fligths endpoint
app.get(
    '/api/flights',
    async (req, res)=> {
        res.json(await getAllFlights());
    }
);

// flight id endpoint
app.get(
    '/api/flights/:id',
    async (req,res) => {
        const flightId = req.params.id;
        //flight info
        const flight = await getFlight(flightId);
        // passengers info
        const passengers = await getPassengers(flightId);
        res.json({
            id : flight.id,
            origin: flight.origin,
            destination: flight.destination,
            duration: flight.duration,
            passengers: passengers
        });
    }
);

app.listen(PORT, ()=>{
    console.log(`Server running at http://localhost:${PORT}`)
})