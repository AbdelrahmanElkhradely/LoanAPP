# Generated by Django 4.2.3 on 2023-08-01 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LoanRestProject', '0011_alter_provider_options_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('trail', 'trail'),)},
        ),
    ]
