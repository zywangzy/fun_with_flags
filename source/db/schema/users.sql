CREATE TABLE users (
	user_id		SERIAL		PRIMARY KEY,
	username	varchar (32)	UNIQUE NOT NULL,
	nickname	varchar (32),
	password	bytea		NOT NULL,
	salt		bytea		NOT NULL,
	email		varchar (128)	UNIQUE NOT NULL,
	created_at	timestamp	NOT NULL,
	last_login	timestamp,
	avatar_id	char (16)
);

