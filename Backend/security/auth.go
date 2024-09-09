package security

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v4"
	"github.com/joho/godotenv"
)

func GenerateJWt(Username string) (string, error) {
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

func ValidateJWT(tokenstring string) (string, error) {
	secretKey := os.Getenv("SECRET_KEY")
	if secretKey == "" {
		log.Println("SECRET_KEY not found in environment variables")
		return "", fmt.Errorf("SECRET_KEY not found")
	}

	token, err := jwt.Parse(tokenstring, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(secretKey), nil
	})
	if err != nil {
		log.Printf("Error parsing token: %v\n", err)
		return "", err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims["sub"].(string), nil
	} else {
		log.Println("Invalid token")
		return "", fmt.Errorf("invalid token")
	}
}
