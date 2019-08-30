# Test instruction

Just run command `./run_test.sh`, output would be:
```bash
➜  test ✗ ./run_test.sh
Creating init_db.sql...
Building docker image...
Sending build context to Docker daemon  6.656kB
Step 1/6 : FROM postgres:latest
 ---> f97a959a7d9c
Step 2/6 : ENV POSTGRES_USER docker
 ---> Using cache
 ---> d0faf4a44fb6
Step 3/6 : ENV POSTGRES_PASSWORD docker
 ---> Using cache
 ---> f328df978d66
Step 4/6 : ENV POSTGRES_DB docker
 ---> Using cache
 ---> c16154d7bc12
Step 5/6 : ENV PORT=5432
 ---> Using cache
 ---> fa0bca1476a1
Step 6/6 : COPY init_db.sql		/docker-entrypoint-initdb.d/
 ---> Using cache
 ---> 3df9a5b56c3d
Successfully built 3df9a5b56c3d
Successfully tagged test-postgres:latest
Cleaning up test environment...
Making data directory...
Running docker container...
98c7c88a2068e098b075e5db70e8afc61b8d237205ae291efc1eac0963d0ed1b
Verifying running containers...
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                  PORTS                    NAMES
98c7c88a2068        test-postgres       "docker-entrypoint.s…"   1 second ago        Up Less than a second   0.0.0.0:5432->5432/tcp   test-postgres
Please run following command to connect to container:
docker exec -it [container ID] bash
➜  test ✗ docker exec -it 98c bash
root@98c7c88a2068:/# psql -U docker
psql (11.2 (Debian 11.2-1.pgdg90+1))
Type "help" for help.

docker=# \c
You are now connected to database "docker" as user "docker".
docker=# \d
                 List of relations
 Schema |         Name         |   Type   | Owner
--------+----------------------+----------+--------
 public | board                | table    | docker
 public | board_board_id_seq   | sequence | docker
 public | epic                 | table    | docker
 public | epic_epic_id_seq     | sequence | docker
 public | sprint               | table    | docker
 public | sprint_sprint_id_seq | sequence | docker
 public | story                | table    | docker
 public | story_story_id_seq   | sequence | docker
 public | team                 | table    | docker
 public | team_team_id_seq     | sequence | docker
 public | teammates            | table    | docker
 public | users                | table    | docker
 public | users_user_id_seq    | sequence | docker
(13 rows)

docker=# exit
root@98c7c88a2068:/# exit
exit
➜  test ✗ docker stop 98c
98c
```
