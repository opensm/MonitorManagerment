# myapp/apps.py
from django.apps import AppConfig
from logpipe import Consumer, register_consumer
from .serializer import PrometheusSerializer


class MyAppConfig(AppConfig):
    name = 'monitor'


# Register consumers with logpipe
@register_consumer
def build_person_consumer():
    consumer = Consumer('test')
    consumer.register(PrometheusSerializer)
    return consumer
