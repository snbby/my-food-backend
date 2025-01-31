# Generated by Django 5.0.7 on 2024-07-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfood', '0007_alter_serverhealth_min_10_avg_cpu_load_perc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverhealth',
            name='memory_free',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='serverhealth',
            name='memory_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
