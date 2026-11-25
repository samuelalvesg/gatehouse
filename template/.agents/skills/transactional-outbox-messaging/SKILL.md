---
name: transactional-outbox-messaging
description: Publish and consume events and real-time messages safely: transactional outbox for critical messages, a separate high-volume channel for messages that can be lost, and a single real-time hub per client session. Use when adding a publisher, a subscriber, a topic, or a real-time hub method.
metadata:
  triggers:
    files:
      - '**/Hubs/**'
      - '**/*Subscriber*.cs'
      - '**/*Publisher*.cs'
      - '**/Messaging/**'
    keywords:
      - outbox
      - publish
      - subscribe
      - SignalR
      - idempotent
---

# Transactional Outbox and Real-Time Messaging

## **Priority: P0 (CRITICAL)**

## Choose the channel

| Message | Channel | Reason |
|---|---|---|
| Billing, audit, workflow state | Transactional outbox | The event and the business write must commit together. |
| High volume, loss acceptable (telemetry, outbound webhooks) | Event bus without outbox | Cost per message matters more than exactly-once delivery. |
| Real-time UI update | One real-time hub per client session | One connection carries all live updates for that session. |

## Rules

1. **Commit the event with the business write.** Publish inside the same transaction, never in a separate step after the commit.
2. **The transport can change per environment; the outbox storage does not.** Keep the outbox in the same database as the business data.
3. **One hub per client session.** Add methods to the existing hub; open a new hub only when load or failure isolation justifies it.
4. **Keep the documented signature of streaming hub methods.** Extra parameters can silently break the client call.
5. **A topic with several subscribers is one contract.** A change to its schema or publisher needs a test that covers every subscriber.
6. **Subscribers are idempotent.** The same message can arrive twice; running the handler again must be safe.

## Checklist for a new message

- [ ] Channel chosen from the table.
- [ ] Publish inside the transaction (outbox path).
- [ ] Subscriber is idempotent and tested.
- [ ] Every subscriber of the topic is covered by a test.
- [ ] Hub method signature documented.

## Anti-Patterns

- Publishing after the commit on the outbox path.
- A new hub for every small feature.
- A subscriber that assumes exactly-once delivery.
