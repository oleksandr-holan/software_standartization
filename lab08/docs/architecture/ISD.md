# Infrastructure Specification Document (ISD)

> **Версія:** v1.0 | **Дата:** 2026-04-22  
> **Статус:** Затверджено  
> **Джерело істини для:** середовища розгортання, CI/CD, масштабування

---

## 1. Середовище розгортання

Мікросервіс розгортається у **хмарному середовищі** (AWS або Google Cloud) з використанням контейнеризації **Docker** та оркестрації **Kubernetes**.

| Параметр | Значення |
| :--- | :--- |
| Хмарний провайдер | AWS (EKS) або GCP (GKE) |
| Контейнеризація | Docker 24+ |
| Оркестратор | Kubernetes 1.28+ |
| Реєстр образів | Docker Hub / AWS ECR |
| Протокол | HTTPS (TLS 1.3) |

---

## 2. Інфраструктурні компоненти

### API Gateway

- **Роль:** єдина точка входу для всіх зовнішніх запитів.
- **Функції:** маршрутизація до мікросервісу автентифікації, термінація SSL-сертифікатів, базовий rate limiting на мережевому рівні.

### App Containers (Auth Service)

- **Мінімальна кількість реплік:** 2 (для High Availability).
- **Максимальна кількість реплік:** 10 (Auto-scaling).
- **Ресурси контейнера:**
  - CPU Request: 250m / Limit: 500m
  - Memory Request: 256Mi / Limit: 512Mi

### PostgreSQL (Relational DB)

- **Призначення:** надійне зберігання облікових даних користувачів.
- **Топологія:** Primary (запис) + 2 Read Replicas (читання).
- **Backup:** щоденний snapshot + WAL-архівування.

### Redis (In-memory Cache)

- **Призначення:**
  - Blacklist відкликаних JWT-токенів.
  - Rate Limiting (лічильники невдалих спроб входу по IP).
- **Топологія:** Redis Sentinel (1 master + 2 replicas) для HA.
- **TTL ключів:** відповідає терміну дії accessToken.

---

## 3. Схема інфраструктури

```
Internet
    │
    ▼
┌─────────────────┐
│   API Gateway   │  (SSL Termination, Routing)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│         Kubernetes Cluster      │
│  ┌──────────┐  ┌──────────┐    │
│  │ Auth Pod │  │ Auth Pod │    │  (2–10 replicas, HPA)
│  └──────────┘  └──────────┘    │
└────────┬───────────────┬────────┘
         │               │
         ▼               ▼
   ┌──────────┐    ┌──────────┐
   │PostgreSQL│    │  Redis   │
   │ Primary  │    │ Sentinel │
   └──────────┘    └──────────┘
```

---

## 4. Принципи масштабування

### Горизонтальне масштабування (HPA)

Kubernetes Horizontal Pod Autoscaler автоматично збільшує кількість реплік якщо:

- Середнє навантаження на CPU перевищує **70%**.
- Кількість вхідних запитів різко зростає (custom metric).

### Масштабування БД

PostgreSQL масштабується за принципом **Primary-Replica**:

- Один сервер для операцій запису.
- Кілька Read Replicas для операцій читання (балансування через pgBouncer).

---

## 5. CI/CD пайплайн

```
Developer → Git Push → Pull Request
                            │
                            ▼
                    ┌───────────────┐
                    │  CI Pipeline  │
                    │  • Unit Tests │
                    │  • API Tests  │
                    │  • Lint/SAST  │
                    └───────┬───────┘
                            │ merge to main
                            ▼
                    ┌───────────────┐
                    │  CD Pipeline  │
                    │  • Build Image│
                    │  • Push to ECR│
                    │  • Deploy K8s │
                    └───────────────┘
```

**Стадії пайплайну:**

| Стадія | Інструмент | Тригер |
| :--- | :--- | :--- |
| Lint & Static Analysis | ESLint / Bandit | кожен PR |
| Unit Tests | Jest / Pytest | кожен PR |
| API Integration Tests | Postman/Newman | кожен PR |
| Build Docker Image | Docker Build | merge до `main` |
| Push to Registry | ECR / Docker Hub | merge до `main` |
| Deploy to Kubernetes | kubectl / Helm | merge до `main` |
| Performance Tests | JMeter | щотижня / перед релізом |

---

## 6. Вимоги до середовища (Environment Variables)

| Змінна | Опис | Приклад |
| :--- | :--- | :--- |
| `DATABASE_URL` | Рядок підключення до PostgreSQL | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Рядок підключення до Redis | `redis://host:6379` |
| `JWT_SECRET` | Секретний ключ для підпису токенів | (генерується автоматично) |
| `JWT_ACCESS_TTL` | Термін дії accessToken (секунди) | `900` (15 хв) |
| `JWT_REFRESH_TTL` | Термін дії refreshToken (секунди) | `604800` (7 днів) |
| `RATE_LIMIT_MAX` | Макс. невдалих спроб входу | `5` |
| `RATE_LIMIT_WINDOW` | Вікно блокування (секунди) | `600` (10 хв) |

---

*Пов'язані документи: [SSD](SSD.md) | [SDD](SDD.md)
