FROM postgres:latest
ENV POSTGRES_USER service
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB postgres

ENV PORT=5432

COPY ./db-setup/init_db.sql		/docker-entrypoint-initdb.d/
