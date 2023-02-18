from datetime import date
from .resolvers.Batching import UserLoader
import graphene
from graphene.types import field
from graphene_django import DjangoListField
from graphene_django.types import DjangoObjectType
from .models import Transaction, Username, Warehouse, Prolongation

class ProlongationType(DjangoObjectType):
    class Meta:
        model = Prolongation

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction

class WarehouseType(DjangoObjectType):
    class Meta:
        model = Warehouse

class UsernameType(DjangoObjectType):
    class Meta:
        model = Username

class UserTopType(graphene.ObjectType):
    user__username  = graphene.String()
    id__count       = graphene.Int()

class OrgsTopType(graphene.ObjectType):
    org__username  = graphene.String()
    id__count       = graphene.Int()

class UsernameType(DjangoObjectType):
    class Meta:
        model = Username

class SevenDaysType(graphene.ObjectType):
    date            = graphene.Date()
    paid            = graphene.Int()
    transactions    = graphene.Int()
    unique_users    = graphene.Int()

# class UsersByMonthType(graphene.ObjectType):
#     users       = graphene.List(lambda: UsernameType)
#     date        = graphene.Date()

#     def resolve_users(root, info):
#         ids = []
#         for user in root["users"]:
#             ids.append(user.user.id)
#         resp = UserLoader().batch_load_fn(ids)
#         # print(f'resp -> {resp.value}')
#         return resp.value


class InOutUsersType(graphene.ObjectType):
    date                    = graphene.Date()
    waterfall_step_change   = graphene.Int()
    incoming                = graphene.Int()
    departed                = graphene.Int()

class MonthToMonthBodyType(graphene.ObjectType):
    date            = graphene.Date()
    paid            = graphene.Int()
    transactions    = graphene.Int()
    unique_users    = graphene.Int()

class MonthToMonthType(graphene.ObjectType):
    date = graphene.Int()
    body = graphene.List(MonthToMonthBodyType)
