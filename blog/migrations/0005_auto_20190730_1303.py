# Generated by Django 2.2.3 on 2019-07-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190730_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='readtime',
            field=models.IntegerField(editable=False),
        ),
    ]