package api

import (
	"github.com/TechHubHQ/QuickByte/Backend/schema"
	"github.com/TechHubHQ/QuickByte/Backend/security"
	"github.com/TechHubHQ/QuickByte/Backend/services"
	"github.com/gin-gonic/gin"
)

func ApiRouter(app *gin.Engine) {
	app.GET("/", func(context *gin.Context) {
		context.JSON(200, gin.H{
			"message": "Hello World!",
		})
	})

	app.GET("/test", func(context *gin.Context) {
		context.JSON(200, gin.H{
			"message": "API call test passed!",
		})
	})

	app.POST("/v1/generate-token", func(context *gin.Context) {
		var req schema.LoginRequest
		if err := context.ShouldBindJSON(&req); err != nil {
			context.JSON(400, gin.H{"error": "Invalid request body"})
			return
		}
		token, err := security.GenerateJWT(req.Username)
		if err != nil {
			context.JSON(500, gin.H{
				"error": "Failed to generate token",
			})
			return
		}
		context.JSON(200, gin.H{
			"token": token,
		})
	})

	app.POST("/v1/validate-token", func(context *gin.Context) {
		var req struct {
			Token string `json:"token"`
		}
		if err := context.ShouldBindJSON(&req); err != nil {
			context.JSON(400, gin.H{"error": "Invalid request body"})
			return
		}
		username, err := security.ValidateJWT(req.Token)
		if err != nil {
			context.JSON(401, gin.H{"error": "Invalid token"})
			return
		}
		context.JSON(200, gin.H{"username": username})
	})

	app.POST("/v1/login", func(context *gin.Context) {
		var req schema.LoginRequest
		if err := context.ShouldBindJSON(&req); err != nil {
			context.JSON(400, gin.H{"error": "Invalid request body"})
			return
		}
		token, err := services.HandleLogin(req.Username, req.Password)
		if err != nil {
			context.JSON(401, gin.H{"error": err.Error()})
			return
		}
		context.JSON(200, gin.H{"token": token})
	})

	app.POST("/v1/signup", func(context *gin.Context) {
		var req schema.SignupRequest
		if err := context.ShouldBindJSON(&req); err != nil {
			context.JSON(400, gin.H{"error": err.Error()})
			return
		}
		token, err := services.HandleSignUp(req.FirstName, req.LastName, req.Password, req.Phone, req.Email, req.Street, req.City, req.State, req.ZipCode)
		if err != nil {
			context.JSON(400, gin.H{"error": "Signup failed: " + err.Error()})
			return
		}
		context.JSON(200, gin.H{"token": token})
	})
}
