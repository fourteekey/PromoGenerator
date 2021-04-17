from django.urls import path
from . import views


urlpatterns = [
    path('promo', views.PromoCheckerAPIView.as_view(), name='promo_check'),
    path('promo/generate', views.PromoGeneratorAPIView.as_view(), name='promo_generate'),

]
