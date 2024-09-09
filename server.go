package main

import (
	"time"

	"github.com/TechHubHQ/QuickByte/Backend/api"
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
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))


	// configure routes
	api.ApiRouter(app)

	app.Run()
}
