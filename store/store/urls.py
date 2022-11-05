from django.urls import path, include
from rest_framework import routers

from cars import views as vcar
from users import views as vuser

router = routers.DefaultRouter()

urlpatterns = [
    path('cars/', vcar.cars.as_view(), name='cars'),
    path('users/', vuser.users.as_view(), name='users'),
    path('', include(router.urls))
]
