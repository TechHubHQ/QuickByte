package api

import (
	"github.com/TechHubHQ/QuickByte/Backend/security"
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

	app.POST("/generate-token", func(context *gin.Context) {
		username := context.PostForm("username")
		token, err := security.GenerateJWt(username)
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

	app.POST("/validate-token", func(context *gin.Context) {
		tokenstring := context.PostForm("token")
		username, err := security.ValidateJWT(tokenstring)

		if err != nil {
			context.JSON(401, gin.H{"error": "Invalid token"})
			return
		}
		context.JSON(200, gin.H{"username": username})
	})
}
