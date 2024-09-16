package main

import (
	"log"

	"github.com/TechHubHQ/QuickByte/Backend/api"
	"github.com/TechHubHQ/QuickByte/Backend/database"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	// set up app
	app := gin.Default()

	// set trusted proxies
	app.SetTrustedProxies([]string{"127.0.0.1", "192.168.1.0/24"})

	// set up CORSMiddleware
	app.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: false,
	}))

	// configure routes
	api.ApiRouter(app)

	// create the database
	err := database.CreateDB()
	if err != nil {
		log.Fatal("Error Creating DB: ", err)
	}

	// run the server
	app.Run(":8080")
}
