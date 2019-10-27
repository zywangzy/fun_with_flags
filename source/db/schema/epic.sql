CREATE TABLE epic (
	epic_id		SERIAL		PRIMARY KEY,
	epic_name	varchar (128)	NOT NULL,
	epic_note	text,
	project_id	integer		REFERENCES project(project_id) ON DELETE CASCADE
);

