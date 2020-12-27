from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = 'api.crm'
    verbose_name = 'API CRM - SALES'

    def ready(self):
        import api.crm.signals
