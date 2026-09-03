# Task Manager — Учебный проект

## Установка и запуск бэкенда

1. Открыть терминал в папке `backend/` (команда cd backend)

2. Создать виртуальное окружение:
  python -m venv venv

3. Активировать venv:
  Windows (Git Bash): source venv/Scripts/activate

Windows (CMD): venv\Scripts\activate

4. Установить зависимости:
  pip install -r requirements.txt

5. Инициализировать Alembic:
  bash
  alembic init alembic
  Затем заменить alembic/env.py на настроенный (см. урок).

6. Создать и применить миграции:
  bash
  alembic revision --autogenerate -m "create tasks table"
  alembic upgrade head

7. Запустить сервер:
  bash
  uvicorn app.main:app --reload
  Сервер доступен на http://localhost:8000

## Установка и запуск фронтенда

1. Открыть терминал в папке `frontend/`
  cd frontend

2. Установить зависимости:
  bash
  npm install

3. Запустить:
  bash
  npm run dev
  Фронтенд доступен на http://localhost:5173



email 
password 
JWT - токен (JSON Web Token) header.payload.signature 
eyaksodpsajpAPSD.AdpsojdpAJSS.
{
  alg: "HS256",
  typ": "JWT"
}
{
  "sub": "admin@mail.ru"
}

SHA256(base64(header) + "." + base64(payload), SECRET_KEY)




1. Браузер GET /tasks
2. Сервер Ответ + заголовок Set-Cookie:{session_id=abc123}
3. Браузер сохраняет Cookie 
4. Браузе: GET/tasks + заголовок Cookie: session_id=abc123
5. Сервер: сравнивает значение куки 

Cookie (в браузере):            Сессии(на сервере):
| session_id = abc123 | -->   | user_id: 5              |
                              | email: example@mail.com |
                              | ...                     |



## Docker ключевые понятия

### Образ (image) 
Это шаблон приложения 
содержит: библиотеки, настройки и код
неизменяемый - *как класс* 

### Контейнер (Container) 
Это запущенный *экземпляр образа*
Один образ -> много контейнеров 

### Dockerfile 
Текстовый файл с инструкциями, как собирать образ 



### CI/CD

CI - непрерывная интеграция
CD - непрерывная доставка
