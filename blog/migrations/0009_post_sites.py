# Generated by Django 2.2.3 on 2019-09-29 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_auto_20190929_2113'),
        ('blog', '0008_auto_20190926_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sites',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]