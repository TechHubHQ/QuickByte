package api

import "github.com/gin-gonic/gin"

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
}