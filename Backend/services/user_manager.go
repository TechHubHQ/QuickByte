package services

import (
	"log"

	"github.com/TechHubHQ/QuickByte/Backend/database"
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

	return "Login successful", nil
}

func HandleSignUp() {

}
