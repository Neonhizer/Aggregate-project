# Generated by Django 4.2.5 on 2023-09-24 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20230911_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='short_description',
            field=models.CharField(default='N/A', max_length=500),
        ),
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]