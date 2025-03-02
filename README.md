# MISIS Elephants - Fuel Exchange - BestHack


Tasks completed
-
✅ Главная страница с лотами (front + back)\
✅ Подробная информация о каждом лоте (front + back)\
✅ Регистрация (front + back)\
✅ Авторизация (Пользователь/Администратор) (JWT, front + back)\
✅ ЛК Администратора - создание лотов\
✅ Измениние статуса товара при истечении срока (front + back) \
✅ Добавление слотов в csv формате (ftp + interface) (front + back) \
Для добавления товара надо перейти по ссылке http://109.73.207.86/AddLot \
✅ Заказ лота (front + back) \
➕ Валидация приходящих лотов \
-Фильтрация слотов (front + back) \

Stack
-
 - Backend: 
    - Python - FastAPI
    - DataBase - PostgreSQL
 - Frontend:
    - HTML/CSS/JS
    - React
 - Docker / Docker Compose
 - nginx

 Collaborators:
- 
backend/teamlead - @cvbnqq \
backend - @dontpaniczy \
frontend - @ignat3333 \
design - @aantaars

## Инструкция по развертыванию локально
1. Клонировать гит репо
```
git clone https://github.com/dontpanicw/besthack
```
2. Зайти в корневую папку
```
cd ./besthack
```
3. Из корневой папки
```
docker-compose up --build -d
```
