# Generated by Django 4.1.7 on 2023-06-01 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreApp', '0020_alter_business_postdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='postDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 1, 22, 14, 44, 14146), verbose_name='Дата публикации'),
        ),
    ]
