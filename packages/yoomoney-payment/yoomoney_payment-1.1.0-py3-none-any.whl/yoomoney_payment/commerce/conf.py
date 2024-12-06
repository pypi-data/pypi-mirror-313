from django.conf import settings


HASH_SECRET_KEY = getattr(settings, "HASH_SECRET_KEY", "cgDywMThqhuxBOEEnjhfgeFGxBJZJJLa6Xc3WpqKn")
YOOMONEY_EXTENSION_URL = getattr(settings, "YOOMONEY_EXTENSION_URL", None)
