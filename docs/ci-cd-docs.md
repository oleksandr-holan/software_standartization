# Documentation CI/CD Pipeline

> **Версія:** v1.0 | **Дата:** 2026-04-22  
> **Платформа:** GitHub Actions + GitHub Pages

---

## 1. Артефакти документації

| Артефакт | Інструмент | Джерело |
| :--- | :--- | :--- |
| API-документація (Swagger UI) | swagger-ui-dist | `docs/api/openapi.yaml` |
| UI-документація (Storybook) | Storybook 8.x | `src/components/**/*.stories.ts` |
| Загальний сайт документації | MkDocs Material | `docs/**/*.md` |

---

## 2. Тригери генерації

| Тригер | Дія |
| :--- | :--- |
| `push` у будь-яку `feature/*` гілку | Валідація та збірка (preview, не публікація) |
| `pull_request` до `main` | Валідація + збірка + звіт у PR |
| `merge` до `main` | Повна збірка + публікація на GitHub Pages |
| Git-тег `v*.*.*` | Збірка версійованої документації |

---

## 3. Послідовність кроків пайплайну

### Triggers

- **Push / Pull Request**: Запускає стадії валідації та збірки (Stage 1 & 2).
- **Merge into `main`**: Єдиний тригер для фінальної стадії публікації (Stage 3).

### Stages

#### 1. Stage 1: Validate (Валідація)

- **Lint Markdown**: Перевірка синтаксису документації за допомогою `markdownlint`.

- **Validate OpenAPI schema**: Перевірка відповідності специфікації стандарту за допомогою `openapi-generator-cli validate`.
- **Type-check Storybook**: Перевірка TypeScript-типів у файлах сторіз для уникнення помилок у документації UI.

#### 2. Stage 2: Build (Збірка артефактів)

- **MkDocs Build**: Збірка основного сайту документації з Markdown-файлів у директорію `./site/`.

- **Swagger UI**: Генерація інтерактивного інтерфейсу для API у підпапку `./site/api-docs/`.
- **Storybook Build**: Компіляція візуальної документації компонентів у підпапку `./site/ui/`.

#### 3. Stage 3: Publish (Публікація) — **Тільки для гілки `main`**

- **Умова**: Виконується лише за умови успішного проходження попередніх стадій та злиття (merge) коду в основну гілку `main`.

- **Deploy**: Автоматичне розгортання всього вмісту директорії `./site/` на **GitHub Pages**.

---

## 4. Структура URL на GitHub Pages

```text
https://<org>.github.io/<repo>/
├── /                    ← MkDocs — загальний сайт документації
├── /api-docs/           ← Swagger UI (інтерактивна API-документація)
│   └── openapi.yaml     ← вихідна специфікація
└── /ui/                 ← Storybook (UI-компоненти)
```

**Приклад для репозиторію `github.com/example/auth-service`:**

| URL | Зміст |
| :--- | :--- |
| `example.github.io/auth-service/` | Головна сторінка документації (MkDocs) |
| `example.github.io/auth-service/api-docs/` | Swagger UI |
| `example.github.io/auth-service/ui/` | Storybook |

---

## 5. Політика версійності документації

**Відповідність версій:** версія документації відповідає версії застосунку (SemVer).

| Версія застосунку | Версія документації | Дія |
| :--- | :--- | :--- |
| `v1.0.0` → `v1.0.1` (patch) | Немає нової версії | Документ оновлюється in-place |
| `v1.0.x` → `v1.1.0` (minor) | `docs/v1.1` | Нова гілка документації |
| `v1.x.x` → `v2.0.0` (major) | `docs/v2` | Нова версія, стара архівується |

**Правило тегування:**

```bash
# При релізі застосунку v1.1.0
git tag -a docs/v1.1.0 -m "Documentation for release v1.1.0"
git push origin docs/v1.1.0
```

При push тегу `docs/v*.*.*` пайплайн публікує документацію також за URL `/v1.1/`.

---

*Пов'язані документи: [Definition of Done](definition-of-done.md) | [OpenAPI](api/openapi.yaml) | [Storybook](ui/storybook.md)*
