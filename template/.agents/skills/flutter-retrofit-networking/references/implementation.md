# Dio Implementation Examples

## Remote Datasource

```dart
class OrderRemoteDataSource {
  OrderRemoteDataSource(this._dio);

  final Dio _dio;

  Future<OrderDto> getOrder(String id) async {
    final response = await _dio.get<Map<String, dynamic>>('/orders/$id');
    return OrderDto.fromJson(response.data!);
  }

  Future<void> cancelOrder(String id) async {
    await _dio.post<void>('/orders/$id/cancel');
  }
}
```

## Tolerant Enum DTO (json_serializable)

```dart
@JsonSerializable()
class OrderDto {
  const OrderDto({required this.id, required this.status});

  factory OrderDto.fromJson(Map<String, dynamic> json) => _$OrderDtoFromJson(json);

  final String id;

  @JsonKey(unknownEnumValue: OrderStatus.unknown)
  final OrderStatus status;

  Map<String, dynamic> toJson() => _$OrderDtoToJson(this);
}

enum OrderStatus { open, closed, unknown }
```

## Error Mapping in the Repository

```dart
Future<Order> fetchOrder(String id) async {
  try {
    final dto = await _remote.getOrder(id);
    return dto.toDomain();
  } on DioException catch (e) {
    throw switch (e.response?.statusCode) {
      401 => const UnauthorizedFailure(),
      final code? when code >= 500 => ServerFailure(code),
      _ => const NetworkFailure(),
    };
  }
}
```
