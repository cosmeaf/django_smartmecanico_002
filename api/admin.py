from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Address, HourAvailable, Profile, Schedule, Service, Vehicle
admin.site.register(Address)
admin.site.register(HourAvailable)
admin.site.register(Service)
admin.site.register(Vehicle)

############################## PROFILE ADMIN  ##############################
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'user', 'phone_number', 'birthdate', 'biography')

    exclude = ['user', ]
    list_display_links = ('image_tag', 'user',)
    # readonly_fields = ['created_at', 'updated_at', 'deleted_at']

    def image_tag(self, obj):
        return format_html('<img src="{0}", style="width: 40px;" />'.format(obj.image.url))

    def delete(self, *args, **kwargs):
        """
        Delete Image From Media
        """
        storage, path = self.image.storage, self.image.path
        super(Profile, self).delete(*args, **kwargs)
        storage.delete(path)

    def get_queryset(self, request):
        """
        Show result user by id
        """
        queryset = super(ProfileAdmin, self).get_queryset(request)
        if (request.user.is_superuser):
            return queryset
        else:
            return queryset.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        """
        Change Method for save Profile data on Database
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)      
############################## SCHEDULE ADMIN  ##############################  
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('address', 'vehicle', 'service', 'hour', 'day','created_at', 'updated_at', 'user')
    # exclude = ['user', ]
    list_display_links = ('day',)
    readonly_fields = ['user', 'created_at', 'updated_at', 'deleted_at']

    def get_queryset(self, request):
        """
        Show result user by id
        """
        queryset = super(ScheduleAdmin, self).get_queryset(request)
        if (request.user.is_superuser):
            return queryset
        else:
            return queryset.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        """
        Change Method for save Service data on Database
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)