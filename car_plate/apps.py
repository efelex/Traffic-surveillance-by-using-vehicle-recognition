from django.apps import AppConfig


class CarPlateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'car_plate'

    def ready(self):
        import car_plate.signals
