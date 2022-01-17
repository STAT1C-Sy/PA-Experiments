package handlers

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/STAT1C-Sy/PA2-Service/datastorage"
	"github.com/STAT1C-Sy/PA2-Service/model"
	"github.com/STAT1C-Sy/PA2-Service/performance"
	"github.com/gin-gonic/gin"
)

func HandleRequestWithPostgres(c *gin.Context) {
	customfield_id := c.Param("id")

	resp, err := getDataFromPostgres(customfield_id)

	if err != nil {
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, resp)
}

func getDataFromPostgres(key string) ([]model.CustomFieldValueOptions, error) {
	conn, err := datastorage.GetPostgresConnection()

	if err != nil {
		return []model.CustomFieldValueOptions{}, err
	}

	defer conn.Close()

	var rows *sql.Rows

	start := performance.GetTimestamp()

	rows, err = conn.Query("SELECT text, value FROM Valueoptions WHERE metadata='" + key + "'")

	if err != nil {
		return []model.CustomFieldValueOptions{}, err
	}

	defer rows.Close()

	result := []model.CustomFieldValueOptions{}

	for rows.Next() {
		var displayText string
		var value string

		rows.Scan(&displayText, &value)
		result = append(result, model.CustomFieldValueOptions{Value: value, DisplayText: displayText})
	}

	end := performance.GetTimestamp()

	performance.LogResult(start, end, performance.METHOD_POSTGRES)

	return result, nil

}
