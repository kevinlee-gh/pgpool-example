FROM postgres:17.4-bookworm

COPY --chown=postgres:postgres ./configs /configs

RUN mkdir -p /var/lib/postgresql/data && chown -R postgres:postgres /var/lib/postgresql/data

USER postgres

COPY ./entrypoint.sh /ha-entrypoint.sh

ENTRYPOINT [ "/ha-entrypoint.sh" ]
CMD [ "postgres" ]