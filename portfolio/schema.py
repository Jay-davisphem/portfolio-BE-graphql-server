from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
User = get_user_model()
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')
class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info, **kwarg):
        return info.context.user

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
