from django.contrib.auth import get_user_model
import django

import graphene

import graphql_jwt
from graphql_jwt.decorators import login_required

from .models import Portfolio, Project, Skill
from .gql.types import UserType, PortfolioType, ProjectType, SkillType
from .gql.mutations import (
    CreateUser,
    UpdateUser,
    DeleteUser,
    CreatePortfolio,
    CreateProject,
    UpdateProject,
    CreateSkill,
)

User = get_user_model()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    get_portfolio = graphene.Field(PortfolioType, title=graphene.String(required=True))
    get_portfolios = graphene.List(PortfolioType)

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user

    def resolve_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_get_portfolio(self, info, title):
        return Portfolio.objects.select_related("owner").get(
            owner=info.context.user, title=title
        )

    @login_required
    def resolve_get_portfolios(self, info):
        return Portfolio.objects.select_related("owner").filter(owner=info.context.user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_portfolio = CreatePortfolio.Field()
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    create_skill = CreateSkill.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
