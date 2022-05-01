from django.contrib import admin
from .models import CustomUser as User, Portfolio, Project, Skill


class PortfolioInline(admin.TabularInline):
    model = Portfolio
    extra = 1


class UserModelAdmin(admin.ModelAdmin):
    inlines = [PortfolioInline]
    fieldsets = [
        (None, {"fields": ["username", "email", "password", "first_name", "last_name"]})
    ]


admin.site.register(User, UserModelAdmin)
admin.site.register(Project)
admin.site.register(Skill)
