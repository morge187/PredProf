# АИС Школьного Питания
## Полная техническая документация

---

## 0. Преимущества используемых технологий

### Почему Python

- Простота и читаемость кода, низкий порог входа и высокая скорость разработки веб‑приложений.  
- Большая экосистема библиотек для веб‑разработки, аналитики, интеграций и автоматизации.  
- Кроссплатформенность и зрелое сообщество, обеспечивающее долгосрочную поддержку и развитие языка.  

### Преимущества Flask

- Лёгкий, модульный и минималистичный фреймворк, позволяющий подключать только нужные компоненты (ORM, формы, авторизация и т.д.).  
- Быстрый старт и простая архитектура: удобно строить небольшие сервисы, прототипы и постепенно масштабировать до сложных систем.  
- Хорошая интеграция с SQLAlchemy и удобная работа с REST API, шаблонами и аутентификацией. 

### Преимущества PostgreSQL

- Надёжная промышленная СУБД с полной поддержкой транзакций ACID и расширенными возможностями обеспечения целостности данных.  
- Поддержка продвинутых SQL‑функций, сложных запросов, индексов и оптимизации, что важно для отчётности и аналитики.  
- Расширяемость: пользовательские типы данных, функции и хорошие возможности работы с JSON/JSONB и полуструктурированными данными.

---

## 1. Введение

**АИС Школьного Питания** — автоматизированная информационная система, разработанная для управления питанием учащихся в школьной столовой. Система обеспечивает:

- Регистрацию и авторизацию пользователей с разделением ролей (ученик, повар, администратор)
- Просмотр меню завтраков и обедов
- Оплату питания (разово или абонементом)
- Учёт выданных блюд и остатков продуктов
- Управление заявками на закупку продуктов
- Формирование отчётов по оплатам и посещаемости
- Оставление отзывов и указание пищевых аллергий

Решение реализовано на **Flask** с использованием **SQLAlchemy** для работы с БД, **Flask-Login** для управления сессиями и **WTForms** для валидации форм.

---

## 2. Архитектура системы

### 2.1 Общее описание

Система построена на классической трёхуровневой архитектуре:
- **Уровень представления (UI)**: HTML/CSS/JavaScript шаблоны (Jinja2)
- **Уровень приложения (Business Logic)**: Flask routes и обработчики
- **Уровень данных (Data)**: SQLAlchemy ORM с поддержкой SQLite/PostgreSQL

### 2.2 Компоненты

#### **Аутентификация и авторизация**
- `routes/auth.py` — регистрация, вход, выход
- `models/user.py` — модель User с ролями (STUDENT, COOK, ADMIN)
- `utils/decorators.py` — декоратор `@role_required()` для проверки прав

#### **Студенческий кабинет**
- `routes/student.py` — просмотр меню, оплата, отметка получения, отзывы
- `models/menu.py` — меню на дату и блюда
- `models/order.py` — платежи и заказы питания

#### **Кабинет повара**
- `routes/cook.py` — учёт выданных блюд, управление остатками, заявки на закупку
- `models/inventory.py` — остатки продуктов и готовых блюд
- `models/procurement.py` — заявки на закупку

#### **Административный кабинет**
- `routes/admin.py` — статистика, согласование заявок, отчёты
- Формирование CSV-отчётов по платежам и посещаемости

---

## 3. Схема базы данных

![Database Schema][1]

### Таблицы и связи

| Таблица | Назначение | Ключевые поля |
|---------|-----------|---------------|
| **users** | Учётные записи пользователей | id (PK), username (UNIQUE), email (UNIQUE), role |
| **menu_days** | Дни, на которые задано меню | id (PK), day (UNIQUE) |
| **menu_items** | Блюда в меню | id (PK), menu_day_id (FK), meal_type, name, price_rub |
| **payments** | Платежи учеников | id (PK), student_id (FK), amount_rub, status |
| **meal_orders** | Заказы питания (отметка получения) | id (PK), student_id (FK), day, meal_type, received_by_student_at |
| **product_stocks** | Остатки сырья | id (PK), name (UNIQUE), quantity, unit |
| **dish_stocks** | Остатки готовых блюд | id (PK), dish_name (UNIQUE), portions_available |
| **procurement_requests** | Заявки на закупку | id (PK), created_by_cook_id (FK), status (pending/approved/rejected) |
| **procurement_items** | Строки заявки (какие товары) | id (PK), request_id (FK), product_name, quantity |
| **dish_feedback** | Отзывы на блюда | id (PK), student_id (FK), dish_name, rating (1-5), comment |

