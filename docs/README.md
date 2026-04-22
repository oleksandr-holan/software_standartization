# Auth Microservice — Documentation

> **Версія документації:** v1.1  
> **Дата:** 2026-04-23  
> **Single Source of Truth:** цей репозиторій є єдиним джерелом актуальної документації проєкту.

Мікросервіс автентифікації користувачів (REST API) — незалежний компонент для реєстрації, перевірки облікових даних та генерації JWT-токенів.

---

## Навігація

### Архітектура та вимоги

- [System Specification Document (SSD)](architecture/SSD.md) — функціональні та нефункціональні вимоги, межі системи
- [Software Design Document (SDD)](architecture/SDD.md) — архітектура, компоненти, API-інтерфейси
- [Infrastructure Specification Document (ISD)](architecture/ISD.md) — середовище розгортання, CI/CD, масштабування

### Якість

- [Test Strategy](quality/test-strategy.md) — стратегія тестування, рівні та підходи
- [Traceability Matrix](quality/traceability-matrix.md) — матриця зв'язку вимог та тест-кейсів

---

## Single Source of Truth

| Область | Джерело істини | Залежні документи |
| :--- | :--- | :--- |
| Функціональні вимоги | `architecture/SSD.md` | SDD, Test Strategy, Traceability Matrix |
| Архітектура | `architecture/SDD.md` | ISD, Onboarding |
| Інфраструктура | `architecture/ISD.md` | Onboarding |
| Тестові кейси | `quality/traceability-matrix.md` | Test Strategy |

**Правила оновлення:**

1. Будь-яка зміна вимог починається з оновлення `SSD.md` та отримує новий ідентифікатор (FR-XX / NFR-XX).
2. Зміна архітектури відображається в `SDD.md`.
3. Нові або змінені вимоги потребують оновлення `traceability-matrix.md` з новими TC-ID.
4. Версія документації зростає відповідно до [моделі версійності](#версійність).

---

## Версійність

| Версія | Дата | Опис змін |
| :--- | :--- | :--- |
| v1.0 | 2026-04-22 | Початковий реліз документації (ЛР-7 → DaC) |
| v1.1 | 2026-04-23 | ЛР-9: OpenAPI 3.2.0, Swagger UI, Storybook, CI/CD pipeline, Definition of Done |

**Модель версійності:** документація слідує [Semantic Versioning](https://semver.org/):

- **MAJOR** (v2.0) — кардинальна зміна API або архітектури (breaking change).
- **MINOR** (v1.1) — нова функціональність без порушення сумісності.
- **PATCH** (v1.0.1) — виправлення помилок, уточнення формулювань.

Версія документації синхронізується з версією сервісу. Тег у Git-репозиторії (`docs/v1.0`) фіксує знімок документації для кожного релізу.
