from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Address, HourAvailable, Schedule, Service, Vehicle, Profile
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.utils.translation import gettext_lazy as _

admin.site.register(Address)
admin.site.register(HourAvailable)
admin.site.register(Service)
admin.site.register(Vehicle)


class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def get_actions(self, request):
        actions = super(OutstandingTokenAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)

############################## PRFILE ADMIN  ############################## 
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('foto', 'user','phone_number','birthday',)

#     #exclude = ['user', ]
#     #list_display_links = ('image_tag',)
#     #readonly_fields = ['created_at', 'updated_at', 'deleted_at']

#     def foto(self, obj):
#         return format_html('<img src="{0}", style="width: 40px;" />'.format(obj.image.url))

#     def delete(self, *args, **kwargs):
#         """
#         Delete Image From Media
#         """
#         storage, path = self.image.storage, self.image.path
#         super(Profile, self).delete(*args, **kwargs)
#         storage.delete(path)

#     def get_queryset(self, request):
#         """
#         Show result user by id
#         """
#         queryset = super(ProfileAdmin, self).get_queryset(request)
#         if (request.user.is_superuser):
#             return queryset
#         else:
#             return queryset.filter(user_id=request.user)

#     def save_model(self, request, obj, form, change):
#         """
#         Change Method for save Service data on Database
#         """
#         obj.user = request.user
#         super().save_model(request, obj, form, change)

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
        
########################################################################################
