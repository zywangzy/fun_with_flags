CREATE TABLE epic (
	epic_id		SERIAL		PRIMARY KEY,
	epic_name	varchar (128)	NOT NULL,
	epic_note	text,
	board_id	integer		REFERENCES board(board_id) ON DELETE CASCADE
);
