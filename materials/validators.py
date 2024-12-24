from urllib.parse import urlparse

from django.core.exceptions import ValidationError


class YouTubeURLValidator:
    """Валидатор для проверки ссылки на YouTube"""

    allowed_url = {"youtube.com"}

    def __init__(self, field="video_url"):
        self.field = field

    def __call__(self, value):
        parsed_url = urlparse(value)

        if parsed_url.netloc not in self.allowed_url:
            raise ValidationError("Недопустимая ссылка. Разрешены только ссылки на YouTube.")
