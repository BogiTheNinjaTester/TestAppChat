FROM postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB postgres
ADD CreateDB.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
