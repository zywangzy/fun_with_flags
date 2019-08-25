CREATE TABLE epic (
	epic_id		SERIAL		PRIMARY KEY,
	epic_name	VARCHAR (128)	NOT NULL,
	epic_note	TEXT,
	board_id	INTEGER		REFERENCES board(board_id) ON DELETE CASCADE
);
