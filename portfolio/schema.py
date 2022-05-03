from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
import graphql_jwt
from graphql_jwt.decorators import login_required

from .models import Portfolio, Project, Skill


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


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    get_portfolio = graphene.Field(PortfolioType, title=graphene.String(required=True))
    get_portfolios = graphene.List(PortfolioType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

    def resolve_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_get_portfolio(self, info, title):
        return Portfolio.objects.get(title=title)

    @login_required
    def resolve_get_portfolios(self, info):
        return Portfolio.objects.select_related("owner").filter(owner=info.context.user)


class CreateUser(graphene.Mutation):
    message = graphene.String()
    user = graphene.Field(UserType)
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()

    def mutate(self, info, username, password, email=None):
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(
            ok=True, user=user, message=f"Successfully created user {user.username}"
        )


class UpdateUser(graphene.Mutation):
    message = graphene.String()
    user = graphene.Field(UserType)
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        username = info.context.user.username
        email = info.context.user.email

        user = User.objects.get(username=kwargs.get("username", None))

        user.username = kwargs.get("username", username)
        user.email = kwargs.get("email", email)
        if kwargs.get("password", ""):
            user.set_password(kwargs.get("password"))
        user.save()

        return UpdateUser(ok=True, message="User details updated", user=user)


class DeleteUser(graphene.Mutation):
    message = graphene.String()
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)

    @login_required
    def mutate(self, info, username):
        if info.context.user.is_superuser and info.context.user.username != username:
            user = User.objects.get(username=username).delete()
            return DeleteUser(message=f"{user} deleted!", ok=True)
        return DeleteUser(message="Not deleted!", ok=False)


"""class CreatePortfolio(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        owner = graphene
"""


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
