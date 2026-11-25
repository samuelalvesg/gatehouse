# Mobile Security Implementation Examples

## Secure Storage

```dart
const storage = FlutterSecureStorage();

await storage.write(key: 'auth_token', value: token);
final token = await storage.read(key: 'auth_token');
await storage.delete(key: 'auth_token');
```

## Build-Time Configuration

```dart
const apiBaseUrl = String.fromEnvironment('API_URL');
```

```bash
flutter build appbundle \
  --obfuscate \
  --split-debug-info=build/debug-info \
  --dart-define=API_URL=$API_URL
```

## Masking in Logs

```dart
log('Login for user ${maskId(userId)}');
```
