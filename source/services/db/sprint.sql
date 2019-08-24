CREATE TABLE sprint (
	sprint_id	SERIAL		PRIMARY KEY,
	sprint_num	INTEGER		NOT NULL,
	sprint_name	VARCHAR (128)	NOT NULL,
	board_id	INTEGER		REFERENCES board(board_id) ON DELETE CASCADE,
	status		INTEGER		NOT NULL,
	created_at	TIMESTAMP	NOT NULL,
	closed_at	TIMESTAMP,
	begin_time	TIMESTAMP,
	end_time	TIMESTAMP
)
