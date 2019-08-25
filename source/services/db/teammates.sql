CREATE TABLE teammates (
	user_id		integer		REFERENCES users(user_id),
	team_id		integer		REFERENCES team(team_id),
	PRIMARY KEY (user_id, team_id)
);
