from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView,TokenBlacklistView)
from api import views


router = routers.DefaultRouter()
router.register(r'user', views.UserModelViewSet, basename='user')
router.register(r'profile', views.UserProfileModelViewSet, basename='profile')
router.register(r'address', views.AddressModelViewSet, basename='address')
router.register(r'vehicle', views.VehicleModelViewSet, basename='vehicle')
router.register(r'service', views.ServiceReadOnlyModelViewSet, basename='service')
router.register(r'schedule', views.ScheduleModelViewSet, basename='schedule')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.UserRegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(router.urls)),
    # path('', include('rest_framework.urls', namespace='rest_framework'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
