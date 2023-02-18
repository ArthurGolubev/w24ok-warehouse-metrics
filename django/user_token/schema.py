import graphene

from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    # ДОБАВЛЕНИЕ НАСТРОЕК ПО JWT в SETTINGS даёт обработку в мидлвере для предоставления
    # в context.user проверку не по Cookie, а по JWT
    # в таком случае механизм JWT сверяет пароль на сервере и присланный токен (так думаю)
    class Meta:
        model = get_user_model()

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    created_user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username, first_name, last_name, email, password):
        u = get_user_model()(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        u.set_password(password)
        u.save()
        return CreateUserMutation(created_user=u)

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_me(root, info, **kwargs):
        user = info.context.user
        print(info.context.headers.items())
    
        print(f'resolve_me {info.context.user}')
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user
        
    def resolve_users(root, info):
        return get_user_model().objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)