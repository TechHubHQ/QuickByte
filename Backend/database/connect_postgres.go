package database

import (
	"database/sql"
	"log"
)

func ConnectPG() (*sql.DB, error) {
	db, err := sql.Open("postgres", "user=postgres password=Bangaram@118 host=localhost sslmode=disable")
	if err != nil {
		log.Fatal(err)
		return nil, err
	}

	return db, nil
}
