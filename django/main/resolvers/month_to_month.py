import datetime
from loguru import logger
from ..models import Transaction, Warehouse
from calendar import monthrange
from django.core.cache import cache
from django.db.models import Count, Sum
from graphql import GraphQLError



def month_to_month(warh):
    response = cache.get(f'month_to_month_{warh}')
    warh = Warehouse.objects.get(short_name=warh)
    
    first =  Transaction.objects.filter(warh=warh).order_by('datetime').first()
    if first:
        first = first.datetime
    else:
        return GraphQLError(f'В базе данных нет транзакция склада {warh} чтобы взять first.datetime в in_out_users')
    last =  Transaction.objects.filter(warh=warh).order_by('datetime').last().datetime

    def month_year_iter(start_month, start_year, end_month, end_year):
        ym_start= 12*start_year + start_month - 1
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            yield y, m+1

    def calculate_payload(year, month):
        m = Transaction.objects.filter(warh=warh, datetime__year=year, datetime__month=month)
        unique_users = m.aggregate(Count('user', distinct=True))
        paid = m.aggregate(Sum('paid'))
        last_day = monthrange(year, month)[1]
        payload = {
                'date': datetime.date(year, month, last_day),
                'transactions': len(m),
                'unique_users': unique_users['user__count'],
                'paid': paid['paid__sum'],
            }
        return payload


    range_iterator = month_year_iter(1, first.year, last.month, last.year)
    response = {}
    result = []

    logger_message = []    
    for month in range_iterator:
        cache_month = cache.get(f'month_to_month_{warh}_{month[0]}_{month[1]}')
        if cache_month:
            '''Месяц есть в кэше'''
            logger_message.append(f'month_to_month {warh} case 1.2')
            response[month] = cache_month
        else:
            '''Месяца нет в кэше'''
            logger_message.append(f'month_to_month {warh} case 1.3')
            payload = calculate_payload(year=month[0], month=month[1])
            response[month] = payload
            cache.set(f'month_to_month_{warh}_{month[0]}_{month[1]}', payload, None)
    te = {}
    for r in response:
        lst = te.get(r[0])
        if not lst:
            te[r[0]] = [response[r], ]
        else:
            lst.append(response[r])
            te[r[0]] = lst
    
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
    cache.set(f'month_to_month_{warh}_{month[0]}_{month[1]}', payload, None)
    '''Обновление предыдущего месяца'''
    if month[1] != 1:
        payload = calculate_payload(year=month[0], month=month[1]-1)
        response[(month[0], month[1]-1)] = payload
        cache.set(f'month_to_month_{warh}_{month[0]}_{month[1]-1}', payload, None)

    for year in te:
        result.append({"date": year, "body": te[year]})
    # for o in result:
        # print(f'\n\n\n{o}\n\nlen body {len(o["body"])} ')
    logger.info('\n'.join(logger_message))
    return result


