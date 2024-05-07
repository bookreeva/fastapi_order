import time

from main import redis, Product

key = 'order_completed'
group = 'inventory-group'

# Создает группу потребителей для ключа, если она еще не существует.
try:
    redis.xgroup_create(key, group)
except Exception as e:
    print(f'Группа уже существует: {str(e)}.')

while True:
    try:
        # Читает события из потока Redis и обрабатывает заказы.
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                # Обрабатывает данные заказа и обновляет количество продукта.
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except Exception as e:
                    print(str(e))
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
