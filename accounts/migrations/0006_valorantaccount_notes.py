# Generated by Django 4.0.4 on 2023-09-04 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_valorantaccount_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='valorantaccount',
            name='notes',
            field=models.CharField(blank=True, help_text='Notes', max_length=2000, null=True),
        ),
    ]
