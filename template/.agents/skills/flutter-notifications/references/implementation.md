# Notification Service Skeleton

Versions to pin in the app's `pubspec.yaml` are the ones the project already uses; check the lock file before changing them.

## Lifecycle Handlers

```dart
// Foreground: FCM does not show a system notification, so show a local one.
FirebaseMessaging.onMessage.listen(showLocalNotification);

// Background: the user tapped a notification while the app was in the background.
FirebaseMessaging.onMessageOpenedApp.listen(openFromMessage);

// Terminated: the app was launched by a tap.
final initial = await FirebaseMessaging.instance.getInitialMessage();
if (initial != null) {
  WidgetsBinding.instance.addPostFrameCallback((_) => openFromMessage(initial));
}
```

## Service Skeleton

```dart
class NotificationService {
  NotificationService(this._fcm, this._local);

  final FirebaseMessaging _fcm;
  final FlutterLocalNotificationsPlugin _local;

  Future<void> start({required void Function(String route) onOpenRoute}) async {
    await _local.initialize(
      const InitializationSettings(
        android: AndroidInitializationSettings('@mipmap/ic_launcher'),
        iOS: DarwinInitializationSettings(),
      ),
      onDidReceiveNotificationResponse: (response) =>
          onOpenRoute(decodeRoute(response.payload)),
    );
    for (final channel in allNotificationChannels) {
      await _local
          .resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>()
          ?.createNotificationChannel(channel.channel);
    }
    FirebaseMessaging.onMessage.listen(showLocalNotification);
    FirebaseMessaging.onMessageOpenedApp.listen((m) => onOpenRoute(decodeRoute(m.data)));
  }
}
```

The channels, the payload codec and the web path live in the project's notification package. Copy their names from there, not from this skeleton.
