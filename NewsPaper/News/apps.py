from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'News'

    def ready(self):
        import News.signals
