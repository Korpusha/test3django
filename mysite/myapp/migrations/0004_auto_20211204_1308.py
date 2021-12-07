# Generated by Django 3.2.9 on 2021-12-04 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20211202_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='buymodel',
            name='good',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.goods'),
        ),
        migrations.AddField(
            model_name='buymodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
