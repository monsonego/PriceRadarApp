# Shopping Price Alert App - EX1

This project is the EX1 backend for a shopping price alert application. Users can track products, store the current price, and define a target price for future alerts.

The design stays intentionally small for EX1, but the codebase already uses a database-backed structure that can grow into EX2 and EX3 without replacing the core API.

## Tech Stack

- FastAPI
- SQLModel
- SQLite
- pytest
- repository/service structure for easier extension

## API Resource

The core resource is `tracked products`.

Fields:

- `id`
- `name`
- `store`
- `product_url`
- `current_price`
- `target_price`
- `currency`
- `is_active`
- `created_at`

## Setup with uv

1. Create a virtual environment:

```bash
uv venv
```

2. Activate it:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

4. Optional: seed sample products

```bash
python scripts/seed_products.py
```

## Run the API

```bash
uv run uvicorn app.main:app --reload
```

The API will start on `http://127.0.0.1:8000`.

Interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Useful endpoints:

- `GET /health`
- `GET /products`
- `GET /products/{id}`
- `POST /products`
- `PUT /products/{id}`
- `DELETE /products/{id}`

## Run Tests

```bash
uv run pytest
```

If you do not have `uv` installed yet, you can also run:

```bash
python -m pytest
```

## Project Structure

- `app/main.py`: FastAPI routes and app startup
- `app/models.py`: SQLModel entities and API schemas
- `app/database.py`: database engine and sessions
- `app/repositories.py`: data-access layer
- `app/services.py`: business logic layer
- `tests/test_main.py`: API tests
- `scripts/seed_products.py`: sample data seeding
- `requests.http`: manual API playground

## Environment Variable

The database URL can be overridden for future exercises:

```bash
$env:DATABASE_URL="sqlite:///./shopping_price_alert.db"
```

## Example Request

```json
{
  "name": "Sony WH-1000XM5",
  "store": "KSP",
  "product_url": "https://example.com/products/sony-wh1000xm5",
  "current_price": 1299.9,
  "target_price": 999.9,
  "currency": "ILS",
  "is_active": true
}
```

## Notes for Future Exercises

- EX2 can reuse this API from a Streamlit dashboard or Typer CLI.
- EX3 can add users, alerts, notifications, JWT protection, Redis, and a background worker without replacing the core product model.
- The `DATABASE_URL` setting makes it easier to switch from SQLite to another database later.
- The service/repository split is in place so new features do not need to be mixed directly into the route handlers.
- Use `requests.http` to manually exercise the API in VS Code or IntelliJ HTTP Client.
- Do not commit SQLite artifacts such as `shopping_price_alert.db`; regenerate the database locally when needed.

## AI Assistance

This project was developed with AI assistance for planning, scaffolding, and code review. All generated output should be verified locally by running the API and the tests.
