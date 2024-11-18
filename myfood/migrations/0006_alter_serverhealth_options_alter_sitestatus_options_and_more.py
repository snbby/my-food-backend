# Generated by Django 5.0.7 on 2024-07-20 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfood', '0005_serverhealth_alter_openaiimagegeneration_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serverhealth',
            options={'verbose_name_plural': 'Server Health'},
        ),
        migrations.AlterModelOptions(
            name='sitestatus',
            options={'verbose_name_plural': 'Site Status'},
        ),
        migrations.AddField(
            model_name='serverhealth',
            name='min_10_avg_cpu_load_perc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='serverhealth',
            name='min_15_avg_cpu_load_perc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='serverhealth',
            name='min_5_avg_cpu_load_perc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
