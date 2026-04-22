# Software Design Document (SDD)

> **Версія:** v1.1 | **Дата:** 2026-04-23  
> **Статус:** Затверджено  
> **Джерело істини для:** внутрішньої архітектури, компонентів, API-інтерфейсів

---

## 1. Загальна архітектура

Система побудована за архітектурним стилем **мікросервісів**. Внутрішня архітектура самого сервісу базується на багатошаровому підході (Layered Architecture): Presentation Layer (Controllers), Business Logic Layer (Services), Data Access Layer (Repositories).

## 2. Перелік компонентів та їх взаємодія

* **Auth Controller:** Відповідає за прийом HTTP REST запитів, первинну валідацію вхідних даних (формат email, довжина пароля) та повернення HTTP відповідей.
* **Auth Service:** Містить основну бізнес-логіку (перевірка чи існує користувач, виклик сервісу хешування, прийняття рішень).
* **JWT Manager:** Утиліта для криптографічного створення та розшифровки JWT токенів.
* **User Repository:** Компонент, що абстрагує роботу з базою даних (виконання SQL-запитів).

**Схема взаємодії:** Клієнт -> `Auth Controller` -> `Auth Service` -> `User Repository` -> Database. Після успішної перевірки `Auth Service` звертається до `JWT Manager` для генерації токена і повертає його через контролер клієнту.

## 3. Короткий опис API інтерфейсів

* `POST /api/v1/auth/register` — приймає JSON з email та password, повертає `201 Created`.
* `POST /api/v1/auth/login` — приймає JSON з email та password, повертає `200 OK` та об'єкт з токенами `{"accessToken": "...", "refreshToken": "..."}`.
* `POST /api/v1/auth/refresh` — приймає `refreshToken`, повертає новий `accessToken`.

*Пов'язані документи: [SSD](SSD.md) | [ISD](ISD.md)
