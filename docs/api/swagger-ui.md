# Swagger UI — Інтерактивна документація API

> **Специфікація:** [openapi.yaml](openapi.yaml)  
> **Стандарт:** OpenAPI 3.0.3

---

## 1. Роль API у системі

Auth Microservice API є **internal API**:

- **Тип:** internal (не публічний, не third-party)
- **Споживачі:** Web SPA (React/Vue), Mobile App (iOS/Android), інші мікросервіси системи
- **Контракт:** специфікація `openapi.yaml` є єдиним джерелом істини для формату запитів і відповідей — backend і frontend команди домовляються на рівні YAML, а не через усні угоди

---

## 2. API-first підхід

До написання будь-якого рядка коду визначено:

| Ендпоінт | Метод | Призначення |
| :--- | :--- | :--- |
| `/api/v1/auth/register` | `POST` | Реєстрація нового користувача |
| `/api/v1/auth/login` | `POST` | Авторизація, отримання JWT-токенів |
| `/api/v1/auth/refresh` | `POST` | Оновлення accessToken |

Структури запитів, відповідей та коди помилок зафіксовані в `openapi.yaml` до реалізації.

---

## 3. Запуск Swagger UI локально

### Варіант A — через Docker (рекомендовано)

```bash
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/api/openapi.yaml \
  -v $(pwd)/docs/api:/api \
  swaggerapi/swagger-ui
```

Відкрийте: `http://localhost:8080`

### Варіант B — через npm-пакет swagger-ui-express

```bash
npm install swagger-ui-express yamljs
```

```javascript
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const swaggerDoc = YAML.load('./docs/api/openapi.yaml');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDoc));
```

Відкрийте: `http://localhost:3000/api-docs`

### Варіант C — статична HTML-сторінка

```html
<!DOCTYPE html>
<html>
<head>
  <title>Auth API Docs</title>
  <link rel="stylesheet"
    href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "./openapi.yaml",
      dom_id: '#swagger-ui',
      presets: [SwaggerUIBundle.presets.apis],
      layout: "BaseLayout"
    });
  </script>
</body>
</html>
```

---

## 4. Валідація специфікації (Swagger Editor)

Для перевірки коректності `openapi.yaml`:

```bash
# Через Docker
docker run -p 8081:8080 swaggerapi/swagger-editor

# Або онлайн: editor.swagger.io
# Відкрити файл: File → Import File → openapi.yaml
```

Специфікація вважається валідною, якщо Swagger Editor не показує помилок (warnings допускаються).

---

## 5. Генерація клієнтського SDK (Swagger Codegen)

```bash
# Встановлення
npm install @openapitools/openapi-generator-cli -g

# Генерація TypeScript-клієнта для Web SPA
openapi-generator-cli generate \
  -i docs/api/openapi.yaml \
  -g typescript-axios \
  -o ./sdk/typescript-client

# Генерація Python-клієнта
openapi-generator-cli generate \
  -i docs/api/openapi.yaml \
  -g python \
  -o ./sdk/python-client
```

Згенерований SDK автоматично синхронізований з контрактом — при зміні `openapi.yaml` достатньо перегенерувати SDK.

---

*Пов'язані документи: [openapi.yaml](openapi.yaml) | [SDD](../architecture/SDD.md) | [CI/CD](../ci-cd-docs.md)*
