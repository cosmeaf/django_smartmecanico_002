from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'profile', views.ProfileModelViewSet, basename='profile')
router.register(r'address', views.AddressModelViewSet, basename='vehicle')
router.register(r'vehicle', views.VehicleModelViewSet, basename='address')
router.register(r'service', views.ServiceReadOnlyModelViewSet, basename='service')
router.register(r'schedule', views.ScheduleModelViewSet, basename='schedule')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='rest_framework'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
