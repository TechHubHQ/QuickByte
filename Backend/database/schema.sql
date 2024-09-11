CREATE ROLE qbdb WITH PASSWORD 'Bangaram@118';

GRANT CONNECT ON DATABASE quickdb TO qbdb;
GRANT USAGE ON SCHEMA public TO qbdb;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE qb_user TO qbdb;

-- Connect to the QuickDB database
\c QuickDB

-- Create the qb_user table
CREATE TABLE qb_user (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone_number VARCHAR(20),
  address TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add a unique constraint to the email column
ALTER TABLE qb_user
ADD CONSTRAINT unique_email UNIQUE (email);

-- Add a unique constraint to the username column
ALTER TABLE qb_user
ADD CONSTRAINT unique_username UNIQUE (username);