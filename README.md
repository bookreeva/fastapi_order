<a id="toup"></a>
<h1>FastApi Order</h1>
<h2>Добро пожаловать!</h2>
~~В процессе.~~
<h3>Перед началом использования программы создайте файл .env и 
заполните его данными из файла .env.sample:</h3>


| Шаблон .env.sample |
|--------------------|

```text 
CORS_ORIGINS=
CORS_METHODS=
CORS_HEADERS=

REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
 ```

<h4>✔️ Создайте виртуальное окружение и активируйте его</h3>
<h4>✔️ Установите зависимости из файла requirements.txt из микросервисов</h3>

<h4>✔️ Для запуска серверов: </h4>

| Описание                   | Команды                                     |
|----------------------------|---------------------------------------------|
| Запустить inventory сервер | ```uvicorn main:app --reload```             |
| Запустить payment сервер   | ```uvicorn main:app --reload --port=8001``` |
| Запустить react            | ```npm start```                             |


 <div style="display: flex; align-items: center;">
    <div style="display: inline-block; margin: 2px;" >


</div>
  </div>

<h2>Ошибки и улучшения</h2>
Если вы обнаружили ошибки, у вас есть предложения по улучшению данного проекта 
или у вас есть вопросы по использованию API, пожалуйста, присылайте pull request.

[Вверх](#toup)

```commandline

```
