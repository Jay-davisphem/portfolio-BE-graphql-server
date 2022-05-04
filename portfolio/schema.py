from django.contrib.auth import get_user_model
import django

import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload

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
    def resolve_me(self, info, **kwarg):
        return info.context.user

    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_get_portfolio(self, info, title):
        return Portfolio.objects.select_related("owner").get(
            owner=info.context.user, title=title
        )

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
        if info.context.user.is_anonymous:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            return CreateUser(
                ok=True, user=user, message=f"Successfully created user {user.username}"
            )
        return CreateUser(
            ok=False,
            message=f"User {info.context.user.username} is logged in!. Failed to create new account ):.",
            user=info.context.user,
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

        user = get_user_model().objects.get(username=username)

        if user or user.is_superuser:
            user.username = kwargs.get("username", username)
            user.email = kwargs.get("email", email)
            if kwargs.get("password", ""):
                user.set_password(kwargs.get("password"))
            user.save()

            return UpdateUser(ok=True, message="User details updated", user=user)
        return UpdateUser(ok=False, message="Can only update personal data!")


class DeleteUser(graphene.Mutation):
    message = graphene.String()
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)

    @login_required
    def mutate(self, info, username):
        if info.context.user.is_superuser and info.context.user.username != username:
            user = get_user_model().objects.get(username=username).delete()
            return DeleteUser(message=f"{user} deleted!", ok=True)
        return DeleteUser(message="Not deleted!", ok=False)


class CreatePortfolio(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        title = graphene.String(required=True)

    @login_required
    def mutate(self, info, title):
        try:
            Portfolio.objects.create(owner=info.context.user, title=title)
            ok = True
            message = f"Portfolio {title} created for user {info.context.user.username}"
        except django.db.utils.IntegrityError as err:
            ok = False
            message = f"{err}"
        except:
            ok = False
            message = (
                f"Cannot create portfolio {title} for user {info.context.user.username}"
            )
        return CreatePortfolio(ok=ok, message=message)


class CreateProject(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        image = Upload(description="Project image")
        deployed_at = graphene.String(required=True)
        code_url = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):

        name = kwargs.get("name")
        description = kwargs.get("description")
        image = kwargs.get("image", None)
        de_at = kwargs.get("deployed_at")
        co_u = kwargs.get("code_url", "")

        file_data = {}
        if image:
            file_data = {"image": image}

        try:
            project = Project.objects.create(
                name=name,
                description=description,
                image=image,
                deployed_at=de_at,
                code_url=co_u,
            )
            message = f"Successfully created {project.name} with {project.image.photo}"
            ok = True
        except Exception as err:
            message = f"Fail to create {project.name}"
            ok = False
        return CreateProject(ok=ok, message=message)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_portfolio = CreatePortfolio.Field()
    create_project = CreateProject.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
