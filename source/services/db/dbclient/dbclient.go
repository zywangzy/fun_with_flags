package dbclient

import (
        "database/sql"
        "fmt"
        _ "github.com/lib/pq"
        "log"
        "time"
)

const(
        PORT = "5432"
        MAX_RETRY = 10
        CONNECTION_STR = "host=dbpostgres user=docker password=docker dbname=docker port=5432 sslmode=disable"
)

// type hashPwdFunc func(string, string) (string, error)

type DbClient struct {
    dbHandle *sql.DB
}

func NewDbClient(connStr string) *DbClient {
        log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds | log.Llongfile)
        dbClient := new(DbClient)
        if err := dbClient.ConnectPostgresDB(connStr); err != nil {
                return nil
        }
        return dbClient
}

func NewDbClientWithParams(host string, user string, password string, dbname string, port string) *DbClient {
        connStr := fmt.Sprintf("host=%v user=%v password=%v dbname=%v port=%v sslmode=disable", host, user, password, dbname, port)
        return NewDbClient(connStr)
}

func NewDbClientDefault() *DbClient {
        return NewDbClient(CONNECTION_STR)
}

func (dbCli *DbClient) ConnectPostgresDB(connStr string) error {
        retryCount := 0
        var retErr, err error
        for retryCount < MAX_RETRY {
                retryCount += 1
                dbCli.dbHandle, err = sql.Open("postgres", connStr)
                if err == nil {
                        log.Print("ConnectPostgresDB succeeded")
                        return nil
                } else {
                        log.Printf("ConnectPostgresDB failed %v times: %v", retryCount, err.Error())
                        if retryCount == MAX_RETRY {
                                retErr = err
                                return retErr
                        }
                        time.Sleep(5 * time.Second)
                }
        }
        err = dbCli.dbHandle.Ping()
        if err != nil {
                log.Printf("ConnectPostgresDB: Could not ping the database - %v", err)
                retErr = err
        }
        return retErr
}