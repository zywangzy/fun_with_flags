CREATE TABLE sprint (
	sprint_id	SERIAL		PRIMARY KEY,
	sprint_num	integer		NOT NULL,
	sprint_name	varchar (128)	NOT NULL,
	project_id	integer		REFERENCES project(project_id) ON DELETE CASCADE,
	status		integer		NOT NULL,
	created_at	timestamp	NOT NULL,
	closed_at	timestamp,
	begin_time	timestamp,
	end_time	timestamp
);

