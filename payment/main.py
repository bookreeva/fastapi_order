import time
import os
from dotenv import load_dotenv

import requests
from starlette.requests import Request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from redis_om import get_redis_connection, HashModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('CORS_ORIGINS')],
    allow_methods=[os.getenv('CORS_METHODS')],
    allow_headers=[os.getenv('CORS_HEADERS')]
)

redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)


class Order(HashModel):
    """ Модель заказа. """
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending(в ожидании), completed(успешно), refunded(ошибка)

    def __str__(self):
        return f"{self.pk, self.quantity}"

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str) -> Order:
    """
    Получает заказ.
    :param pk: pk заказа.
    """
    return Order.get(pk)


@app.get('/orders/all')
def all_orders():
    """ Возвращает список заказов. """
    return Order.all_pks()


@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):
    """
    Создает новый заказ на основе данных из запроса.

    :param request: Объект запроса с данными заказа (id, quantity).
    :param background_tasks: Объект для добавления фоновых задач.
    """
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order) -> None:
    """
    Обрабатывает завершенный заказ.
    Обновляет статус заказа.
    Отправляет событие order_completed в Resid с данными заказа.

    :param order: Объект заказа, для которого необходимо
    выполнить обработку.
    :return:
    """
    time.sleep(5)
    order.status = 'completed'
    order.save()

    redis.xadd('order_completed', order.dict(), '*')
