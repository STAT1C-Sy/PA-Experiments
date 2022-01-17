package performance

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

const (
	METHOD_POSTGRES  = "POSTGRES"
	METHOD_SINGLEDDB = "DDB_SINGLE"
	METHOD_TWODDB    = "DDB_TWO"
	LOGFILE          = "performance_data.txt"
)

func GetTimestamp() int64 {
	return time.Now().UTC().UnixNano()
}

func LogResult(start int64, end int64, method string) {
	file, err := os.OpenFile(LOGFILE, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
	if err != nil {
		log.Fatal(err)
	}

	file.WriteString(fmt.Sprintf("start:%s;end:%s;method:%s\n", strconv.FormatInt(start, 10), strconv.FormatInt(end, 10), method))
	file.Close()
}
