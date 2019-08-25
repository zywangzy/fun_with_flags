CREATE TABLE board (
	board_id	SERIAL		PRIMARY KEY,
	board_name	varchar (128)	NOT NULL,
	board_note	text,
	board_type	integer		NOT NULL, -- personal or team, only one of user_id or team_id will be used
	user_id		integer 	REFERENCES users(user_id) ON DELETE CASCADE,
	team_id		integer		REFERENCES team(team_id) ON DELETE CASCADE,
	admin_id	integer		NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
	created_at	timestamp	NOT NULL
);
