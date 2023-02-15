INSTALLED_APPS += ("rest_framework",)  # type: ignore # noqa: F821

REST_FRAMEWORK = {
    # "DEFAULT_SCHEMA_CLASS": ("rest_framework.schemas.coreapi.AutoSchema"),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}
