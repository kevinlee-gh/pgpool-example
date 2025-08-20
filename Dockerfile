FROM postgres:17.4-bookworm

RUN mkdir -p /var/lib/postgresql/data/pgdata
RUN chown -R postgres:postgres /var/lib/postgresql/data/pgdata