#! /bin/bash

echo "Creating init_db.sql..."
cd ../schema
cat users.sql team.sql teammates.sql project.sql board.sql epic.sql sprint.sql story.sql > ../test/init_db.sql
cd ../test
echo "Building docker image..."
docker build -t test-postgres .
echo "Cleaning up test environment..."
rm -rf ./docker
echo "Making data directory..."
mkdir -p docker/volumes/postgres
echo "Running docker container..."
docker run --rm --name test-postgres -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $PWD/docker/volumes/postgres:/var/lib/postgresql/data test-postgres
echo "Verifying running containers..."
docker ps
echo "Please run following command to connect to container:"
echo "docker exec -it [container ID] bash"
