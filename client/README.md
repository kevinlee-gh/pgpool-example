1. init pgbench
```bash
$ PGPASSWORD=postgres123 pgbench -i -h node-1 -U postgres benchmark_db
```
2. Run pgbench
```bash
$ PGPASSWORD=postgres123 pgbench -h node-1 -U postgres benchmark_db -c 10 -T 600
```