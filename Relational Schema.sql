-- Relational Schema
-- User_types(type [PK])

-- Users(Email [PK, FK -> User_types.type], Name, User_type)

-- Agents(Agent_Email [PK, FK → Users.Email], job_title, Agency, phone)

-- Prospective_Renters(Renter_Email [PK, FK → Users.Email], Budget, preferred_location, move_in_date, reward_points)

-- Addresses(Address_id [PK], street, city, state, zip_code, User_email [FK → Users.Email])

-- Credit_cards(card_number [PK], card_holder_name,expiry_date, cvv, billing_address_id [FK → Addresses.Address_id])

-- prop_type(type [PK])

-- Neighborhood(Neighborhood_id [PK], crime_rate, nearby_schools)

-- Property(Property_id [PK], property_type [FK → prop_type.type], location, description, city, state, price, availability, sqft, no_of_rooms, neighborhood_id [FK → Neighborhood.Neighborhood_id])

-- Houses(House_id [PK, FK → Property.Property_id], building_type)

-- Apartments(Apartment_id [PK, FK → Property.Property_id], building_type)

-- Commercial_Buildings(building_id [PK, FK → Property.Property_id], type_of_business)

-- Booking(Booking_ID [PK], property_id [FK → Property.Property_id], booking_date, card_number [FK → Credit_cards.card_number], agent_id [FK → Agents.Agent_Email], renter_id [FK → Prospective_Renter.Renter_Email])

-- ==========================================================================================================================================
--APP Phase
-- ==========================================================================================================================================
CREATE TABLE User_type (
    type VARCHAR(20) PRIMARY KEY
);

CREATE TABLE Users (
    Email VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50),
    User_type VARCHAR(10),
    FOREIGN KEY (User_type) REFERENCES User_type(type)
);

CREATE TABLE Agents (
    Agent_Email VARCHAR(50) PRIMARY KEY,
    job_title VARCHAR(20),
    Agency VARCHAR(20),
    phone VARCHAR(10),
    FOREIGN KEY (Agent_Email) REFERENCES Users(Email) ON DELETE CASCADE
);

CREATE TABLE Prospective_Renters (
    Renter_Email VARCHAR(50) PRIMARY KEY,
    Budget INT,
    preferred_location VARCHAR(100),
    move_in_date VARCHAR(20),
    FOREIGN KEY (Renter_Email) REFERENCES Users(Email) ON DELETE CASCADE
);

CREATE TABLE prop_type (
    type VARCHAR(20) PRIMARY KEY
);

CREATE TABLE Neighborhood (
    Neighborhood_id SERIAL PRIMARY KEY,
    crime_rate VARCHAR(50),
    nearby_schools VARCHAR(50)
);

CREATE TABLE Property (
    Property_id SERIAL PRIMARY KEY,
    property_type VARCHAR(20),
    location VARCHAR(20),
    description VARCHAR(500),
    city VARCHAR(30),
    state VARCHAR(30),
    price INT,
    availability VARCHAR(30),
    sqft INT,
    no_of_rooms INT,
    neighborhood_id INT,
    FOREIGN KEY (neighborhood_id) REFERENCES Neighborhood(Neighborhood_id) ON DELETE SET NULL,
    FOREIGN KEY (property_type) REFERENCES prop_type(type) ON DELETE SET NULL
);

CREATE TABLE Houses (
    House_id INT PRIMARY KEY,
    building_type VARCHAR(20),
    FOREIGN KEY (House_id) REFERENCES Property(Property_id) ON DELETE CASCADE
);

CREATE TABLE Apartments (
    Apartment_id INT PRIMARY KEY,
    property_type VARCHAR(20),
    building_type VARCHAR(20),
    FOREIGN KEY (Apartment_id) REFERENCES Property(Property_id) ON DELETE CASCADE
);

CREATE TABLE Commercial_Buildings (
    building_id INT PRIMARY KEY,
    type_of_business VARCHAR(100),
    FOREIGN KEY (building_id) REFERENCES Property(Property_id) ON DELETE CASCADE
);

CREATE TABLE Addresses (
    Address_id SERIAL PRIMARY KEY,
    street VARCHAR(40),
    city VARCHAR(30),
    state VARCHAR(20),
    zip_code INT,
    User_email VARCHAR(50),
    FOREIGN KEY (User_email) REFERENCES Users(Email) ON DELETE CASCADE
);

CREATE TABLE Credit_cards (
    card_number BIGINT PRIMARY KEY,
    expiry_date VARCHAR(15),
    cvv CHAR(3),
    billing_address_id INT,
    FOREIGN KEY (billing_address_id) REFERENCES Addresses(Address_id) ON DELETE CASCADE
);

