#! /bin/bash

echo "Creating init_db.sql..."
cd ../schema
cat users.sql team.sql teammates.sql project.sql board.sql epic.sql sprint.sql story.sql > ../test/db-setup/init_db.sql
cd ../test
echo "Building docker image..."
docker-compose build
echo "Running integration tests..."
docker-compose up
echo "To end all docker containers, please run:"
echo "docker-compose down"
