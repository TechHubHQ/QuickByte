package database

import (
	"os"
	"log"
	"fmt"
	"database/sql"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func ConnectDB() (*sql.DB, error) {
	err := godotenv.Load()
	if err != nil {
		log.Printf("Error loading .env file: %v\n", err)
		return nil, err
	}

	DB_HOST 			:= os.Getenv("SBPG_HOST")
	DB_PORT				:= os.Getenv("SBPG_PORT")
	DB_USER				:= os.Getenv("SBPG_USER")
	DB_PASSWORD		:= os.Getenv("SBPG_PASSWORD")
	DB_NAME				:= os.Getenv("SBPG_NAME")

	conn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", 
												DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
												
	db, err := sql.Open("postgres", conn)

	if err != nil {
		return nil, err
	}

	return db, nil
}