### Ограничения целостности
- `users.username` и `users.email` — UNIQUE
- `menu_days.day` — UNIQUE
- `meal_orders(student_id, day, meal_type)` — UNIQUE (один прием пищи в день)
- Все FK используют ON DELETE CASCADE для чистки данных

---

## 4. Диаграмма классов

![UML Class Diagram][2]

### Основные классы

#### **User** (модель пользователя)
```
Атрибуты: id, username, email, password_hash, role, allergies, preferences
Методы: is_admin(), is_cook(), is_student()
Связи: One-to-Many с Payments, MealOrders, ProcurementRequests, DishFeedback
```

#### **MenuItem** (блюдо в меню)
```
Атрибуты: id, name, price_rub, allergens, meal_type (breakfast/lunch)
Связи: Many-to-One с MenuDay
```

#### **Payment** (платёж)
```
Атрибуты: id, amount_rub, payment_type (single/subscription), status
Связи: Many-to-One с User, One-to-Many с MealOrder
```

#### **MealOrder** (заказ питания)
```
Атрибуты: id, day, meal_type, paid, received_by_student_at, issued_by_cook_at
Связи: Many-to-One с User и Payment
```

#### **ProcurementRequest** (заявка на закупку)
```
Атрибуты: id, status (pending/approved/rejected), comment, created_at, decided_at
Связи: Many-to-One с User (повар), One-to-Many с ProcurementItem
```

#### **DishFeedback** (отзыв)
```
Атрибуты: id, dish_name, rating (1-5), comment
Связи: Many-to-One с User
```

---

## 5. Блок-схема основного алгоритма

![Flowchart Algorithm][3]

### Описание потока

1. **Старт приложения** → User открывает сайт
2. **Проверка аутентификации**
   - Если не авторизован → Регистрация/Вход → Установка роли
   - Если авторизован → Переход к шагу 3

3. **Ветвление по роли пользователя**:

   **Путь ученика:**
   - Просмотр меню на дату
   - Оплата питания (разово или абонемент)
   - Отметка получения завтрака/обеда
   - Оставление отзыва на блюдо
   - Указание аллергий и предпочтений

   **Путь повара:**
   - Учёт выданных завтраков и обедов
   - Обновление остатков продуктов и готовых блюд
   - Создание заявки на закупку товаров
   - Просмотр списка собственных заявок

   **Путь администратора:**
   - Просмотр статистики (сумма оплат, посещаемость)
   - Согласование/отклонение заявок на закупку
   - Формирование CSV-отчётов по датам

4. **Конец** → Выход из системы

---

## 6. Структура проекта

