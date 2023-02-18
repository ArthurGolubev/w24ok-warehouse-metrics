import datetime
import graphene
from loguru import logger
from django.db.models import Count, Sum, F
from .models import Prolongation, Transaction, Username, Warehouse
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from operator import itemgetter
from .graphene_types import InOutUsersType, OrgsTopType, ProlongationType, SevenDaysType, MonthToMonthType, TransactionType, UserTopType, UsernameType, WarehouseType
import time
from main.resolvers.in_out_users import in_out_users
from main.resolvers.month_to_month import month_to_month
from main.resolvers.TransactionsMutation import TransactionsMutation
from main.resolvers.ProlongationsMutation import ProlongationsMutation
from main.resolvers.ReductionFineMutation import ReductionFineMutation
from graphene_django import DjangoListField



class Mutation(graphene.ObjectType):
    push_transactions = TransactionsMutation.Field()
    push_prolongations = ProlongationsMutation.Field()
    push_decreases = ReductionFineMutation.Field()



class Query(graphene.ObjectType):

    warh_list       = graphene.List(WarehouseType)
    seven_days      = graphene.List(SevenDaysType, warh=graphene.String())
    in_out_users    = graphene.List(InOutUsersType, warh=graphene.String())
    month_to_month  = graphene.List(MonthToMonthType, warh=graphene.String())
    top_users       = graphene.List(UserTopType, warh=graphene.String(), range_top=graphene.String())
    top_orgs        = graphene.List(OrgsTopType, warh=graphene.String(), range_top=graphene.String())
    prolongations   = DjangoListField(ProlongationType, warh=graphene.String())



    @logger.catch
    @login_required
    def resolve_top_users(root, info, warh, range_top):
        if not info.context.user.has_perm(f'main.can_view_warh_{warh}'):
            return GraphQLError('Permission denied')
        warh = Warehouse.objects.get(short_name=warh)
        now = datetime.datetime.now()
        if range_top == 'month':
            response = Transaction.objects.filter(
                warh=warh,
                datetime__month=now.month,
                datetime__year=now.year
                )
        else:
            response = Transaction.objects.filter(
                warh=warh,
                datetime__year=now.year
                )
        response = response.values('user__username').annotate(Count('id'))
        response = sorted(response, key=itemgetter('id__count'), reverse=True)
        return response



    @logger.catch
    @login_required
    def resolve_prolongations(root, info, warh):
        response = Prolongation.objects.filter(transact__warh__short_name=warh)
        return response



    @logger.catch
    @login_required
    def resolve_top_orgs(root, info, warh, range_top):
        if not info.context.user.has_perm(f'main.can_view_warh_{warh}'):
            return GraphQLError('Permission denied')
        warh = Warehouse.objects.get(short_name=warh)
        now = datetime.datetime.now()
        if range_top == 'month':
            response = Transaction.objects.filter(
                warh=warh,
                datetime__month=now.month,
                datetime__year=now.year
                )
        else:
            response = Transaction.objects.filter(
                warh=warh,
                datetime__year=now.year
                )
        response = response.values('org__username').annotate(Count('id'))
        response = sorted(response, key=itemgetter('id__count'), reverse=True)
        return response




    @logger.catch
    @login_required
    def resolve_warh_list(root, info):
        x = info.context.user.get_group_permissions()
        warh_list = []
        for i in x:
            if i.startswith('main.can_view_warh_'):
                warh_list.append(i[19:])
        return Warehouse.objects.filter(short_name__in=warh_list)




    @logger.catch
    @login_required
    def resolve_month_to_month(root, info, warh):
        start_resolver = time.time()
        if not info.context.user.has_perm(f'main.can_view_warh_{warh}'):
            return GraphQLError('Permission denied')
        
        response = month_to_month(warh)
        response_resolver = time.time() - start_resolver
        logger.info(f"Время выполнения month_to_monthF {response_resolver}")
        return response



    @logger.catch
    @login_required
    def resolve_in_out_users(root, info, warh):
        start_resolver = time.time()
        if not info.context.user.has_perm(f'main.can_view_warh_{warh}'):
            return GraphQLError('Permission denied')
        
        response = in_out_users(warh)
        response_resolver = time.time() - start_resolver
        logger.info(f"Время выполнения in_out_users {response_resolver}")
        return response



    @logger.catch
    @login_required
    def resolve_seven_days(root, info, warh):
        if not info.context.user.has_perm(f'main.can_view_warh_{warh}'):
            return GraphQLError('Permission denied')

        m = info.context.headers.items()
        g = [f"{i}\n" for i in m]
        msg = ''.join(g)
        # logger.info(f'{msg["Origin"]=}')
        warh = Warehouse.objects.get(short_name=warh)
        start_date = datetime.date.today()-datetime.timedelta(days=7)
        end_date = datetime.date.today()
        agr_date = Transaction.objects.filter(warh=warh, datetime__date__range=(start_date, end_date)).values('datetime__date')
        response = agr_date.annotate(
            date=F('datetime__date'),
            paid=Sum('paid'),
            transactions=Count('id'),
            unique_users=Count('user', distinct=True)
            )
        return response

schema = graphene.Schema(query=Query, mutation=Mutation)
