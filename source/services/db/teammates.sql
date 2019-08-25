CREATE TABLE teammates (
	user_id		INTEGER		REFERENCES users(user_id),
	team_id		INTEGER		REFERENCES team(team_id),
	PRIMARY KEY (user_id, team_id)
);
