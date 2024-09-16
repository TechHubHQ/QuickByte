-- Create the qb_user table
CREATE TABLE qb_user (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone_number VARCHAR(20),
  street VARCHAR(50),
  city VARCHAR(50),
  state VARCHAR(50),
  zip_code VARCHAR(50),
  country VARCHAR(50),
  full_address TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add a unique constraint to the email column
ALTER TABLE qb_user
ADD CONSTRAINT unique_email UNIQUE (email);

-- Add a unique constraint to the username column
ALTER TABLE qb_user
ADD CONSTRAINT unique_username UNIQUE (username);


-- Create an index on the username column
CREATE INDEX idx_username ON qb_user (username);