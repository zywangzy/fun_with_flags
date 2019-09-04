CREATE TABLE project (
	project_id	SERIAL		PRIMARY KEY,
	project_name	varchar (128)	NOT NULL,
	project_note	text,
	project_type	integer		NOT NULL, -- personal or team, only one of user_id or team_id will be used
	project_public	boolean		NOT NULL, -- public project or private project
	user_id		integer		REFERENCES users(user_id) ON DELETE CASCADE,
	team_id		integer		REFERENCES team(team_id) ON DELETE CASCADE,
	admin_id	integer		NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
	created_at	timestamp	NOT NULL
);
