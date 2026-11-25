---
name: flutter-notifications
description: Deliver and show push and local notifications in Flutter with Firebase Messaging and flutter_local_notifications: channels, foreground and background handling, tap payloads with routes, permission requests, and web notifications. Use when changing how a notification is received, shown or opened.
metadata:
  triggers:
    files:
      - '**/*notification*.dart'
      - '**/main.dart'
    keywords:
      - FirebaseMessaging
      - FlutterLocalNotificationsPlugin
      - AndroidNotificationChannel
      - onMessageOpenedApp
      - getInitialMessage
      - push
---

# Flutter Notifications

## **Priority: P1 (HIGH)**

## Implementation Workflow

1. **One service owns the wiring.** A single notification service sets up the local plugin, the channels, the FCM listeners and the permission request. Features call it; they do not listen to FCM themselves.
2. **Channels are named and explicit.** Each kind of notification has its own channel with its own importance. Create all channels once, at startup.
3. **Handle the three app states.** Foreground (`onMessage`: show a local notification), background (`onMessageOpenedApp`: navigate) and terminated (`getInitialMessage`: navigate after the first frame).
4. **Payloads carry a route.** Encode the payload as a string that includes the target route and the identifiers the screen needs. Decode it in one function and validate it before navigating.
5. **Permission is requested in context.** Explain the benefit in the app first, then call the system request. Do not request it at cold start without context.
6. **Web is a separate path.** On web, use the browser Notification API behind a conditional import. Do not call native plugins on web.
7. **Badges.** Clear the iOS badge when the user opens the relevant screen, not on every launch.

## Anti-Patterns

- **No FCM listeners in features**: they run twice and navigate twice.
- **No channel created per notification**.
- **No navigation from a payload without validation**.
- **No permission request on the first frame**.
- **No native plugin calls on web**.

## Reference & Examples

See [references/implementation.md](references/implementation.md) for the lifecycle handlers and the service skeleton.

## Related Topics

- Navigation target: `flutter-go-router-navigation`.
- Payload and personal data in logs: `flutter-security`.
