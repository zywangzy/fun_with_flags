#! /bin/bash

echo "Creating init_db.sql..."
cd ../db/schema
cat users.sql team.sql teammates.sql project.sql board.sql epic.sql sprint.sql story.sql > ../test/db-setup/init_db.sql
cd ../../integration_tests
echo "Building docker image..."
docker-compose build
echo "Running integration tests..."
docker-compose up
echo "After tests are complete"
docker-compose down
