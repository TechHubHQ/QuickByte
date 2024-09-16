package database

import (
	"database/sql"
	"log"

	_ "github.com/lib/pq"
)

func ConnectSupaBase() (*sql.DB, error) {
	connStr := "postgres://postgres.culpgrvtanhbcrukkzjs:Bangaram@118@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Error while connecting to Supabase: ", err)
	}

	return db, nil
}
