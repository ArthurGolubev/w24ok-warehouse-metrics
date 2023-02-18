from loguru import logger
import graphene
from ..models import Warehouse, Transaction, Username, Organizer, ReductionFine
from datetime import datetime
from graphql_jwt.decorators import login_required
from graphql import GraphQLError


class TransactionsMutation(graphene.Mutation):
    class Arguments:
        warh = graphene.String()
        clear_data = graphene.List(
            graphene.List(graphene.String)
        )

    success = graphene.JSONString()
    
    @classmethod
    @login_required
    def mutate(cls, root, info, warh, clear_data):
        if not info.context.user.has_perm(f'main.can_upload_warh_{warh}'):
            logger.error(f'{info.context.user.has_perm(f"can_upload_warh_{warh}")=}')
            return GraphQLError('Permission denied')
        wh = Warehouse.objects.get_or_create(short_name=warh)[0]

        for tr in clear_data:
            try:
                f7 = float(tr[7])
            except ValueError:
                f7 = 0
            except TypeError:
                f7 = 0

            # Обработка повреждённых данных
            if tr[3] == None:
                tr[3] = 'X'
            if tr[4] == None:
                tr[4] = 'X'
            if tr[5] == None:
                tr[5] = 'X'

            if tr[8] == 'нет':
                pbc = False
            else:
                pbc = True
            Transaction.objects.get_or_create(
                warh=wh,
                cod=tr[0],
                datetime=datetime.strptime(tr[1]+'+0700', '%Y.%m.%d %H:%M:%S%z'),
                target=tr[2],
                org=Organizer.objects.get_or_create(username=tr[3])[0],
                purchase_title=tr[4],
                user=Username.objects.get_or_create(username=tr[5])[0],
                fare=float(tr[6].replace(',', '.')),
                paid=f7,
                paid_by_card=pbc,
                fine=float(tr[9].replace(',', '.'))
            )
        
        return TransactionsMutation(success={"success": "yes"})