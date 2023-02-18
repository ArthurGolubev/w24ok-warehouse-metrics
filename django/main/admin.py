from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Warehouse, Username, Organizer, Transaction, ReductionFine, Prolongation
# Register your models here.

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_datetime', 'id')
    list_display = ('short_name', 'name',)

@admin.register(Username)
class UsernameAdmin(admin.ModelAdmin):
    pass

@admin.register(Prolongation)
class ProlongationAdmin(admin.ModelAdmin):
    raw_id_fields = ["transact",]

    # readonly_fields = ('transact_purchase_title', 'transact_datetime', 'transact', 'id')
    pass

    def transact_purchase_title(self, obj):
        return obj.transact.purchase_title

    def transact_datetime(self, obj):
        return obj.transact.datetime

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime')
    list_filter = ('warh',)

@admin.register(ReductionFine)
class ReductionFineAdmin(admin.ModelAdmin):
    raw_id_fields = ["transact",]
    # pass

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass