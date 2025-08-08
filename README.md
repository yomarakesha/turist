# Туристический API

## Установка и запуск

1. **Установить зависимости:**
```bash
pip install -r requirements.txt
```

2. **Создать базу данных:**
```bash
flask db upgrade
```

3. **Создать админа:**
```bash
python create_admin.py
```

4. **Запустить сервер:**
```bash
python run.py
```

## API Endpoints

Все endpoints возвращают данные на двух языках (русский и английский):

- `GET /api/cities` - список городов
- `GET /api/hotels` - список отелей  
- `GET /api/excursions` - список экскурсий
- `GET /api/attractions` - список достопримечательностей
- `GET /api/banners` - список баннеров

## Структура ответов

```json
{
  "id": 1,
  "name_ru": "Москва",
  "name_en": "Moscow",
  "description_ru": "Столица России",
  "description_en": "Capital of Russia"
}
```

## Админка

- URL: `http://localhost:5000/admin`
- Логин: `admin`
- Пароль: `admin` 

## Поиск по названиям (search)

Теперь для следующих эндпоинтов можно использовать параметр `search` для поиска по name_ru и name_en (регистр не важен):

- `/api/cities?search=Москва`
- `/api/hotels?search=Hilton`
- `/api/excursions?search=Обзорная`
- `/api/attractions?search=музей`

Можно комбинировать с другими параметрами:
- `/api/hotels?city_id=1&search=Hilton`
- `/api/excursions?city_id=2&type=bus&search=Обзорная`

**Пример запроса для Postman:**
```
GET http://localhost:5000/api/hotels?search=Hilton
```

**Результат:**
```json
[
  {
    "id": 1,
    "name_ru": "Хилтон Москва",
    "name_en": "Hilton Moscow",
    ...
  }
]
``` 