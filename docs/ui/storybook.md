# UI-документація — Storybook

> **Аудиторія:** Frontend-розробники, дизайнери, QA  
> **Інструмент:** [Storybook](https://storybook.js.org/) 8.x

---

## 1. Призначення

Хоча Auth Microservice є суто backend-сервісом (REST API без UI), клієнтські застосунки, що споживають цей API, містять UI-компоненти для автентифікації. Storybook документує ці компоненти як інтерактивну бібліотеку, незалежно від backend.

Обрані компоненти для документування:

1. **LoginForm** — форма входу (використовує `POST /auth/login`)
2. **AuthButton** — кнопка з підтримкою станів завантаження/помилки

---

## 2. Запуск Storybook

```bash
# Встановлення
npx storybook@latest init

# Запуск dev-сервера
npm run storybook
# → http://localhost:6006

# Збірка статичного сайту
npm run build-storybook
# → ./storybook-static/
```

---

## 3. Компонент: LoginForm

### Опис

Форма для авторизації користувача. Відправляє `POST /api/v1/auth/login`, обробляє стани завантаження та помилки.

### Stories

| Story | Тригер | API-відповідь |
| :--- | :--- | :--- |
| `Default` | Компонент щойно відрендерений | — |
| `Loading` | Форму відправлено, запит в процесі | — |
| `WithError` | Сервер повернув помилку | `401 Unauthorized` |
| `RateLimited` | Забагато спроб входу | `429 Too Many Requests` |

---

## 4. Компонент: AuthButton

### Опис компонента

Кнопка для форм автентифікації з підтримкою станів завантаження та відключення.

### Stories AuthButton

| Story | Стан | Умова відображення |
| :--- | :--- | :--- |
| `Default` | Активна | Форма заповнена коректно |
| `Loading` | Завантаження (спінер) | Запит відправлено |
| `Disabled` | Неактивна | Поля форми порожні або невалідні |
| `Secondary` | Вторинна дія | Реєстрація, скидання паролю |

---

## 5. Структура файлів Storybook

```text
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── LoginForm.stories.ts   ← Storybook story
│   │   ├── AuthButton.tsx
│   │   └── AuthButton.stories.ts  ← Storybook story
└── .storybook/
    ├── main.ts                    ← конфігурація
    └── preview.ts                 ← глобальні декоратори
```

---

*Пов'язані документи: [CI/CD](../ci-cd-docs.md) | [Definition of Done](../definition-of-done.md)*
