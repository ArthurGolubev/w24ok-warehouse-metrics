import graphene
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from loguru import logger
from ..models import Prolongation, Transaction

class ProlongationsMutation(graphene.Mutation):
    class Arguments:
        warh = graphene.String()
        prolongations = graphene.List(
            graphene.List(graphene.String)
        )

    success = graphene.JSONString()
    
    @classmethod
    @login_required
    def mutate(cls, root, info, warh, prolongations):
        if not info.context.user.has_perm(f'main.can_upload_warh_{warh}'):
            logger.error(f'{info.context.user.has_perm(f"can_upload_warh_{warh}")=}')
            return GraphQLError('Permission denied')
        logger.info(f'{prolongations=}')
        for p in prolongations:
            Prolongation.objects.get_or_create(
                transact=Transaction.objects.get(cod=p[0]),
                reason = p[1]
            )

        return ProlongationsMutation(success={"success": "yes"})