CREATE TABLE Reward_program (
    renter_email VARCHAR(50) PRIMARY KEY,
    reward_points INT,
    FOREIGN KEY (renter_email) REFERENCES Prospective_Renters(Renter_Email) ON DELETE CASCADE
);

CREATE TABLE Booking (
    Booking_ID SERIAL PRIMARY KEY,
    property_id INT,
    booking_date VARCHAR(10),
    card_number BIGINT,
    agent_id VARCHAR(50),
    renter_id VARCHAR(50),
	start_date DATE DEFAULT CURRENT_DATE,
	end_date DATE DEFAULT CURRENT_DATE + INTERVAL '7 days',
    FOREIGN KEY (renter_id) REFERENCES Prospective_Renters(Renter_Email),
    FOREIGN KEY (agent_id) REFERENCES Agents(Agent_Email),
    FOREIGN KEY (card_number) REFERENCES Credit_cards(card_number),
    FOREIGN KEY (property_id) REFERENCES Property(Property_id)
);


INSERT INTO User_type (type) VALUES
('Agent'),
('Renter');

INSERT INTO Users (Email, Name, User_type) VALUES
('agent.kadhir@example.com', 'John Doe', 'Agent'),
('agent.avinash@example.com', 'Susan Smith', 'Agent'),
('renter.harish@example.com', 'Kate Johnson', 'Renter'),
('agent1@example.com', 'Alice Brown', 'Agent'),
('agent2@example.com', 'Bob White', 'Agent'),
('agent3@example.com', 'Charlie Green', 'Agent'),
('agent4@example.com', 'Diana Blue', 'Agent'),
('renter1@example.com', 'Ethan Black', 'Renter'),
('renter2@example.com', 'Fiona Grey', 'Renter'),
('renter3@example.com', 'George Pink', 'Renter'),
('renter4@example.com', 'Hannah Orange', 'Renter'),
('agent.rahul@example.com', 'Rahul Dev', 'Agent'),
('agent.meena@example.com', 'Meena Iyer', 'Agent'),
('renter.vijay@example.com', 'Vijay Kumar', 'Renter'),
('renter.sana@example.com', 'Sana Shaikh', 'Renter');

INSERT INTO Agents (Agent_Email, job_title, Agency, phone) VALUES
('agent.kadhir@example.com', 'Senior Agent', 'DreamHomes', '1234567890'),
('agent.avinash@example.com', 'Field Agent', 'UrbanNest', '9876543210'),
('agent1@example.com', 'Consultant', 'DreamWorks', '1111111111'),
('agent2@example.com', 'Senior Agent', 'UrbanEdge', '2222222222'),
('agent3@example.com', 'Manager', 'Skyline Realty', '3333333333'),
('agent4@example.com', 'Agent', 'NestQuest', '4444444444'),
('agent.rahul@example.com', 'Lead Agent', 'BlueSky Realty', '2223334444'),
('agent.meena@example.com', 'Agent', 'PrimeStay', '3334445555');

INSERT INTO Prospective_Renters (Renter_Email, Budget, preferred_location, move_in_date) VALUES
('renter.harish@example.com', 1500, 'Downtown', '2025-05-01'),
('renter1@example.com', 1600, 'Downtown', '2025-06-01'),
('renter2@example.com', 1700, 'Uptown', '2025-07-01'),
('renter3@example.com', 1800, 'Suburb', '2025-08-01'),
('renter4@example.com', 1900, 'Midtown', '2025-09-01'),
('renter.vijay@example.com', 2000, 'Uptown', '2025-06-01'),
('renter.sana@example.com', 1300, 'Downtown', '2025-06-15');

INSERT INTO prop_type (type) VALUES
('House'),
('Apartment'),
('Commercial');

INSERT INTO Neighborhood (Neighborhood_id, crime_rate, nearby_schools) VALUES
(1, 'Low', 'Lincoln High'),
(2, 'Medium', 'Roosevelt Elementary'),
(3, 'High', 'Maple High School'),
(4, 'Low', 'Springfield Prep');

INSERT INTO Property (Property_id, property_type, location, description, city, state, price, availability, sqft, no_of_rooms, neighborhood_id) VALUES
(101, 'House', 'Maple Street', 'Cozy 3BHK with garden', 'Springfield', 'IL', 1800, 'Available', 1600, 3, 1),
(102, 'Apartment', 'Main Avenue', '2BHK in city center', 'Springfield', 'IL', 1400, 'Available', 1000, 2, 2),
(103, 'Commercial', 'Oak Plaza', 'Office space suitable for startups', 'Springfield', 'IL', 2500, 'Occupied', 2000, 0, 1),
(107, 'House', 'River Rd', 'Luxury 5BHK', 'Springfield', 'IL', 2200, 'Available', 2100, 5, 3),
(108, 'Apartment', 'Skyline Blvd', 'Studio with great view', 'Springfield', 'IL', 1100, 'Available', 600, 1, 4),
(109, 'Commercial', 'Sunset St', 'Warehouse unit', 'Springfield', 'IL', 2400, 'Available', 2500, 0, 3),
(104, 'House', 'Elm Street', 'Charming 4BHK with backyard', 'Springfield', 'IL', 1900, 'Available', 1700, 4, 1),
(105, 'Apartment', 'Park Lane', 'Modern 1BHK with balcony', 'Springfield', 'IL', 1200, 'Available', 800, 1, 2),
(106, 'Commercial', 'Tech Park', 'Shared coworking space', 'Springfield', 'IL', 2300, 'Available', 1800, 0, 1);

