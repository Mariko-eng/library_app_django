# Generated by Django 3.2.20 on 2023-08-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school_id_no',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]