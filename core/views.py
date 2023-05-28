from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from core.models import CurrencyChangeRequest
from django.db import models
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status

from core.services.utils import Utils


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CurrencyConverterView(ViewSet):

    @swagger_auto_schema(
        operation_description="convert from source_currency to target_currency",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'source_currency': openapi.Schema(type=openapi.TYPE_STRING, description="currency option ['usd', 'eur', 'egp']"),
                'target_currency': openapi.Schema(type=openapi.TYPE_STRING, description="currency option ['usd', 'eur', 'egp']"),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER, description="value to convert")
            }
        ),
    )
    @action(detail=True, methods=['post'])
    def convert_currency(self, request):
        available_currency = ['usd', 'eur', 'egp']
        source_currency = request.data.get('source_currency')
        target_currency = request.data.get('target_currency')
        val = request.data.get('value', 1)
        if val <= 0:
            return Response({'error': 'value must be greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)
        if source_currency not in available_currency:
            return Response({'error': "source_currency must be in ['usd', 'eur', 'egp']."}, status=status.HTTP_400_BAD_REQUEST)
        if target_currency not in available_currency:
            return Response({'error': "target_currency must be in ['usd', 'eur', 'egp']."}, status=status.HTTP_400_BAD_REQUEST)

        instance, created = CurrencyChangeRequest.objects.get_or_create(
            source_currency=source_currency,
            target_currency=target_currency,
        )
        if not created:
            instance.number_of_requests = instance.number_of_requests + 1
            instance.save()

        res = Utils.get_latest_exchange_rates(source_currency, target_currency, val)
        return Response({'res': res}, status=status.HTTP_200_OK)
