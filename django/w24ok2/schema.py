import graphene
from graphene_django.debug.types import DjangoDebug
import graphql_jwt

import main.schema
import user_token.schema

class Query(
    main.schema.Query,
    user_token.schema.Query,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')

class Mutation(
    main.schema.Mutation,
    user_token.schema.Mutation,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)