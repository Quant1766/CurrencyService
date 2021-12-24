from django.urls import path, include

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from Currency.api import CurrencyAPI, CreateUserView

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
# Inlcude the schema view in our urls.
urlpatterns = [
    path('currency/', CurrencyAPI.as_view(), name='exchange'),
    path('', schema_view, name='docs'),
    path('register/', CreateUserView.as_view(),name='register')
]
