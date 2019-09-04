CREATE TABLE board (
	board_id	SERIAL		PRIMARY KEY,
	board_name	varchar (128)	NOT NULL,
	board_note	text,
	project_id	integer		REFERENCES project(project_id) ON DELETE CASCADE,
	admin_id	integer		NOT NULL REFERENCES users(user_id),
	created_at	timestamp	NOT NULL
);

