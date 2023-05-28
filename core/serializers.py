from rest_framework import serializers

from core.models import CurrencyChangeRequest


class CurrencyChangeRequestSerializer(serializers.ModelSerializer):
    value = serializers.FloatField()

    def validate(self, data):
        if data['value'] <= 0:
            raise serializers.ValidationError('value must be greater than 0.')

        return data

    class Meta:
        model = CurrencyChangeRequest
        fields = "__all__"