```
project/
├── app.py                      # Фабрика приложения Flask
├── main.py                     # Точка входа
├── settings.py                 # Конфигурация приложения
├── database.py                 # Инициализация SQLAlchemy
├── requirements.txt            # Зависимости Python
├── .env                        # Переменные окружения
├── Dockerfile                  # Образ Docker
├── docker-compose.yml          # Конфигурация контейнеров
│
├── models/                     # ORM модели SQLAlchemy
│   ├── __init__.py
│   ├── user.py                 # User с ролями
│   ├── menu.py                 # MenuDay, MenuItem
│   ├── order.py                # Payment, MealOrder
│   ├── inventory.py            # ProductStock, DishStock
│   ├── procurement.py          # ProcurementRequest, ProcurementItem
│   ├── feedback.py             # DishFeedback
│   └── reports.py              # Модели отчётов (опционально)
│
├── routes/                     # Flask blueprints (маршруты)
│   ├── __init__.py
│   ├── auth.py                 # POST /auth/login, /auth/register
│   ├── student.py              # GET /student/dashboard, /student/menu и т.д.
│   ├── cook.py                 # GET /cook/dashboard, /cook/issue
│   └── admin.py                # GET /admin/dashboard, /admin/stats
│
├── utils/                      # Утилиты
│   ├── __init__.py
│   ├── security.py             # hash_password, verify_password
│   ├── decorators.py           # @role_required()
│   └── helpers.py              # Вспомогательные функции
│
├── wtf_forms/                  # WTForms для валидации
│   ├── __init__.py
│   ├── auth_forms.py           # LoginForm, RegisterForm
│   ├── student_forms.py        # PayForm, FeedbackForm и т.д.
│   ├── cook_forms.py           # IssueMealForm, StockForm
│   └── admin_forms.py          # DecideProcurementForm, ReportForm
│
├── templates/                  # Jinja2 шаблоны HTML
│   ├── base.html               # Базовый макет
│   ├── index.html              # Главная страница
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── student/
│   │   ├── dashboard.html
│   │   ├── menu.html
│   │   ├── pay.html
│   │   ├── preferences.html
│   │   ├── feedback.html
│   │   └── my_orders.html
│   ├── cook/
│   │   ├── dashboard.html
│   │   ├── issue_meal.html
│   │   ├── inventory.html
│   │   ├── procurement_new.html
│   │   └── procurements.html
│   └── admin/
│       ├── dashboard.html
│       ├── stats.html
│       ├── procurements.html
│       └── report.html
│
└── static/                     # Статические файлы
    ├── css/
    │   └── styles.css          # Стили приложения
    ├── js/
    │   └── app.js              # JavaScript логика
    └── images/                 # Изображения
```

---

## 7. Интеграция и развёртывание

### 7.1 Локальная разработка

```bash
# 1. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать .env файл
echo "SECRET_KEY=dev-key" > .env
echo "DATABASE_URL=sqlite:///canteen.db" >> .env

# 4. Запустить приложение
python main.py
```

Приложение будет доступно на `http://localhost:5000`

### 7.2 Docker и Docker Compose

