import datetime
import time
from loguru import logger
from django.core.cache import cache
from ..models import Transaction, Warehouse
from calendar import monthrange
from graphql import GraphQLError




def in_out_users(warh):
    logger_message = []
    response = cache.get(f'in_out_users_{warh}')
    if response:
        return response

    warh = Warehouse.objects.get(short_name=warh)
    first = Transaction.objects.filter(warh=warh).order_by('datetime').first()
    if first:
        first = first.datetime
    else:
        return GraphQLError(f'В базе данных нет транзакция склада {warh} чтобы взять first.datetime в in_out_users')
    last = Transaction.objects.filter(warh=warh).order_by('datetime').last().datetime
    def month_year_iter(start_month, start_year, end_month, end_year):
        ym_start= 12*start_year + start_month - 1
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            yield y, m+1
    
    def calculate_payload(year, month):
        cur = Transaction.objects.filter(warh=warh, datetime__year=year, datetime__month=month).order_by('user').distinct('user')
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        prev = Transaction.objects.filter(warh=warh, datetime__year=prev_year, datetime__month=prev_month).order_by('user').distinct('user')
        cur_users = []
        prev_users = []
        for user in cur:
            cur_users.append(user.user.id)
        for user in prev:
            prev_users.append(user.user.id)
        last_day = monthrange(year, month)[1]
        logger_message.append('case 1.0')
        incoming = len(set(cur_users).difference(set(prev_users)))
        departed = len(set(prev_users).difference(set(cur_users)))
        re = {
            "date": datetime.date(year, month, last_day),
            "waterfall_step_change": incoming - departed,
            "incoming": incoming,
            "departed": departed,
        }
        return re

    range_iterator = month_year_iter(1, first.year, last.month, last.year)
    response = {}
    for month in range_iterator:
        cache_month = cache.get(f'in_out_users_{warh}_{month[0]}_{month[1]}')
        if cache_month:
            '''Месяц есть в кэше'''
            logger_message.append(f'in_out_users {warh} case 1.2')
            response[month] = cache_month
        else:
            '''Месяца нет в кэше'''
            logger_message.append(f'in_out_users {warh} case 1.3')
            payload = calculate_payload(year=month[0], month=month[1])
            response[month] = payload
            cache.set(f'in_out_users_{warh}_{month[0]}_{month[1]}', payload, None)

    '''Пересчитать текущий и предыдущий месяц'''
    '''
    Текущий - ежедневно обновляется, его надо пересчитывать.
    Предыдущий - может быть не полным,
    если кэш обновился последний раз, к примеру, 24 числа
    (последний запрос текущего месяца) после чего запросов на обновление текущего месяца небыло
    а месяц начался следующий - он стал текущим, а предыдущий так и сотался в кэше с обновлением 24 числа
    '''
    '''Обновление текущего месяца'''
    payload = calculate_payload(year=month[0], month=month[1])
    response[month] = payload
    cache.set(f'in_out_users_{warh}_{month[0]}_{month[1]}', payload, None)
    '''Обновление предыдущего месяца'''
    if month[1] != 1:
        payload = calculate_payload(year=month[0], month=month[1]-1)
        response[(month[0], month[1]-1)] = payload
        cache.set(f'in_out_users_{warh}_{month[0]}_{month[1]-1}', payload, None)

    logger.info('\n'.join(logger_message))
    logger.info(f"response in_out_users {len(response)}")
    return response.values()