from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Hobby, User

admin.site.unregister(Group)
admin.site.register(Hobby)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Change the layout and view of User model in Admin Panel
    """

    list_display = ["phone_number", "full_name", "last_login", "is_active"]
    ordering = ["date_joined"]
    search_fields = ["phone_number", "full_name", "bio"]
    date_hierarchy = "date_joined"
    list_per_page = 50
    list_filter = ["is_active", "is_staff", "is_superuser"]
    readonly_fields = ["last_login", "date_joined"]
    add_fieldsets = (
        (None, {"fields": ("phone_number", "password1", "password2")}),
        (
            "User Details",
            {
                "fields": (
                    "full_name",
                    "date_of_birth",
                    "gender",
                    "show",
                    "profile_photo",
                )
            },
        ),
        ("User Meta", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            "User Details",
            {
                "fields": (
                    "full_name",
                    "date_of_birth",
                    "gender",
                    "show",
                    "profile_photo",
                    "bio",
                    "hobbies",
                )
            },
        ),
        (
            "User Meta",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "last_login",
                    "date_joined",
                )
            },
        ),
        ("Permissions", {"classes": ("collapse",), "fields": ("user_permissions",)}),
    )

    # Removing default delete action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions
