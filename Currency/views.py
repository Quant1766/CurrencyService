from datetime import datetime

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model  # If used custom user model

from Currency.serializers import UserSerializer, CurrencySerializer, Currency


class CurrencyAPI(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencySerializer
    model = Currency

    def get_queryset(self):
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        date_c = self.request.query_params.get('date', None)
        if date_c:
            queryset = self.model.objects.filter(
                exchangedate=datetime.strptime(date_c, '%d.%m.%Y'),
            )
        elif to_date and from_date:
            queryset = self.model.objects.filter(
                exchangedate__gte=datetime.strptime(from_date, '%d.%m.%Y'),
                exchangedate__lte=datetime.strptime(to_date, '%d.%m.%Y')
            )
        elif to_date:
            from_date = '06.01.1996'
            queryset = self.model.objects.filter(
                exchangedate__gte=datetime.strptime(from_date, '%d.%m.%Y'),
                exchangedate__lte=datetime.strptime(to_date, '%d.%m.%Y')
            )

        elif from_date:
            queryset = self.model.objects.filter(
                exchangedate__gte=datetime.strptime(from_date, '%d.%m.%Y'),
                exchangedate__lte=datetime.now().date()
            )
        else:
            queryset = self.model.objects.filter(
                exchangedate=datetime.now().date(),
            )
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = UserSerializer
