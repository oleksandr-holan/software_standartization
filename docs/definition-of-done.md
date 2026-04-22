# Definition of Done — Документація

> **Версія:** v1.0 | **Дата:** 2026-04-22  
> **Застосовується до:** будь-якого Pull Request у репозиторій Auth Microservice

PR вважається готовим до merge лише якщо всі застосовні критерії нижче виконані.

---

## 1. Матриця DoD за типом змін

| Тип зміни | Обов'язкові дії | Автоматична перевірка | Ручна перевірка |
| :--- | :--- | :--- | :--- |
| **Додано новий API-ендпоінт** | Додати шлях до `openapi.yaml` з усіма відповідями та схемами | `openapi-generator-cli validate` | Code review OpenAPI |
| **Змінено request/response формат** | Оновити схему в `openapi.yaml` + оновити приклади | OpenAPI validation | Перевірка Swagger UI |
| **Видалено або перейменовано ендпоінт** | Оновити `openapi.yaml` + позначити deprecated, оновити SDD | OpenAPI validation | Code review + версійність |
| **Breaking change в API** | Нова major-версія в `info.version` + git-тег `docs/v2.0.0` | Version tag у CI | Оповіщення споживачів |
| **Додано UI-компонент** | Створити `.stories.ts` файл з мін. 2 stories (Default + альтернативний стан) | `npm run build-storybook` | Перегляд у Storybook |
| **Змінено поведінку UI-компонента** | Оновити відповідну story або додати нову | Storybook build | Code review stories |
| **Зміна нефункціональних вимог (NFR)** | Оновити `architecture/SSD.md` + `quality/test-strategy.md` | MkDocs build | Code review документа |
| **Зміна архітектури** | Оновити `architecture/SDD.md` | MkDocs build | Code review архітектурного рішення |
| **Зміна інфраструктури** | Оновити `architecture/ISD.md` | MkDocs build | DevOps review |
| **Новий тест-кейс** | Додати рядок до `quality/traceability-matrix.md` | MkDocs build | QA review |

---

## 2. Перевірювані критерії готовності

### 2.1 API-зміни

- [ ] `docs/api/openapi.yaml` містить всі нові/змінені ендпоінти
- [ ] Кожен шлях має `summary`, `description`, `requestBody` (якщо потрібен) та всі можливі `responses`
- [ ] Нові схеми додані до `components/schemas`
- [ ] `openapi-generator-cli validate` завершується без помилок
- [ ] Swagger UI відображає зміни коректно (перевіряється локально)

### 2.2 UI-зміни

- [ ] Кожен новий компонент має файл `*.stories.ts`
- [ ] Мінімум 2 stories: `Default` та хоча б один альтернативний стан (`Loading` / `Error` / `Disabled`)
- [ ] `npm run build-storybook` завершується без помилок

### 2.3 Документація (завжди)

- [ ] `mkdocs build --strict` завершується без помилок
- [ ] Markdownlint не показує нових помилок (`markdownlint-cli2 "docs/**/*.md"`)
- [ ] Всі внутрішні посилання між документами працюють

### 2.4 Breaking changes

- [ ] Версія в `openapi.yaml` → `info.version` оновлена (major або minor)
- [ ] Git-тег `docs/vX.Y.Z` створено
- [ ] Споживачів API оповіщено (через CHANGELOG або Release Notes)

---

## 3 Автоматичні перевірки в CI

Перераховані перевірки блокують мердж якщо не пройшли:

```text
PR Checks:
  ✅ validate / Lint Markdown
  ✅ validate / Validate OpenAPI spec
  ✅ build / Build MkDocs site (--strict)
  ✅ build / Build Storybook
```

---

*Пов'язані документи: [CI/CD Pipeline](ci-cd-docs.md) | [OpenAPI](api/openapi.yaml) | [Test Strategy](quality/test-strategy.md)*
