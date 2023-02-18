from promise import Promise
from promise.dataloader import DataLoader
from ..models import Username

class UserLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # print(f'my {keys}')
        users = {user.id: user for user in Username.objects.filter(id__in=keys)}
        # print(f'new1 ->{users}')
        # print(f'new2 ->{keys}')
        return Promise.resolve([users.get(user_id) for user_id in keys])