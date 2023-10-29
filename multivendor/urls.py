from .views import *
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('seller', UserSellerViewSet, basename='seller')
router.register('buyer', UserBuyerViewSet, basename='buyer')
urlpatterns = [
    path('user/', UserGeneric_list.as_view(), name='login'),

    ]

urlpatterns += router.urls