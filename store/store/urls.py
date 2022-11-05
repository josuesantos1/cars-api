from django.urls import path, include
from rest_framework import routers

from cars import views

router = routers.DefaultRouter()

urlpatterns = [
    path('cars/', views.cars.as_view(), name='cars'),
    path('', include(router.urls))
]
