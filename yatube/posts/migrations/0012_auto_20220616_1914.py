# Generated by Django 2.2.16 on 2022-06-16 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20220615_1145'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('author', 'user'), name='unique_following'),
        ),
    ]
