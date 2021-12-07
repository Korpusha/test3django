from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    purse = models.IntegerField(default=10000)


class Goods(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.name


class BuyModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    interact_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.good}_{self.user}'


class ReturnModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(BuyModel, on_delete=models.CASCADE)
    interact_date = models.DateTimeField(auto_now_add=True, null=True)
