# Token Refresh with One Retry

## Interceptor

```dart
class AuthInterceptor extends QueuedInterceptorsWrapper {
  AuthInterceptor({required this.dio, required this.readToken, required this.refreshToken});

  final Dio dio;
  final Future<String?> Function() readToken;
  final Future<String?> Function() refreshToken;

  static const _retriedKey = '_retriedAfterRefresh';

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    final token = await readToken();
    if (token != null) options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    final alreadyRetried = err.requestOptions.extra[_retriedKey] == true;
    if (err.response?.statusCode != 401 || alreadyRetried) {
      return handler.next(err);
    }
    final newToken = await refreshToken();
    if (newToken == null) return handler.next(err);

    final retry = err.requestOptions
      ..headers['Authorization'] = 'Bearer $newToken'
      ..extra[_retriedKey] = true;
    try {
      handler.resolve(await dio.fetch<dynamic>(retry));
    } on DioException catch (e) {
      handler.next(e);
    }
  }
}
```

## Why these choices

- `QueuedInterceptorsWrapper` holds the other requests while one refresh runs. Without it, several 401s start several refreshes, and the later ones can invalidate the earlier tokens.
- The flag in `extra` limits the repeat to one attempt. A second 401 returns to the caller as an error.
- If the refresh itself fails, the original 401 is returned. The caller then decides to sign the user out.
