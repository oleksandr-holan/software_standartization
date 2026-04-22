# Software Design Document (SDD)

> **Версія:** v1.0 | **Дата:** 2026-04-22  
> **Статус:** Затверджено  
> **Джерело істини для:** внутрішньої архітектури, компонентів, API-інтерфейсів

---

## 1. Загальна архітектура

Система побудована за архітектурним стилем **мікросервісів**. Внутрішня архітектура сервісу — **Layered Architecture** (багатошарова):

```
┌─────────────────────────────────┐
│     Presentation Layer          │  ← Auth Controller (HTTP/REST)
├─────────────────────────────────┤
│     Business Logic Layer        │  ← Auth Service, JWT Manager
├─────────────────────────────────┤
│     Data Access Layer           │  ← User Repository
├─────────────────────────────────┤
│     Infrastructure              │  ← PostgreSQL, Redis
└─────────────────────────────────┘
```

---

## 2. Компоненти системи

### Auth Controller

- **Відповідальність:** прийом HTTP-запитів, первинна валідація вхідних даних (формат email, довжина пароля), повернення HTTP-відповідей.
- **Взаємодіє з:** Auth Service.

### Auth Service

- **Відповідальність:** основна бізнес-логіка — перевірка існування користувача, виклик хешування, прийняття рішень щодо автентифікації.
- **Взаємодіє з:** User Repository, JWT Manager.

### JWT Manager

- **Відповідальність:** криптографічне створення та верифікація JWT-токенів (Access + Refresh). Перевірка підпису, терміну дії, наявності в blacklist.
- **Взаємодіє з:** Redis (blacklist відкликаних токенів).

### User Repository

- **Відповідальність:** абстракція роботи з базою даних (виконання SQL-запитів: пошук, вставка облікових записів).
- **Взаємодіє з:** PostgreSQL.

---

## 3. Схема взаємодії компонентів

```
Client
  │
  ▼
Auth Controller  ──(validate input)──►  Auth Service
                                            │
                              ┌─────────────┼─────────────┐
                              ▼             ▼             ▼
                        User Repository  JWT Manager   Redis
                              │                         (blacklist)
                              ▼
                          PostgreSQL
```

**Сценарій логіну:**

1. `Client` → `POST /api/v1/auth/login` → `Auth Controller`
2. `Auth Controller` валідує формат → передає в `Auth Service`
3. `Auth Service` → `User Repository` → знаходить юзера в PostgreSQL
4. `Auth Service` перевіряє bcrypt-хеш пароля
5. `Auth Service` → `JWT Manager` → генерує `accessToken` + `refreshToken`
6. `Auth Controller` повертає `200 OK` з токенами клієнту

---

## 4. API-інтерфейси

### POST /api/v1/auth/register

**Опис:** Реєстрація нового користувача (FR-01).

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Responses:**

| Код | Опис |
| :--- | :--- |
| `201 Created` | Користувача успішно створено |
| `409 Conflict` | Email вже зареєстровано |
| `422 Unprocessable Entity` | Невалідний формат email або пароль |

---

### POST /api/v1/auth/login

**Опис:** Авторизація користувача, отримання токенів (FR-02).

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

**Responses:**

| Код | Опис |
| :--- | :--- |
| `200 OK` | Успішна авторизація, повернення токенів |
| `401 Unauthorized` | Невірний email або пароль |
| `429 Too Many Requests` | IP заблоковано після 5 невдалих спроб |

---

### POST /api/v1/auth/refresh

**Опис:** Оновлення accessToken за допомогою refreshToken (FR-03).

**Request body:**

```json
{
  "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

**Response (200 OK):**

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Responses:**

| Код | Опис |
| :--- | :--- |
| `200 OK` | Новий accessToken видано |
| `401 Unauthorized` | Токен прострочений, відкликаний або невалідний |

---

## 5. Технологічний стек

| Шар | Технологія |
| :--- | :--- |
| Runtime | Node.js / Python / Go (на вибір команди) |
| Фреймворк | Express / FastAPI / Gin |
| База даних | PostgreSQL |
| Кеш / Blacklist | Redis |
| Автентифікація | JWT (RS256) |
| Хешування | bcrypt (cost factor 12) |
| Контейнеризація | Docker |

---

*Пов'язані документи: [SSD](SSD.md) | [ISD](ISD.md)
