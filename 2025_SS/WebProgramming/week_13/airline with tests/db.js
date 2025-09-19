// db.js
// 모듈 설정
const fs = require('fs');
const sqlite = require('sqlite');
const sqlite3 = require('sqlite3');

//사용할 데이터 베이스 파일 이름 설정
const DB_FILE = 'airline.db';

// 데이터 베이스 연결 함수: SQLite 파일 기반 연결
async function getDBConnection() {
    return sqlite.open({ filename: DB_FILE, driver: sqlite3.Database });
}

// 1) Load schema  SQL 스키마 파일을 읽어 데이터베이스 초기화
async function loadDB(sqlFile) {
    const db = await getDBConnection(); // 데이터베이스 연결
    // SQL 파일을 읽어 문자열로 변환 후 sql 변수에 저장
    const sql = fs.readFileSync(sqlFile, 'utf8'); 
    await db.exec(sql); // 문자열로 된 SQL 명령 실행
    console.log('DB initialized'); // 초기화 완료 메시지 출력
    await db.close(); // 데이터베이스 연결 종료
}

// 2) Get all flights
async function getAllFlights() {
    const db = await getDBConnection();
    const rows = await db.all(`
    SELECT f.id,
           a1.code AS origin,
           a2.code AS destination,
           f.duration
    FROM flight f
    JOIN airport a1 ON f.origin_id = a1.id
    JOIN airport a2 ON f.destination_id = a2.id
  `);
    await db.close();
    return rows;
}


// 3) Get one flight
async function getFlight(flightId) {
    const db = await getDBConnection();
    const flight = await db.get(
        `SELECT f.id, a1.code AS origin, a2.code AS destination, f.duration
         FROM flight f
         JOIN airport a1 ON f.origin_id = a1.id
         JOIN airport a2 ON f.destination_id = a2.id
         WHERE f.id = ?`,[flightId]
    );
    await db.close();
    return flight;
}

// 2) Get all passengers of a flight
async function getPassengers(flightId) {
    const db = await getDBConnection();
    const passengers = await db.all(
        `SELECT p.person_id, pr.first, pr.last
         FROM passenger p
         JOIN person pr ON p.person_id = pr.id
         WHERE p.flight_id = ?`,[flightId]
    );
    await db.close();
    return passengers;
}

// 4) Test / example
async function testQuery() {
    console.log(await getAllFlights());
}

//loadDB('flights_schema.sql');
// testQuery();
module.exports = { loadDB, getAllFlights, getFlight, getPassengers, testQuery };
