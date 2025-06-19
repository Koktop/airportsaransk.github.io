# Аэропорт Саранск - Веб-сайт

Веб-сайт для аэропорта Саранск, разработанный на Python с использованием Flask.

## Функциональность

- Просмотр расписания рейсов
- Информация об аэропорте
- Контактная информация
- Форма обратной связи

## Требования

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- другие зависимости из requirements.txt

## Установка

1. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
cd [название-папки]
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

1. Инициализируйте базу данных:
```bash
flask db init
flask db migrate
flask db upgrade
```

2. Запустите приложение:
```bash
python app.py
```

3. Откройте браузер и перейдите по адресу:
```
http://localhost:5000
```

## Структура проекта

```
├── app.py              # Основной файл приложения
├── requirements.txt    # Зависимости проекта
├── static/            # Статические файлы (CSS, JS, изображения)
│   └── css/
│       └── style.css
└── templates/         # HTML шаблоны
    ├── base.html
    ├── index.html
    ├── about.html
    ├── schedule.html
    └── contact.html
```

## Разработка

Для внесения изменений в проект:

1. Создайте новую ветку:
```bash
git checkout -b feature/название-функции
```

2. Внесите изменения и зафиксируйте их:
```bash
git add .
git commit -m "Описание изменений"
```

3. Отправьте изменения в репозиторий:
```bash
git push origin feature/название-функции
```

## Лицензия

MIT 