package database

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
)

func ConnectPG() (*sql.DB, error) {

	err := godotenv.Load()
	if err != nil {
		log.Printf("Error loading .env file: %v\n", err)
		return nil, err
	}

	DB_HOST 			:= os.Getenv("PG_HOST")
	DB_PORT 			:= os.Getenv("PG_PORT")
	DB_USER 			:= os.Getenv("PG_USER")
	DB_PASSWORD 	:= os.Getenv("PG_PASSWORD")
	DB_NAME 			:= os.Getenv("PG_NAME")

	conn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

	// Open the connection
	db, err := sql.Open("postgres", conn)
	if err != nil {
		log.Fatal(err)
		return nil, err
	}

	return db, nil
}
