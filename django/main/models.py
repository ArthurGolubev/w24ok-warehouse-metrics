from datetime import datetime


from datetime import datetime
from django.db import models
# from django.contrib.auth import User

# Create your models here.

class Warehouse(models.Model):
    name                    = models.CharField(max_length=50, null=True, blank=True)
    short_name              = models.CharField(max_length=10, default='YP')
    created_datetime        = models.DateTimeField(auto_now_add=True)
    start_date_download     = models.DateField(null=True, blank=True, verbose_name="Начальная дата для скачивания архивных данных")
    last_download_date      = models.DateField(null=True, blank=True, verbose_name="Последняя дата уже скачанных архивных данных")
    end_date_download       = models.DateField(null=True, blank=True, verbose_name="Конечная дата для скачивания архивных данных")
    download_status         = models.BooleanField(default=False, verbose_name="Статус загрузки архивных данных (запустить/остановить)")
    def __str__(self) -> str:
        return self.short_name

class Username(models.Model):
    username = models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.username

class Organizer(models.Model):
    username = models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.username

class Transaction(models.Model):
    warh                    = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    cod                     = models.CharField(max_length=150, unique_for_date="datetime")
    datetime                = models.DateTimeField()
    target                  = models.CharField(max_length=220)
    org                     = models.ForeignKey(Organizer, null=True, on_delete=models.CASCADE)
    purchase_title          = models.CharField(null=True, max_length=1000)
    user                    = models.ForeignKey(Username, on_delete=models.CASCADE)
    fare                    = models.IntegerField()
    paid                    = models.IntegerField()
    paid_by_card            = models.BooleanField(default=False)
    fine                    = models.IntegerField()
    def __str__(self) -> str:
        return self.user.username

class ReductionFine(models.Model):
    transact    = models.ForeignKey(Transaction, unique=True, on_delete=models.CASCADE)
    amount      = models.IntegerField()
    def __str__(self):
        return self.transact.user.username

class Prolongation(models.Model):
    transact    = models.ForeignKey(Transaction, unique=True, on_delete=models.CASCADE)
    reason      = models.TextField()
    def __str__(self):
        return self.transact.user.username
