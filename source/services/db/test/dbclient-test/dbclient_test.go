package main

import (
	"github.com/andrewwangzy/fun_with_flags/source/services/db/dbclient"
	"testing"
)

func TestDbClient(t *testing.T) {
	dbClient := dbclient.NewDbClientDefault()
	if dbClient == nil {
		t.Errorf("Failed to create db.DbClient")
		t.FailNow()
	}
}
