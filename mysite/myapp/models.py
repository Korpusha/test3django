from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    purse = models.IntegerField(default=10000)


class Goods(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name


class BuyModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    interact_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-interact_date']

    def __str__(self):
        return f'Product: {self.good} || User: {self.user} || Amount: {self.amount} || Date: {self.interact_date}'


class ReturnModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(BuyModel, on_delete=models.CASCADE, null=True)
    interact_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-interact_date']

    def __str__(self):
        return f'{self.purchase}'


