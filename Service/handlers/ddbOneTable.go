package handlers

import (
	"fmt"
	"net/http"

	"github.com/STAT1C-Sy/PA2-Service/datastorage"
	"github.com/STAT1C-Sy/PA2-Service/model"
	"github.com/STAT1C-Sy/PA2-Service/performance"
	"github.com/gin-gonic/gin"
)

func HandleRequestWithOneTable(c *gin.Context) {
	customfield_id := c.Param("id")

	resp, err := getDataFromSingleDatabaseTable(customfield_id)

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, resp)
}

func getDataFromSingleDatabaseTable(key string) ([]model.CustomFieldValueOptions, error) {
	conn := datastorage.GetConnection(datastorage.ConnectionDetails{TableName: datastorage.TableCustomFieldDefinitions})

	var customfieldDefinition *model.ConfigCustomField

	start := performance.GetTimestamp()

	err := conn.Read(key, &customfieldDefinition)

	end := performance.GetTimestamp()

	performance.LogResult(start, end, performance.METHOD_SINGLEDDB)

	if err != nil {
		fmt.Println(err)
		return []model.CustomFieldValueOptions{}, nil
	}

	result := []model.CustomFieldValueOptions{}

	for _, vo := range customfieldDefinition.CustomFieldValues {
		ele := model.CustomFieldValueOptions{
			Value:       vo.Value,
			DisplayText: vo.Text,
		}

		result = append(result, ele)
	}

	return result, nil
}
