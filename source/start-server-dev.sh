#! /bin/bash

echo "Creating init_db.sql..."
cd db/schema
cat users.sql team.sql teammates.sql project.sql board.sql epic.sql sprint.sql story.sql > ../test/db-setup/init_db.sql
cd ../..
echo "Building docker image..."
docker-compose build
echo "Bring up services..."
docker-compose up
echo "After services are down..."
docker-compose down
