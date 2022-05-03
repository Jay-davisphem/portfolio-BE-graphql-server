from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from .models import Portfolio, Project, Skill

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "email", "id")


class PortfolioType(DjangoObjectType):
    class Meta:
        model = Portfolio
        fields = "__all__"


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    get_portfolio = graphene.Field(PortfolioType, title=graphene.String(required=True))
    get_portfolios = graphene.List(PortfolioType)

    @login_required
    def resolve_me(self, info, **kwarg):
        return info.context.user

    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_get_portfolio(self, info, title):
        return Portfolio.objects.get(title=title)

    @login_required
    def resolve_get_portfolios(self, info):
        return Portfolio.objects.select_related("owner").filter(owner=info.context.user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
