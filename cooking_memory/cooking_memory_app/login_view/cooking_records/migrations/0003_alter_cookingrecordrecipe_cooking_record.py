# Generated by Django 5.1.3 on 2025-04-29 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooking_records', '0002_alter_cookingrecord_cooking_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookingrecordrecipe',
            name='cooking_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cooking_record_recipes', to='cooking_records.cookingrecord'),
        ),
    ]
