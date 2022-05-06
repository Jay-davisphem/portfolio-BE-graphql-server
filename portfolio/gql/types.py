from graphene_django import DjangoObjectType

from django.contrib.auth.models import User
from ..models import Portfolio, Project, Skill


class UserType(DjangoObjectType):
    class Meta:
        description = "GraphQL Type of User"
        model = User
        fields = ("username", "email", "id")


class PortfolioType(DjangoObjectType):
    class Meta:
        description = "GraphQL Type of Portfolio!"
        model = Portfolio
        fields = "__all__"


class ProjectType(DjangoObjectType):
    class Meta:
        description = "GraphQL Type of Project"
        model = Project
        fields = "__all__"


class SkillType(DjangoObjectType):
    class Meta:
        description = "GraphQL Type of Skill"
        model = Skill
        fields = "__all__"
