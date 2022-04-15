from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from users.models import User


admin.site.unregister(Group)


# Get user's IP from a request
def GET_USER_IP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Change the layout and view of User model in Admin Panel
    """

    list_display = ['phone_number', 'full_name', 'last_login', 'is_active']
    ordering = ['date_joined']
    search_fields = ['phone_number', 'full_name', 'bio']
    date_hierarchy = 'date_joined'
    list_per_page = 50
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['last_login', 'date_joined', 'user_created_ip']
    add_fieldsets = (
        (None, {
            'fields' : (
                'phone_number',
                'password1',
                'password2'
            )
        }),
        ('User Details', {
            'fields' : (
                'full_name',
                'date_of_birth',
                'gender',
                'show',
                'profile_photo'
            )
        }),
        ('User Meta', {
            'fields' : (
                'is_active',
                'is_staff',
                'is_superuser'
            )
        })
    )
    fieldsets = (
        (None, {
            'fields' : (
                'phone_number',
                'password'
            )
        }),
        ('User Details', {
            'fields' : (
                'full_name',
                'date_of_birth',
                'gender',
                'show',
                'profile_photo',
                'bio',
                'hobbies'
            )
        }),
        ('User Meta', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'last_login',
                'date_joined',
                'user_created_ip'
                )
        }),
        ('Permissions', {
            'classes' : ('collapse',),
            'fields' : (
                'user_permissions',
            )
        })
    )


    # Removing default delete action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    

    # Overriding default save method to add IPs and author
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user_created_ip = GET_USER_IP(request)
        super().save_model(request, obj, form, change)