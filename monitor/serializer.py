from rest_framework import serializers
from monitor.models import AlertPrometheus
import simplejson as json


class Jsonserializer(serializers.JSONField):
    default_error_messages = {
        'invalid_json': "Incorrect json value"
    }

    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        try:
            if not isinstance(data, dict):
                return json.loads(data)
            return data
        except (TypeError, ValueError):
            self.fail('invalid_json')


class PrometheusSerializer(serializers.ModelSerializer):
    labels = Jsonserializer()
    annotations = Jsonserializer()

    MESSAGE_TYPE = 'prometheus'
    VERSION = 1
    KEY_FIELD = 'event_id'

    class Meta:
        model = AlertPrometheus
        fields = '__all__'
        widget = {
            'labels': serializers.JSONField(),
            'annotations': serializers.JSONField()
        }

    @classmethod
    def lookup_instance(cls, **kwargs):
        try:
            return AlertPrometheus.objects.get(
                event_id=kwargs['event_id']
            )
        except AlertPrometheus.DoesNotExist:
            pass
