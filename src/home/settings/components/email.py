EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = NotImplemented
EMAIL_HOST_PASSWORD = NotImplemented

EMAIL_REGISTER_SUBJECT = "Welcome"
EMAIL_REGISTER_MESSAGE = "Hey there! Welcome to our platform."
EMAIL_RESETPASSWORD_SUBJECT = "OTP number for resetting password"
EMAIL_RESETPASSWORD_MESSAGE = "Hello, \n Use OTP number below to reset your password"
