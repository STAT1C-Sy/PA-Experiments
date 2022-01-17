package main

import (
	"github.com/STAT1C-Sy/PA2-Service/handlers"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	r.GET("/:id/valueoptions1", handlers.HandleRequestWithOneTable)

	r.GET("/:id/valueoptions2", handlers.HandleRequestWithTwoTables)

	r.GET("/:id/valueoptions3", handlers.HandleRequestWithPostgres)

	r.Run()
}
