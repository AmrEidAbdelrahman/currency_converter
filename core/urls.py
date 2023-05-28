from django.urls import path, include

from core.views import CurrencyConverterView

urlpatterns = [
    path('currency_converter/', CurrencyConverterView.as_view({'post': 'convert_currency'}), name="convert_currency"),
]
