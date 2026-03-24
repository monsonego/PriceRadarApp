from os import getenv


def get_database_url() -> str:
    return getenv("DATABASE_URL", "sqlite:///./shopping_price_alert.db")
