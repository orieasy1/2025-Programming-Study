-- Airports
CREATE TABLE airport (
  id    INTEGER PRIMARY KEY,
  code  TEXT NOT NULL,
  city  TEXT NOT NULL
);

-- Flights
CREATE TABLE flight (
  id             INTEGER PRIMARY KEY,
  origin_id      INTEGER NOT NULL REFERENCES airport(id),
  destination_id INTEGER NOT NULL REFERENCES airport(id),
  duration       INTEGER NOT NULL
);

-- optional, you can use this syntax
-- FOREIGN KEY (origin_id) REFERENCES airports(id),

-- Persons (can be booked as passengers)
CREATE TABLE person (
  id     INTEGER PRIMARY KEY,
  first  TEXT    NOT NULL,
  last   TEXT    NOT NULL
);

-- Passenger bookings: links persons → flights
CREATE TABLE passenger (
  person_id INTEGER NOT NULL REFERENCES person(id),
  flight_id INTEGER NOT NULL REFERENCES flight(id),
  PRIMARY KEY(person_id, flight_id)
);

-- INSERT AIRPORTS
INSERT INTO airport (code, city) VALUES ('JFK', 'New York');
INSERT INTO airport (code, city) VALUES ('PVG', 'Shanghai');
INSERT INTO airport (code, city) VALUES ('IST', 'Istanbul');
INSERT INTO airport (code, city) VALUES ('LHR', 'London');
INSERT INTO airport (code, city) VALUES ('SVO', 'Moscow');
INSERT INTO airport (code, city) VALUES ('LIM', 'Lima');
INSERT INTO airport (code, city) VALUES ('CDG', 'Paris');
INSERT INTO airport (code, city) VALUES ('NRT', 'Tokyo');

-- INSERT FLIGHTS
INSERT INTO flight (origin_id, destination_id, duration) VALUES (1, 4, 415);
INSERT INTO flight (origin_id, destination_id, duration) VALUES (2, 7, 760);
INSERT INTO flight (origin_id, destination_id, duration) VALUES (3, 8, 700);
INSERT INTO flight (origin_id, destination_id, duration) VALUES (1, 7, 435);
INSERT INTO flight (origin_id, destination_id, duration) VALUES (5, 7, 245);
INSERT INTO flight (origin_id, destination_id, duration) VALUES (6, 1, 455);


-- INSERT PERSONS
INSERT INTO person (first, last) VALUES ('Harry', 'Potter');
INSERT INTO person (first, last) VALUES ('Ron', 'Weasley');
INSERT INTO person (first, last) VALUES ('Hermione', 'Granger');
INSERT INTO person (first, last) VALUES ('Draco', 'Malfoy');
INSERT INTO person (first, last) VALUES ('Luna', 'Lovegood');
INSERT INTO person (first, last) VALUES ('Ginny', 'Weasley');

-- INSERT PASSENGERS
INSERT INTO passenger (person_id, flight_id) VALUES (1, 1);
INSERT INTO passenger (person_id, flight_id) VALUES (2, 1);
INSERT INTO passenger (person_id, flight_id) VALUES (2, 4);
INSERT INTO passenger (person_id, flight_id) VALUES (3, 2);
INSERT INTO passenger (person_id, flight_id) VALUES (4, 4);
INSERT INTO passenger (person_id, flight_id) VALUES (5, 6);
INSERT INTO passenger (person_id, flight_id) VALUES (6, 6);