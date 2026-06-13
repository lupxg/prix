import os
from typing import List, Type

def read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


password = read_secret(os.getenv("MARIADB_ROOT_PASSWORD_FILE"))
host = os.getenv("MARIADB_HOST", "db")
user = os.getenv("MARIADB_USER", "root")
name = os.getenv("MARIADB_NAME", "spost")
port = os.getenv("MARIADB_PORT", "3306")
db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


SECRET_KEY = "JGAA9GA9AGHUAGJAKGJAGjgakl7ga7uklfjalkgklasjflasjflasjflkasjflkasjfklasjklgaioutuiujgklj"
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 200,
    "pool_pre_ping": True,
}
SQLALCHEMY_DATABASE_URI = os.getenv("MARIADB_DATABASE_URL", db_url)


# JWT config.
jwt_token_expires = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900)
jwt_refresh_token_expires = os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 604800)
