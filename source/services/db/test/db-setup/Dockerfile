FROM postgres:latest
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB docker

ENV PORT=5432

COPY init_db.sql		/docker-entrypoint-initdb.d/
