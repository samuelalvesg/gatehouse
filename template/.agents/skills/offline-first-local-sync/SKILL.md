---
name: offline-first-local-sync
description: Build offline-first data in a client app: a local database mirror per device, optimistic local writes, background sync, a default last-writer-wins conflict policy, and a user filter in every local query. Use when adding a synced collection, a sync service, or a local query.
metadata:
  triggers:
    files:
      - '**/*sync*.dart'
      - '**/*local*.dart'
    keywords:
      - offline
      - optimistic
      - sync
      - conflict
      - userId
---

# Offline-First Local Sync

## **Priority: P0 (CRITICAL)**

## Rules

1. **The local database mirrors each synced collection.** Reads come from the local copy. The server is the source of truth for conflicts.
2. **Writes are optimistic.** Save locally at once and sync in the background. The UI never waits for the network to show the user's own change.
3. **Sync runs in the background.** Triggers (polling, push notifications, reconnection) start it; debounce bursts. Sync logic lives in services, not in widgets.
4. **Conflict policy defaults to last-writer-wins.** Use a merge policy such as CRDT only for a row that several users edit at the same time, and only after an explicit decision.
5. **The local database is per device, not per account.** Filter every local query by the current user or tenant. Without the filter, data of one account is visible after switching accounts on the same device.
6. **Show sync state.** Loading, empty, error and offline states must be visible; never hide a change that has not synced yet.

## Checklist for a new synced collection

- [ ] Local table with a user or tenant column.
- [ ] Every repository query filters by that column.
- [ ] Optimistic write, with rollback when the server rejects it.
- [ ] Conflict policy written down.
- [ ] Test: data of one account is not visible after switching to another on the same device.

## Anti-Patterns

- An unfiltered local query.
- Waiting for the network before the local write.
- Merge policies by default.
- Sync logic inside widgets.
