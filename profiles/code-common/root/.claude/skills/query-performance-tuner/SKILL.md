---
name: query-performance-tuner
description: Analyzes execution plans (EXPLAIN ANALYZE), indexing and N+1 in Postgres/EF Core. Use for slow queries, index migrations, or listings that fire many queries.
---
# Golden rule
Measure → change **one** thing → measure. Only on a local/Testcontainers database with realistic volume (never production).

# Steps
1. **Capture the query**: log `Microsoft.EntityFrameworkCore.Database.Command` at `Information` (or `ToQueryString()`) in a test.
2. **Plan**: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <query>;` Writes: `BEGIN; EXPLAIN (ANALYZE, BUFFERS) ...; ROLLBACK;`
3. **Read the plan** (most expensive node upward):
   | Signal | Likely cause | Action |
   |---|---|---|
   | `Seq Scan` on a big table with a selective filter | missing index | index the predicate column(s) |
   | estimated `rows` ≪ actual | stale statistics | `ANALYZE <table>` |
   | `Sort` with `external merge` | `work_mem` / no sort index | index in `ORDER BY` order |
   | `Nested Loop` × thousands | N+1 or unindexed join | `Include`/projection/FK index |
   | high `Buffers: read` | cold I/O or too much data | project only used columns, paginate |
4. **Index**: column order = equality first, then range/order; partial (`WHERE NOT is_deleted`) with soft delete; cover FKs used in joins; tenant first on shared tables. Every index costs writes: justify with a number.
5. **N+1 (EF Core)**: symptom = N identical queries in a loop. Fix with `Include`/`ThenInclude`, `Select` projection to a DTO, or a batch query (`Where(x => ids.Contains(x.Id))`). Read-only: `AsNoTracking()`. Many collection `Include`s: `AsSplitQuery()`.
6. **Pagination**: keyset (`WHERE (k) > @last ORDER BY k LIMIT n`) on large tables; high `OFFSET` is slow.
7. **Test**: assert the command count (query counter) and that the plan uses the index, in a database-backed test.
8. **Index migration**: `CREATE INDEX CONCURRENTLY` on large tables (outside a transaction); run the migration checker; regenerate EF compiled models if used.

# Output checklist
- [ ] Before/after: `Execution Time`, `Buffers`, query count
- [ ] New index justified and owned (which query)
- [ ] No write regression (insert N rows measured)
- [ ] Performance regression test (query count)
- [ ] Explicit "not measured" where data was missing

# Output (≤15 lines)
`QUERY | problem | change | before → after | risk`.
