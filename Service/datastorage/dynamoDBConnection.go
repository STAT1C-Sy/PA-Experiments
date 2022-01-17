package datastorage

import (
	"fmt"
	"net/url"
	"strings"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/endpoints"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

const (
	awsTypeString                = "S" // see https://docs.aws.amazon.com/sdk-for-go/api/service/dynamodb/#AttributeDefinition
	awsPrimaryKeyType            = "HASH"
	envDynamoEndpoint            = "DYNAMODB_ENDPOINT"
	TableCustomFieldDefinitions  = "Customfields"
	TableCustomFieldValueOptions = "CustomfieldValueoptions"
)

var table2PrimaryKey = map[string]string{
	"CustomfieldsValueoptions": "metadata",
	"CustomfieldsMetadata":     "uuid",
	"Customfields":             "uuid",
}

// DynamoDbConnection implementing dbConnection
type DynamoDbConnection struct {
	tableName string
}

var dbClient *dynamodb.DynamoDB

func createDynamoDBClient() error {
	if dbClient == nil {
		sess, err := getSessionForDynamoEndpoint("http://localhost:8000", "us-west-2")
		if err != nil {
			return err
		}
		endpointCfg := aws.NewConfig().
			WithEndpoint("http://localhost:8000"). // provide custom endpoints only for DynamoDB
			WithCredentialsChainVerboseErrors(true)
		dbClient = dynamodb.New(sess, endpointCfg)
	}
	return nil
}

// Read reads entry from specified table in DynamoDB
func (d DynamoDbConnection) Read(key string, valuePtr interface{}) error {
	if err := createDynamoDBClient(); err != nil {
		return err
	}
	primaryKey := table2PrimaryKey[d.tableName]
	result, err := dbClient.GetItem(&dynamodb.GetItemInput{
		TableName: aws.String(d.tableName),
		Key: map[string]*dynamodb.AttributeValue{
			primaryKey: {
				S: aws.String(key),
			},
		},
	})
	if err != nil {
		return err
	}
	if len(result.Item) == 0 {
		return fmt.Errorf("item for key '%s' not found", key)
	}
	return dynamodbattribute.UnmarshalMap(result.Item, &valuePtr)
}

// Query entrys from specified table in DynamoDB
func (d DynamoDbConnection) Query(keyname string, key string, valuePtr interface{}) error {
	if err := createDynamoDBClient(); err != nil {
		return err
	}

	result, err := dbClient.Query(&dynamodb.QueryInput{
		TableName:              aws.String(d.tableName),
		KeyConditionExpression: aws.String(keyname + " = :key"),
		ExpressionAttributeValues: map[string]*dynamodb.AttributeValue{
			":key": {
				S: aws.String(key),
			},
		},
	})
	if err != nil {
		return err
	}

	if len(result.Items) == 0 {
		return fmt.Errorf("item for key '%s' not found", key)
	}

	return dynamodbattribute.UnmarshalListOfMaps(result.Items, &valuePtr)
}

// Test the connection to the database
func (d DynamoDbConnection) TestConnection() error {
	return createDynamoDBClient()
}

func getSessionForDynamoEndpoint(endpoint, awsRegion string) (*session.Session, error) {
	// if we're connecting to a local DynamoDB, use hardcoded credentials
	if endpointIsLocalhost(endpoint) {
		return session.NewSession(&aws.Config{
			Region:      aws.String("us-west-2"),
			Credentials: credentials.NewStaticCredentials("AKID", "SECRET_KEY", "TOKEN"),
			Endpoint:    aws.String(endpoint),
		})
	}
	return session.NewSession(&aws.Config{
		Region:                        aws.String(awsRegion),
		DisableSSL:                    aws.Bool(true), // we disable SSL so that the AWS API call will be handled by the Envoy proxy instead of the service container directly
		CredentialsChainVerboseErrors: aws.Bool(true),
		STSRegionalEndpoint:           endpoints.RegionalSTSEndpoint, // this makes SDK resolve STS endpoint to http://sts.us-west-2.amazonaws.com instead of default global http://sts.amazonaws.com
	})
}

// endpointIsLocalhost checks whether a given endpoint is referring to a the localhost
// Empty URLs as well as invalid URLs (missing scheme, ...) are assumed to not point to localhost
func endpointIsLocalhost(endpoint string) bool {
	u, err := url.Parse(endpoint)
	if err != nil {
		return false
	}
	return strings.HasPrefix(u.Host, "127.") || u.Hostname() == "localhost" || u.Hostname() == "::1"
}
