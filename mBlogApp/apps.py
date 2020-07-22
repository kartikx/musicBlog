from django.apps import AppConfig


class MblogappConfig(AppConfig):
    name = 'mBlogApp'

    def ready(self):
        import mBlogApp.signals
