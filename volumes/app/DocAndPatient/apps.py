from django.apps import AppConfig


class DoctorAndPatientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DocAndPatient'

    def ready(self) -> None:
        import DocAndPatient.signals
