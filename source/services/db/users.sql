CREATE TABLE users (
	user_id     SERIAL	  PRIMARY KEY,
	username    VARCHAR (32)  UNIQUE NOT NULL,
	password    BYTEA	  NOT NULL,
	salt        BYTEA	  NOT NULL,
	email       VARCHAR (128) UNIQUE NOT NULL,
	created_at  TIMESTAMP     NOT NULL,
	last_login  TIMESTAMP,
	avatar_id   CHAR (16)
);
