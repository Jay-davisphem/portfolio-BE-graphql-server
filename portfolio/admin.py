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
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "username",
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


class ModelProject(admin.ModelAdmin):
    model = Project
    list_display = ("name", "deployed_at", "image")


class ModelSkill(admin.ModelAdmin):
    model = Skill
    list_display = ("name", "image")


admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)
admin.site.register(Project, ModelProject)
admin.site.register(Skill, ModelSkill)
