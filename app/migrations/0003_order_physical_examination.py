# Generated by Django 4.0.6 on 2023-03-10 12:23

from django.db import migrations
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_department_name_alter_medicine_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='physical_examination',
            field=django_jsonform.models.fields.JSONField(blank=True, null=True, verbose_name='体检指标'),
        ),
    ]