CREATE TABLE board (
	board_id	SERIAL		PRIMARY KEY,
	board_name	VARCHAR (128)	NOT NULL,
	board_note	VARCHAR (1024),
	board_type	INTEGER		NOT NULL, -- personal or team, only one of user_id or team_id will be used
	user_id		INTEGER 	REFERENCES users(user_id) ON DELETE CASCADE,
	team_id		INTEGER		REFERENCES team(team_id) ON DELETE CASCADE,
	admin_id	INTEGER		NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
	created_at	TIMESTAMP	NOT NULL,
);
