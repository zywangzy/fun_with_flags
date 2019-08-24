CREATE TABLE board (
	board_id	SERIAL		PRIMARY KEY,
	board_name	VARCHAR (128)	NOT NULL,
	board_note	VARCHAR (1024),
	created_at	TIMESTAMP	NOT NULL,
	admin_id	INTEGER 	REFERENCES users(user_id) ON DELETE RESTRICT
);
