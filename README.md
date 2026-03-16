# KinoCMS 🎬

**KinoCMS** — це система управління контентом для мережі кінотеатрів, розроблена за допомогою Python та фреймворку Django. Проект надає зручні інструменти для адміністрування фільмів, кінотеатрів, залів та розкладу сеансів, а також клієнтську частину для взаємодії з користувачами.

## 🌟 Основний функціонал

* **Управління фільмами:** Додавання нових фільмів, редагування інформації (постери, описи, трейлери, акторський склад).
* **Мережа кінотеатрів:** Створення та налаштування кінотеатрів, управління інформацією про них (галерея, контакти, умови).
* **Управління залами:** Створення залів для кожного кінотеатру, налаштування кількості місць, схеми залу та їх характеристик.
* **Розклад сеансів:** Формування сітки сеансів із прив'язкою до конкретних фільмів, залів та часу.
* **Багатомовність:** Налаштовано підтримку локалізації (папка `locale`).

## 🛠 Стек технологій

* **Backend:** Python 3, Django
* **Frontend:** HTML5, CSS3
* **База даних:** PostgreSQL / SQLite (в залежності від конфігурації)
* **Контейнеризація:** Docker, Docker Compose

## 📁 Структура проекту

* `config/` — головні налаштування Django-проекту.
* `src/` — основні додатки та бізнес-логіка (models, views, forms).
* `templates/` — HTML-шаблони сторінок.
* `deploy/` — файли для розгортання проекту.
* `locale/` — файли перекладів.

## 🚀 Встановлення та запуск

Проект налаштований для швидкого запуску за допомогою Docker.

### Попередні вимоги
Переконайся, що на твоєму комп'ютері встановлені:
* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Кроки для локального розгортання

1. **Клонуй репозиторій:**
   ```bash
   git clone [https://github.com/maksirh/kinoCMS.git](https://github.com/maksirh/kinoCMS.git)
   cd kinoCMS
   ```

2. **Запусти проект через Docker Compose (режим розробки):**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d --build
   ```

3. **Застосуй міграції бази даних:**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

4. **Створи суперкористувача (адміністратора):**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

5. **Збери статичні файли (за потреби):**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input
   ```

Відкрий браузер і перейди за адресою `http://127.0.0.1:8000/`. Панель адміністратора буде доступна за адресою `http://127.0.0.1:8000/admin/`.

## ⚙️ Запуск у Production

Для запуску проекту на бойовому сервері використовуй спеціальний файл конфігурації `docker-compose.prod.yml`:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🤝 Контриб'юція

Якщо ви хочете внести свій вклад у розвиток проекту:
1. Зробіть Fork репозиторію.
2. Створіть нову гілку для вашої фічі (`git checkout -b feature/AmazingFeature`).
3. Зробіть коміт змін (`git commit -m 'Add some AmazingFeature'`).
4. Відправте зміни в гілку (`git push origin feature/AmazingFeature`).
5. Створіть Pull Request.
