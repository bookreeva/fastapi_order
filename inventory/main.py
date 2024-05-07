import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis_om import HashModel, get_redis_connection

app = FastAPI()

load_dotenv()

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


class Product(HashModel):
    """ Модель товара. """
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


def format_product(pk: str) -> dict[str, str | None | int | float]:
    """ Возвращает словарь с данными товара. """
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }


@app.get('/products')
def all_products() -> list[dict]:
    """ Возвращает список товаров. """
    return [format_product(pk) for pk in Product.all_pks()]


@app.post('/products')
def create(product: Product) -> Product:
    """ Создает товар. """
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    """ Получает товар. """
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str) -> int:
    """ Удаляет товар. """
    return Product.delete(pk)
