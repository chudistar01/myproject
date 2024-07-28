/**-- Airlines Table
CREATE TABLE Airlines (
	airline_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) NOT NULL,
	code VARCHAR(10) NOT NULL UNIQUE
);

-- Airports Table
CREATE TABLE Airports (
	airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) NOT NULL,
	code VARCHAR(10) NOT NULL UNIQUE,
	city VARCHAR(255) NOT NULL,
	country VARCHAR(255) NOT NULL
);
**/
--Create flight
CREATE TABLE _FLIGHT_CREAT(
	flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
	flight_number VARCHAR(10) NOT NULL,
	departure_airport VARCHAR(20) NOT NULL,
	arrival_airport VARCHAR(20) NOT NULL,
        departure_time DATETIME NOT NULL,
        arrival_time DATETIME NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        available_seats INT NOT NULL
);

-- Flights Table
CREATE TABLE Flights (
	flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(10) NOT NULL,
	airline_id INT,
	flight_number VARCHAR(10) NOT NULL,
	departure_airport_id INT,
	arrival_airport_id INT,
	arrival_airport VARCHAR(20) NOT NULL,
	departure_time DATETIME NOT NULL,
	arrival_time DATETIME NOT NULL,
	price DECIMAL(10, 2) NOT NULL,
	available_seats INT NOT NULL,
	FOREIGN KEY (airline_id) REFERENCES Airlines(airline_id),
	FOREIGN KEY (departure_airport_id) REFERENCES Airports(airport_id),
	FOREIGN KEY (arrival_airport_id) REFERENCES Airports(airport_id)
);

-- Passengers Table
CREATE TABLE Passengers (
	passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	phone_number VARCHAR(20)
);

-- Bookings Table
CREATE TABLE Bookings (
	booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
	flight_id INT,
	passenger_id INT,
	booking_time DATETIME NOT NULL,
	status VARCHAR(50) NOT NULL,
	FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
	FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id)
);

-- Seats Table
CREATE TABLE Seats (
	seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
	flight_id INT,
	seat_number VARCHAR(5) NOT NULL,
	passenger_id INT,
	FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
	FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id)
);

-- Payment Table
CREATE TABLE Payments (
	payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
	booking_id INT,
	amount DECIMAL(10, 2) NOT NULL,
	payment_date DATETIME NOT NULL,
	payment_method VARCHAR(50) NOT NULL,
	status VARCHAR(50) NOT NULL,
	FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

-- Users Table
CREATE TABLE Users (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	role VARCHAR(50) NOT NULL
);

-- Flight_statuses
CREATE TABLE Flight_Statuses (
	status_id INTEGER PRIMARY KEY AUTOINCREMENT,
	status_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Flight_Status_Updates (
	update_id INTEGER PRIMARY KEY AUTOINCREMENT,
	flight_id INT,
	status_id INT,
	update_time DATETIME NOT NULL,
	FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
	FOREIGN KEY (status_id) REFERENCES Flight_Statuses(status_id)
);

