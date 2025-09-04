1. init pgbench
```bash
$ PGPASSWORD=postgres123 pgbench -i -h postgres-proxy -p 5433 -U postgres benchmark_db
```
2. Run pgbench
```bash
$ PGPASSWORD=postgres123 pgbench -h postgres-proxy -p 5433 -U postgres benchmark_db -c 10 -T 600
```