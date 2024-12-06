import logging

from django.apps import AppConfig

from .callhome import callhome_version

log = logging.getLogger(__name__)


class JfkDjangoCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jfk_django_core"
    verbose_name = "JFK Django Core"

    def ready(self) -> None:
        try:
            log.debug("Starting Callhome")
            callhome_version()
        except Exception:
            log.exception("JFK Django Core ready exception")
