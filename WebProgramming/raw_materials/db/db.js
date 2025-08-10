// db.js
const fs = require('fs');
const sqlite = require('sqlite');
const sqlite3 = require('sqlite3');

const DB_FILE = 'airline.db';

async function getDBConnection() {
    return sqlite.open({ filename: DB_FILE, driver: sqlite3.Database });
}

// 1) Load schema 
async function loadDB(sqlFile) {
    const db = await getDBConnection();
    const sql = fs.readFileSync(sqlFile, 'utf8');
    await db.exec(sql);    
    console.log('DB initialized');
    await db.close();
}

// 2) Get all flights
async function getAllFlights() {
    const db = await getDBConnection();
    const rows = await db.all(`

  `);
    await db.close();
    return rows;
}


// 3) Get one flight
async function getFlight(flightId) {
    const db = await getDBConnection();
    const flight = await db.get(

    );
    await db.close();
    return flight;
}

// 2) Get all passengers of a flight
async function getPassengers(flightId) {
    const db = await getDBConnection();
    const passengers = await db.all(

    );
    await db.close();
    return passengers;
}

// 4) Test / example
async function testQuery() {
    console.log(await getAllFlights());
}

//loadDB('flights_schema.sql');
//testQuery();
module.exports = { loadDB, getAllFlights, getFlight,getPassengers, testQuery };
