from django.urls import path, include


urlpatterns = [
    path('', include('promo_checker.api')),
]
