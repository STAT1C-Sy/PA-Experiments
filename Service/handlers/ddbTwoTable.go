package handlers

import (
	"fmt"
	"net/http"

	"github.com/STAT1C-Sy/PA2-Service/datastorage"
	"github.com/STAT1C-Sy/PA2-Service/model"
	"github.com/STAT1C-Sy/PA2-Service/performance"
	"github.com/gin-gonic/gin"
)

func HandleRequestWithTwoTables(c *gin.Context) {
	customfield_id := c.Param("id")

	resp, err := getDataFromTwoDatabaseTables(customfield_id)

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, resp)
}

func getDataFromTwoDatabaseTables(key string) ([]model.CustomFieldValueOptions, error) {
	conn := datastorage.GetConnection(datastorage.ConnectionDetails{TableName: datastorage.TableCustomFieldValueOptions})

	var customFieldValueOptions []*model.ConfigCustomFieldValue

	start := performance.GetTimestamp()

	err := conn.Query("metadata", key, &customFieldValueOptions)

	end := performance.GetTimestamp()

	performance.LogResult(start, end, performance.METHOD_TWODDB)

	if err != nil {
		fmt.Println(err)
		return []model.CustomFieldValueOptions{}, nil
	}

	result := []model.CustomFieldValueOptions{}

	for _, vo := range customFieldValueOptions {
		ele := model.CustomFieldValueOptions{
			Value:       vo.Value,
			DisplayText: vo.Text,
		}

		result = append(result, ele)
	}

	return result, nil
}
