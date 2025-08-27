FROM postgres:17.4-bookworm

COPY --chown=postgres:postgres ./configs /configs

RUN mkdir -p /var/lib/postgresql/data && chown -R postgres:postgres /var/lib/postgresql/data

USER postgres

ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "postgres" ]