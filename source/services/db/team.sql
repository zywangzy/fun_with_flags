CREATE TABLE team (
	team_id		SERIAL		PRIMARY KEY,
	team_name	varchar (32)	UNIQUE NOT NULL,
	created_at	timestamp	NOT NULL,
	created_by	integer		REFERENCES users(user_id),
	admin_id	integer		REFERENCES users(user_id)
);
