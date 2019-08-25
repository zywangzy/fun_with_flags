create TABLE story (
	story_id	SERIAL		PRIMARY KEY,
	story_name	varchar (128)	NOT NULL,
	story_type	integer		NOT NULL,
	status		integer		NOT NULL,
	estimate	integer,
	created_at	timestamp	NOT NULL,
	created_by	integer		REFERENCES users(user_id) ON DELETE RESTRICT,
	closed_at	timestamp	NOT NULL,
	closed_by	integer		REFERENCES users(user_id) ON DELETE RESTRICT,
	board_id	integer		REFERENCES board(board_id) ON DELETE CASCADE,
	epic_id		integer		REFERENCES epic(epic_id) ON DELETE RESTRICT,
	assignee	integer		REFERENCES users(user_id),
	reporter	integer		REFERENCES users(user_id),
	description	text,
	parent_story	integer		REFERENCES story(story_id)
);
