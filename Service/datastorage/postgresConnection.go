package datastorage

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

const (
	host     = "localhost"
	port     = 5432
	user     = "username"
	password = "password"
	dbname   = "default_database"
)

func GetPostgresConnection() (*sql.DB, error) {
	// connection string
	psqlconn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)

	// open database
	db, err := sql.Open("postgres", psqlconn)

	if err != nil {
		return &sql.DB{}, err
	}

	// check db
	err = db.Ping()

	if err != nil {
		return &sql.DB{}, err
	}

	return db, nil
}
