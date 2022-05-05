from graphene_django import DjangoObjectType

from django.contrib.auth.models import User
from ..models import Portfolio, Project, Skill


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "email", "id")


class PortfolioType(DjangoObjectType):
    class Meta:
        model = Portfolio
        fields = "__all__"


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = "__all__"


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = "__all__"
