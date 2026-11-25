---
name: multi-tenant-isolation
description: Keep tenant data isolated in a multi-tenant backend: tenant resolution per request, global versus tenant-owned data, cross-boundary references, role scope on tenant change, and per-tenant migrations. Use when adding a tenant-owned entity, a query, a migration, or an endpoint that changes tenant.
metadata:
  triggers:
    files:
      - '**/*Tenant*.cs'
      - '**/Interceptors/**'
      - '**/Migrations/**'
    keywords:
      - tenant
      - schema
      - tenant_id
      - isolation
---

# Multi-Tenant Isolation

## **Priority: P0 (CRITICAL)**

## Rules

1. **Resolve the tenant once, per request, from the authenticated identity.** Do not read the tenant from the request body or from a client-chosen header in business code.
2. **Choose one isolation boundary and state it.** Schema per tenant, database per tenant or a discriminator column are valid options. Document the choice in an architecture decision record before writing the first entity.
3. **Global data is separate from tenant data.** Keep identity and catalog data that every tenant shares in a global area, with no direct navigation from tenant data into it.
4. **Cross-boundary links are checked in code** when the database cannot enforce them. Test both sides of each link.
5. **Every tenant-owned query goes through the tenant boundary.** A missing boundary is a data leak, not only a functional bug. Cover it with an isolation test: a second tenant cannot read or write the row.
6. **Changing tenant resets authority.** Roles and permissions belong to one tenant. A tenant change redefines the roles and revokes every active session before a new one is issued.
7. **Migrations run for every tenant boundary.** A new tenant-owned table is created in each boundary by the migration runner, never by hand.

## Checklist for a new tenant-owned entity

- [ ] Mapped in the tenant context, not in the global context.
- [ ] No database foreign key to global data, or the link is checked in code.
- [ ] Query path goes through the tenant boundary.
- [ ] Isolation test: a second tenant cannot read or write it.
- [ ] Migration applied to every boundary and tested with existing rows.

## Anti-Patterns

- Filtering by tenant in a service instead of at the boundary.
- Keeping an old role after a tenant change.
- Global queries over tenant tables.
