package database

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
)

func CreateDB() error {
	// Connect to the database
	db, err := ConnectDB()
	if err != nil {
		log.Fatal(err)
		return err
	}
	defer db.Close()

	// Read the schema file
	_, currentFilePath, _, _ := runtime.Caller(0)
	schemaPath := filepath.Join(filepath.Dir(currentFilePath), "schema.sql")

	schema, err := os.ReadFile(schemaPath)
	if err != nil {
		log.Fatal("Error reading schema.sql", err)
		return err
	}

	// Extract table names using regex
	tableRegex := regexp.MustCompile(`(?i)CREATE\s+TABLE\s+(\w+)`)
	tableMatches := tableRegex.FindAllStringSubmatch(string(schema), -1)

	for _, match := range tableMatches {
		if len(match) < 2 {
			continue
		}
		tableName := match[1]

		// Check if the table exists
		var existingTableName string
		err = db.QueryRow("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name=$1", tableName).Scan(&existingTableName)

		if err == nil && existingTableName == tableName {
			log.Printf("Table '%s' already exists. Skipping its creation.\n", tableName)
			continue
		} else if err != sql.ErrNoRows {
			log.Fatal("Error checking for table existence:", err)
			return err
		}

		tableStartIndex := strings.Index(strings.ToUpper(string(schema)), fmt.Sprintf("CREATE TABLE %s", strings.ToUpper(tableName)))
		nextTableIndex := strings.Index(string(schema)[tableStartIndex:], "CREATE TABLE")

		var tableSQL string
		if nextTableIndex != -1 {
			tableSQL = string(schema)[tableStartIndex : tableStartIndex+nextTableIndex]
		} else {
			tableSQL = string(schema)[tableStartIndex:]
		}

		_, err = db.Exec(tableSQL)
		if err != nil {
			log.Printf("Error creating table '%s': %v\n", tableName, err)
			return err
		}

		log.Printf("Table '%s' created successfully.\n", tableName)

		log.Println("Database schema executed successfully for new tables.")
	}
	return nil
}