INSERT INTO Houses (House_id, building_type) VALUES
(101, 'Detached'),
(107, 'Villa'),
(104, 'Semi-detached');

INSERT INTO Apartments (Apartment_id, property_type, building_type) VALUES
(102, 'Apartment', 'High-rise'),
(105, 'Apartment', 'Mid-rise'),
(108, 'Apartment', 'High-rise');

INSERT INTO Commercial_Buildings (building_id, type_of_business) VALUES
(103, 'Tech Startup Office'),
(106, 'Coworking'),
(109, 'Warehouse');

INSERT INTO Addresses (Address_id, street, city, state, zip_code, User_email) VALUES
(1, '123 Maple St', 'Springfield', 'IL', 62704, 'agent.avinash@example.com'),
(2, '456 Oak St', 'Springfield', 'IL', 62704, 'renter.harish@example.com'),
(3, '789 Pine St', 'Springfield', 'IL', 62704, 'renter.harish@example.com'),
(6, '12 Willow Dr', 'Springfield', 'IL', 62704, 'renter1@example.com'),
(7, '98 Lakeview Ln', 'Springfield', 'IL', 62704, 'renter2@example.com'),
(8, '44 Riverwalk St', 'Springfield', 'IL', 62704, 'renter3@example.com'),
(9, '55 Bridge Rd', 'Springfield', 'IL', 62704, 'renter4@example.com'),
(4, '321 Birch St', 'Springfield', 'IL', 62704, 'renter.vijay@example.com'),
(5, '654 Cedar St', 'Springfield', 'IL', 62704, 'renter.sana@example.com');

INSERT INTO Credit_cards (card_number, expiry_date, cvv, billing_address_id) VALUES
(1111222233334444, '12/26', '123', 2),
(5555666677778888, '09/27', '456', 3),
(1234123412341234, '10/27', '321', 6),
(2345234523452345, '11/27', '432', 7),
(3456345634563456, '01/28', '543', 8),
(4567456745674567, '02/28', '654', 9),
(9999000011112222, '11/26', '789', 4),
(3333444455556666, '08/27', '321', 5);

INSERT INTO Reward_program (renter_email, reward_points) VALUES
('renter.harish@example.com', 120),
('renter1@example.com', 100),
('renter2@example.com', 200),
('renter3@example.com', 300),
('renter4@example.com', 400),
('renter.vijay@example.com', 75),
('renter.sana@example.com', 90);

INSERT INTO Booking (Booking_ID, property_id, booking_date, card_number, agent_id, renter_id) VALUES
(1, 101, '2025-04-10', 1111222233334444, 'agent.kadhir@example.com', 'renter.harish@example.com'),
(2, 102, '2025-04-12', 5555666677778888, 'agent.avinash@example.com', 'renter.harish@example.com'),
(5, 107, '2025-04-19', 1234123412341234, 'agent1@example.com', 'renter1@example.com'),
(6, 108, '2025-04-20', 2345234523452345, 'agent2@example.com', 'renter2@example.com'),
(7, 109, '2025-04-21', 3456345634563456, 'agent3@example.com', 'renter3@example.com'),
(3, 104, '2025-04-15', 9999000011112222, 'agent.rahul@example.com', 'renter.vijay@example.com'),
(4, 105, '2025-04-18', 3333444455556666, 'agent.meena@example.com', 'renter.sana@example.com');

--Error Fix:
SELECT setval(pg_get_serial_sequence('booking', 'booking_id'), COALESCE(MAX(Booking_ID), 1), true) FROM Booking;
SELECT setval(pg_get_serial_sequence('booking', 'booking_id'), COALESCE(MAX(Booking_ID), 1), true) FROM Booking;
SELECT setval(pg_get_serial_sequence('addresses', 'address_id'), COALESCE(MAX(Address_ID), 1), true) FROM addresses;


/*
drop table houses;
drop table Booking;
drop table Commercial_Buildings;
drop table Apartments;
drop table property;
drop table neighborhood;
drop table credit_cards;
drop table addresses;
drop table reward_program;
drop table Prospective_renters;
drop table Agents;
drop table Users;
drop table User_type;
drop table prop_type;
*/




