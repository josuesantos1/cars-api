from django.urls import path, include
from rest_framework import routers

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from cars import views as vcar
from users import views as vuser
from uploader import views as vfile

router = routers.DefaultRouter()

urlpatterns = [
    path('cars/', vcar.cars.as_view(), name='cars'),
    path('users/', vuser.users.as_view(), name='users'),
    path('login/', vuser.Login.as_view(), name='login'),
    path('files/', vfile.Uploader.as_view(), name='file'),
    path('', include(router.urls))
] 
