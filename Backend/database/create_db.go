package database

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"runtime"

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

	// Connect to database
	conn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
	db, err := sql.Open("postgres", conn)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, currentFilePath, _, _ := runtime.Caller(0)
	schemaPath := filepath.Join(filepath.Dir(currentFilePath), "schema.sql")

	schema, err := os.ReadFile(schemaPath)
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
