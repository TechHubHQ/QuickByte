package security

import (
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v4"
	"github.com/joho/godotenv"
)

func GenerateJWT(Username string) (string, error) {
	err := godotenv.Load()
	if err != nil {
		log.Printf("Error loading .env file: %v\n", err)
		return "", err
	}

	secretkey := os.Getenv("SECRET_KEY")
	if secretkey == "" {
		log.Println("SECRET_KEY not found in .env file")
		return "", err
	}

	expirytime := time.Now().Add(24 * time.Hour)
	claims := &jwt.RegisteredClaims{
		ExpiresAt: jwt.NewNumericDate(expirytime),
		Subject:   Username,
		Issuer:    "Go-Auth",
		IssuedAt:  jwt.NewNumericDate(time.Now()),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	Tokenstring, err := token.SignedString([]byte(secretkey))
	if err != nil {
		log.Printf("Error signing token: %v\n", err)
		return "", err
	}

	return Tokenstring, nil
}

func ValidateJWT(tokenString string) (string, error) {
	if !strings.HasPrefix(tokenString, "Bearer ") {
		return "", errors.New("invalid token format")
	}

	token := strings.TrimPrefix(tokenString, "Bearer ")

	secretKey := os.Getenv("SECRET_KEY")
	if secretKey == "" {
		return "", errors.New("SECRET_KEY not found")
	}

	parsedToken, err := jwt.Parse(token, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(secretKey), nil
	})

	if err != nil {
		return "", err
	}

	claims, ok := parsedToken.Claims.(jwt.MapClaims)
	if !ok || !parsedToken.Valid {
		return "", errors.New("invalid token")
	}

	return claims["sub"].(string), nil
}
