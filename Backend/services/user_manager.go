package services

import (
	"fmt"
	"log"
	"strings"

	database "github.com/TechHubHQ/QuickByte/Backend/database/prod"
	"github.com/TechHubHQ/QuickByte/Backend/security"
	"golang.org/x/crypto/bcrypt"
)

func HandleLogin(username string, password string) (string, error) {
	db, err := database.ConnectSupaBase()
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	defer db.Close()

	// Query the qb_user table with the username
	var storedUsername string
	var storedPassword string
	err = db.QueryRow("SELECT username, password FROM qb_user WHERE username = $1", username).Scan(&storedUsername, &storedPassword)
	if err != nil {
		log.Println(err)
		return "", err
	}

	// Compare the provided password with the stored password
	err = bcrypt.CompareHashAndPassword([]byte(storedPassword), []byte(password))
	if err != nil {
		log.Println(err)
		return "", err
	}

	// Generate a JWT token
	token, err := security.GenerateJWT(username)
	if err != nil {
		log.Fatal(err)
		return "", nil
	}

	return token, nil
}

func HandleSignUp(first_name string, last_name string, password string, phone_number string, email string, street string, city string, state string, zip string) (string, error) {
	db, err := database.ConnectSupaBase()
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	defer db.Close()

	username := strings.ToLower(first_name + " " + last_name)

	full_address := fmt.Sprintf("%s, %s, %s, %s", street, city, state, zip)

	// Hash the password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), 12)
	if err != nil {
		return "", err
	}

	_, err = db.Exec(`
		INSERT INTO qb_user (
			username, email, password, first_name, last_name, 
			phone_number, street, city, state, zip_code, country, full_address
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
		username, email, string(hashedPassword),
		first_name, last_name,
		phone_number,
		street, city, state, zip,
		"India",
		full_address,
	)
	if err != nil {
		return "", err
	}

	// Generate a JWT token
	token, err := security.GenerateJWT(username)
	if err != nil {
		log.Fatal(err)
		return "", nil
	}

	return token, nil
}
