from django.apps import AppConfig


class ECommerceConfig(AppConfig):
    name = 'e_commerce'

    def ready(self):
        import e_commerce.signals