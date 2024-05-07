import time

from main import redis, Order

key = 'refund_order'
group = 'payment-group'


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
                # Обрабатывает данные заказа и обновляет
                # статус заказа на 'refunded'.
                obj = result[1][0][1]
                order_pk = obj['pk']
                order = Order.get(order_pk)
                order.status = 'refunded'
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)
