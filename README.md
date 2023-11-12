<p align="center">
  <img src="https://cursin.net/wp-content/uploads/2023/07/e3923daf.webp" alt="screenshot">
</p>


# Backend API

Этот проект представляет собой реализацию API на языке Python с использованием PostgreSQL в качестве базы данных.

## Оглавление


- [Настройка и запуск](#настройка-и-запуск)
- [Примеры использования](#примеры-использования)
- [Тесты](#тесты)
- [Лицензия](#лицензия)

## Настройка и запуск
1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/zayac880/e-commerce_MVP.git

2. Установите зависимости командой: 

    ```bash
    poetry install`

3. Настройте файл .env.sample и создайте базу данных

    ```bash
    CREATE DATABASE name_db;

4. Сделайте миграции


    aerich init-db
    aerich migrate
    aerich upgrade

5. запустите программу

    ```bash
    uvicorn app.main:app --reload 


## Примеры использования
* http://localhost:8000/docs
* http://localhost:8000/redoc

 **Для всех пользователей:**

* POST
http://localhost:8000/docs#/users/register
Register


* POST
http://localhost:8000/docs#/users/login
Authenticate

 **Только для авторизованных пользователей:**

* POST
http://localhost:8000/docs#/products/create
Create Product

* GET
http://localhost:8000/docs#/products
Get list Products 

* GET
http://localhost:8000/docs#/products/{product_id}
Get Product id

* PUT
http://localhost:8000/docs#/products/{product_id}
Update Product

 * DELETE
http://localhost:8000/docs#/products/{product_id}
Delete Product id

## Тесты

Для запуска тестов выполните следующие шаги:

1. Запустите тесты:

    ```bash
    coverage run -m pytest
   
2. Проверьте покрытие тестами:

    ```bash
   coverage report

## Лицензия

* (c) 2023 @zayac880 - [github](#https://github.com/zayac880)