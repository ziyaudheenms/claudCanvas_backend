from django.urls import path,include
from . import views
from .views import sync_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("create/user/",views.Create_user),
    path("create/user/sync-user/",sync_user, name="sync-user")

]
