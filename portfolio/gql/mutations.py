import graphene
from graphene_file_upload.scalars import Upload

import django
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.template import loader

from graphql_jwt.decorators import login_required

from ..models import Portfolio, Project, Skill
from .types import UserType, PortfolioType, ProjectType, SkillType

User = get_user_model()


class CreateUser(graphene.Mutation):
    message = graphene.String(description="Message returned from creation!")
    user = graphene.Field(UserType, description="User returned from creation!")
    ok = graphene.Boolean(description="Ok status")

    class Arguments:
        username = graphene.String(required=True, description="Unique username")
        password = graphene.String(required=True, description='password')
        email = graphene.String(description='Unique email')

    def mutate(self, info, username, password, email=None):
        if email == settings.EMAIL_HOST_USER:
            raise TypeError("Contrained! You can user email %s" % (email))
        if info.context.user.is_anonymous:
            try:
                User.objects.get(email=email)
                return CreateUser(
                    ok=False,
                    message=f"User email {email} exists!",
                )
            except:
                pass
            user = User(username=username, email=email)
            user.set_password(password)

            subject = "Welcome to daviSPhem portfolio api"

            message = f"Hi {username}, thank you for using our api."
            html_message = loader.render_to_string(
                "email.html",
                {"username": username, "subject": subject, "message": message},
            )
            print(html_message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                email,
            ]
            user.save()
            try:
                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    html_message=html_message,
                )
            except Exception as err:
                User.objects.get(username=username).delete()
                raise err
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

        user = User.objects.get(username=username)

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
            user = User.objects.get(username=username).delete()
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
        portfolio_title = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):

        name = kwargs.get("name")
        description = kwargs.get("description")
        de_at = kwargs.get("deployed_at")
        co_u = kwargs.get("code_url", "")
        post = info.context.FILES.get("image")
        title = kwargs.get("portfolio_title")
        port = None
        if title:
            port = Portfolio.objects.get_or_create(owner=info.context.user, title=title)
        else:
            return CreateProject(ok=False, message="Please provide a portfolio title")
        try:
            project = Project.objects.create(
                name=name,
                description=description,
                image=post if image else None,
                deployed_at=de_at,
                code_url=co_u,
                portfolio=port,
            )
            message = f"Successfully created {project.name} with {project.image.photo}"
            ok = True
        except Exception as err:
            message = f"Failed {err}"
            ok = False if "no attribute 'photo'" not in str(err) else True
            if ok:
                message = f"Warning {err}"
        return CreateProject(ok=ok, message=message)


class UpdateProject(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        new_name = graphene.String()
        description = graphene.String()
        image = Upload(description="Project image")
        deployed_at = graphene.String()
        code_url = graphene.String()
        portfolio_title = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        name = kwargs.get("name")
        new_name = kwargs.get("new_name")
        description = kwargs.get("description")
        image = info.context.FILES.get("image")
        dep_url = kwargs.get("deployed_at")
        portfolio_title = kwargs.get("portfolio_title")
        code_u = kwargs.get("code_url")
        ok = False
        message = ""
        try:
            project = Project.objects.get(
                name=name,
                portfolio=Portfolio.objects.get_or_create(
                    owner=info.context.user, title=portfolio_title
                )[0],
            )
            if new_name:
                project.name = new_name
            project.description = description
            project.image = image
            project.deployed_at = dep_url
            project.code_url = code_u
            ok = True
            message = (
                f"Project {name} updated {'to ' +new_name +'!' if new_name else '!'}"
            )
        except Exception as err:
            message = err

        return UpdateProject(ok=ok, message=message)


class CreateSkill(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        image = Upload(description="Skill icon")
        portfolio_title = graphene.String(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        name = kwargs.get("name")
        image = info.context.FILES.get("image")
        portfolio = Portfolio.objects.get_or_create(
            owner=info.context.user, title=portfolio_title
        )
        Skill.objects.create(name=name, image=image, portfolio=portfolio[0])
        return CreateSkill(ok=True, message=f"{name} Skill Created")


class ContactMe(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        message = graphene.String(required=True)

    def mutate(self, info, email, message):
        admin_mail = settings.EMAIL_HOST_USER
        admin_message = ("Hi, I am %s" % email, message, admin_mail, [admin_mail])
        user_message = (
            "Message from David Oluwafemi",
            "This is an automatic response, I'll respond soon.",
            admin_mail,
            [email],
        )

        try:
            send_mass_mail((admin_message, user_message), fail_silently=False)
            return ContactMe(ok=True, message="Message sent to %s!" % admin_mail)
        except:
            return ContactMe(ok=False, message="Message not sent!")