```bash
# Собрать и запустить контейнеры
docker-compose build
docker-compose up

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 7.3 Переменные окружения

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|---------|
| `SECRET_KEY` | dev-secret-key-change-me | Секрет для Flask сессий |
| `DATABASE_URL` | sqlite:///canteen.db | Строка подключения к БД |
| `FLASK_APP` | app:create_app | Фабрика приложения Flask |
| `FLASK_ENV` | development | Окружение (development/production) |

---

## 8. Функциональные требования

### 8.1 Роль: Ученик

| Функция | Статус | Описание |
|---------|--------|---------|
| Регистрация/Авторизация | ✅ Готово | Создание аккаунта и вход |
| Просмотр меню | ✅ Готово | Меню завтраков и обедов на дату |
| Оплата питания | ✅ Готово | Разовый платеж или абонемент |
| Отметка получения | ✅ Готово | Отметить получение завтрака/обеда |
| Указание аллергий | ✅ Готово | Сохранение пищевых предпочтений |
| Оставление отзывов | ✅ Готово | Оценка блюд и комментарии |

### 8.2 Роль: Повар

| Функция | Статус | Описание |
|---------|--------|---------|
| Авторизация | ✅ Готово | Вход в систему |
| Учёт выданных блюд | ✅ Готово | Регистрация выданных завтраков/обедов |
| Управление остатками | ✅ Готово | Обновление количества продуктов/блюд |
| Заявки на закупку | ✅ Готово | Создание и просмотр заявок |

### 8.3 Роль: Администратор

| Функция | Статус | Описание |
|---------|--------|---------|
| Авторизация | ✅ Готово | Вход в систему |
| Статистика | ✅ Готово | Просмотр оплат и посещаемости |
| Согласование заявок | ✅ Готово | Одобрение/отклонение закупок |
| Отчёты | ✅ Готово | Экспорт в CSV по датам |

---

## 9. Технические особенности

### 9.1 Безопасность

- **Хеширование паролей**: использование `werkzeug.security` (PBKDF2)
- **CSRF защита**: `Flask-WTF` автоматически генерирует и проверяет CSRF токены
- **Управление сессиями**: `Flask-Login` с временем жизни 14 дней
- **Валидация формы**: все входные данные валидируются через WTForms

### 9.2 Производительность

- **Кеширование**: могут быть добавлены Redis для сессий в production
- **Индексы БД**: на полях `username`, `email`, `day` в таблице `menu_days`
- **Пагинация**: может быть добавлена для списков заявок и отзывов

### 9.3 Масштабируемость

- **БД**: поддержка PostgreSQL для production-среды
- **WSGI сервер**: рекомендуется Gunicorn вместо встроенного Flask сервера
- **Reverse proxy**: рекомендуется Nginx для фронтенда

---

## 10. Примеры использования

### 10.1 Регистрация ученика

```
1. Открыть http://localhost:5000/auth/register
2. Заполнить форму: логин, email, пароль, роль = "student"
3. Нажать "Создать аккаунт"
4. Перенаправление на /auth/login
5. Вход с учётными данными
```

### 10.2 Просмотр меню и оплата

```
1. Авторизоваться как ученик
2. Перейти в /student/dashboard
3. Клик на "Меню" → выбрать дату
4. Просмотр завтраков и обедов с ценами
5. Клик на "Оплата" → выбрать сумму и тип платежа
6. Подтверждение (в демо-режиме платёж успешен)
7. Клик на "Отметка получения" для завтрака/обеда
```

### 10.3 Управление остатками (повар)

```
1. Авторизоваться как повар
2. Перейти в /cook/inventory
3. Заполнить форму: тип (продукт/блюдо), название, количество, ед.
4. Нажать "Сохранить"
5. Остаток обновлён в таблице
```

### 10.4 Согласование заявки (администратор)

```
1. Авторизоваться как администратор
2. Перейти в /admin/procurements
3. Просмотреть список заявок
4. Заполнить форму: ID заявки, решение (одобрить/отклонить), комментарий
5. Нажать "Применить"
6. Статус заявки изменён
```

---

## 11. Возможные ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `RuntimeError: SQLALCHEMY_DATABASE_URI must be set` | `DATABASE_URL` не установлена | Установить в `.env` или Dockerfile |
| `ERR_EMPTY_RESPONSE` при доступе на 127.0.0.1 | Flask слушает только localhost внутри контейнера | Заменить на `app.run(host="0.0.0.0", port=5000)` |
| `ModuleNotFoundError: No module named 'flask'` | Зависимости не установлены | Выполнить `pip install -r requirements.txt` |
| Сессия теряется после перезагрузки | `SECRET_KEY` не установлен или случайный | Установить постоянный `SECRET_KEY` в `.env` |

---

## 12. Дополнительные ресурсы

- **Flask документация**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Flask-SQLAlchemy**: [https://flask-sqlalchemy.palletsprojects.com/](https://flask-sqlalchemy.palletsprojects.com/)
- **WTForms**: [https://wtforms.readthedocs.io/](https://wtforms.readthedocs.io/)
- **Docker для Python**: [https://docs.docker.com/language/python/](https://docs.docker.com/language/python/)
- **OWASP Top 10**: [https://owasp.org/Top10/](https://owasp.org/Top10/)

---

## 13. Контакты и поддержка

Для вопросов и предложений:
- Email: [support@schoolcanteen.ru](mailto:support@schoolcanteen.ru)
- GitHub Issues: [https://github.com/your-org/school-canteen/issues](https://github.com/your-org/school-canteen/issues)
- Документация: [https://docs.schoolcanteen.ru](https://docs.schoolcanteen.ru)

---

**Версия документации**: 1.0  
**Последнее обновление**: 06.02.2026  
**Автор**: Командный кейс № 2 "Управление столовой" (Московская предпрофессиональная олимпиада)

добавь в начало приимущества питона и Flask.
также плюсы Postgresql
