#! /bin/bash

echo "Creating database setup directory"
cd db
mkdir -p test/db-setup
echo "Creating init_db.sql..."
cd schema
cat users.sql team.sql teammates.sql project.sql board.sql epic.sql sprint.sql story.sql > ../test/db-setup/init_db.sql
cd ../../integration_tests
echo "Building docker image..."
docker-compose build
echo "Bring up services..."
docker-compose up
echo "After services are down..."
docker-compose down
