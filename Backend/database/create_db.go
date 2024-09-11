package database

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func CreateDB() error {
	err := godotenv.Load()
	if err != nil {
		log.Printf("Error loading .env file: %v\n", err)
		return err
	}

	DB_HOST := os.Getenv("DB_HOST")
	DB_PORT := os.Getenv("DB_PORT")
	DB_USER := os.Getenv("DB_USER")
	DB_PASSWORD := os.Getenv("DB_PASSWORD")
	DB_NAME := os.Getenv("DB_NAME")

	// Check if database exists
	exists, err := checkDBExists()
	if err != nil {
		return err
	}

	if !exists {
		// Create database
		conn := fmt.Sprintf("host=%s port=%s user=%s password=%s sslmode=disable",
			DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
		db, err := sql.Open("postgres", conn)
		if err != nil {
			log.Fatal(err)
		}
		defer db.Close()

		_, err = db.Exec(fmt.Sprintf("CREATE DATABASE %s", DB_NAME))
		if err != nil {
			log.Fatal("error creating DB", err)
		}
	}

	// Connect to database
	conn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
	db, err := sql.Open("postgres", conn)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Execute schema
	schema, err := os.ReadFile("schema.sql")
	if err != nil {
		log.Fatal("Error reading schema.sql", err)
		return err
	}
	_, err = db.Exec(string(schema))
	if err != nil {
		log.Fatal(err)
	}

	return nil
}

func checkDBExists() (bool, error) {
	db_admin, err := ConnectPG()
	if err != nil {
		log.Fatal(err)
		return false, err
	}
	defer db_admin.Close()

	var exists bool
	err = db_admin.QueryRow("SELECT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'qbdb')").Scan(&exists)
	if err != nil {
		return false, err
	}

	return exists, nil
}
