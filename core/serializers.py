from rest_framework import serializers

from core.models import CurrencyChangeRequest


class CurrencyChangeRequestSerializer(serializers.ModelSerializer):
    value = serializers.FloatField()

    def validate(self, data):
        if data['value'] <= 0:
            raise serializers.ValidationError('value must be greater than 0.')

        return data

    def create(self, validated_data):
        ModelClass = self.Meta.model
        user = self.context.get('user')

        instance, created = ModelClass.objects.get_or_create(
            source_currency=validated_data['source_currency'],
            target_currency=validated_data['target_currency'],
            user=user
        )
        if not created:
            instance.number_of_requests = instance.number_of_requests + 1
            instance.save()

        return instance

    class Meta:
        model = CurrencyChangeRequest
        exclude = ['user']
