package services

import (
	"fmt"
	"log"

	"github.com/TechHubHQ/QuickByte/Backend/database"
	"github.com/TechHubHQ/QuickByte/Backend/security"
	"golang.org/x/crypto/bcrypt"
)

func HandleLogin(username string, password string) (string, error) {
	db, err := database.ConnectDB()
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

func HandleSignUp(username string, password string, email string, street string, city string, state string, zip string) (string, error) {
	db, err := database.ConnectDB()
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	defer db.Close()

	// Hash the password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), 12)
	if err != nil {
		return "", err
	}

	// Insert the new user into the qb_user table
	_, err = db.Exec(`INSERT INTO qb_user (username, email, password, first_name, last_name, phone_number, address) 
		VALUES ($1, $2, $3, $4, $5, $6, $7)`,
		username, email, string(hashedPassword), "", "", "", fmt.Sprintf("%s, %s, %s, %s", street, city, state, zip))
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
