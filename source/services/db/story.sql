create TABLE story (
	story_id	SERIAL		PRIMARY KEY,
	story_name	VARCHAR (128)	NOT NULL,
	story_type	INTEGER		NOT NULL,
	created_at	TIMESTAMP	NOT NULL,
	created_by	INTEGER		REFERENCES users(user_id) ON DELETE RESTRICT,
	board_id	INTEGER		REFERENCES board(board_id) ON DELETE CASCADE,
	epic_id		INTEGER		REFERENCES epic(epic_id) ON DELETE RESTRICT,
	assignee	INTEGER		REFERENCES users(user_id),
	reporter	INTEGER		REFERENCES users(user_id),
	description	VARCHAR (1024),
	parent_story	INTEGER		REFERENCES story(story_id)
);
