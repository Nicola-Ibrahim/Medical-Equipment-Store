# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_ENGINE = "django.db.backends.sqlite3"
DB_NAME = "db.sqlite3"
DB_HOST = NotImplemented
DB_PORT = NotImplemented
DB_USER = NotImplemented
DB_PASSWORD = NotImplemented

if DB_ENGINE != "django.db.backends.sqlite3":
    if not (DB_HOST and DB_PORT and DB_USER and DB_PASSWORD):
        raise ValueError("The following variables must be set [DB_HOST, DB_PORT, DB_USER, DB_PASSWORD]")

DATABASES = {
    "default": {
        "ENGINE": DB_ENGINE,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
    }
}
