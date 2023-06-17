FROM postgres:15.3
ENV POSTGRES_PASSWORD=CHANGE_IT
ENV POSTGRES_USER=admin
ENV POSTGRES_DB=tracker
COPY init_db.sql /docker-entrypoint-initdb.d/init_db.sql