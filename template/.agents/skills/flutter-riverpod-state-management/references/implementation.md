# Riverpod Implementation Examples

## Notifier with AsyncValue

```dart
class ProductsNotifier extends AsyncNotifier<List<Product>> {
  @override
  Future<List<Product>> build() {
    return ref.watch(productRepositoryProvider).getProducts();
  }

  Future<void> addProduct(Product product) async {
    await ref.read(productRepositoryProvider).create(product);
    ref.invalidateSelf();
  }
}

final productsProvider = AsyncNotifierProvider<ProductsNotifier, List<Product>>(
  ProductsNotifier.new,
);

final productRepositoryProvider = Provider<ProductRepository>((ref) {
  return ProductRepository(ref.watch(apiClientProvider));
});
```

## Consumer Widget with Side Effects

```dart
class ProductsScreen extends ConsumerWidget {
  const ProductsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen<AsyncValue<List<Product>>>(productsProvider, (previous, next) {
      if (next.hasError) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Não foi possível carregar os produtos.')),
        );
      }
    });

    return ref.watch(productsProvider).when(
          data: (products) => ListView.builder(
            itemCount: products.length,
            itemBuilder: (_, i) => ProductTile(products[i]),
          ),
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, stack) => const Center(child: Text('Erro ao carregar.')),
        );
  }
}
```

## Test with an Override

```dart
final container = ProviderContainer(
  overrides: [
    productRepositoryProvider.overrideWithValue(FakeProductRepository()),
  ],
);
addTearDown(container.dispose);
```
