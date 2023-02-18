import graphene
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from loguru import logger
from ..models import ReductionFine, Transaction

class ReductionFineMutation(graphene.Mutation):
    class Arguments:
        warh = graphene.String()
        decreases = graphene.List(
            graphene.List(graphene.String)
        )

    success = graphene.JSONString()
    
    @classmethod
    @login_required
    def mutate(cls, root, info, warh, decreases):
        if not info.context.user.has_perm(f'main.can_upload_warh_{warh}'):
            logger.error(f'{info.context.user.has_perm(f"can_upload_warh_{warh}")=}')
            return GraphQLError('Permission denied')
        for d in decreases:
            ReductionFine.objects.get_or_create(
                transact=Transaction.objects.get(cod=d[0]),
                amount = d[1]
            )


        return ReductionFineMutation(success={"success": "yes"})
