CREATE TABLE team (
	team_id		SERIAL		PRIMARY KEY,
	team_name	VARCHAR (32)	UNIQUE NOT NULL,
	created_at	TIMESTAMP	NOT NULL,
	created_by	INTEGER		REFERENCES users(user_id),
	admin_id	INTEGER		REFERENCES users(user_id)
);
