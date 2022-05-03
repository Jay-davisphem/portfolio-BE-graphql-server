from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Portfolio, Project, Skill

User = get_user_model()


class PortfolioInline(admin.TabularInline):
    model = Portfolio
    extra = 1


class UserModelAdmin(UserAdmin):
    inlines = [PortfolioInline]
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)


admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)
admin.site.register(Project)
admin.site.register(Skill)
