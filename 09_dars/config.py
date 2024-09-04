TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"  # SQLite ma'lumotlar bazasiga ulanish satri
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # `models` - bizning modellari, `aerich.models` - Tortoise migrations uchun
            "default_connection": "default",
        }
    },
}