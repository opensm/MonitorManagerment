from django.core.management.base import BaseCommand, CommandError
from django.apps import AppConfig
from logpipe import Consumer, register_consumer
from monitor.serializer import PrometheusSerializer
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            consumer = Consumer('test', consumer_timeout_ms=1000)
            consumer.register(PrometheusSerializer)
            consumer.run()
            time.sleep(1)
