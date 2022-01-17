package datastorage

type ConnectionDetails struct {
	TableName       string
}

// Connection is an interface which contains DB specific CRUD methods and properties
type DBConnection interface {
	Read(key string, valuePtr interface{}) error
	Query(keyname string, key string, valuePtr interface{}) error
	TestConnection() error
}

// GetConnection returns DynamoDB connection
func GetConnection(connectionDetails ConnectionDetails) DBConnection {
	var connectionDynamoDb DynamoDbConnection
	connectionDynamoDb.tableName = connectionDetails.TableName
	return connectionDynamoDb
}