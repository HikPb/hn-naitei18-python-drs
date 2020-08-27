from django.apps import AppConfig


class DrsConfig(AppConfig):
    name = 'drs'

class UserConfig(AppConfig):
    name = 'drs'
    def ready(self):
        import drs.signals
