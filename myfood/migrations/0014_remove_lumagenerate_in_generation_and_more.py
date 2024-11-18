# Generated by Django 5.0.7 on 2024-07-22 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfood', '0013_lumagenerate_in_generation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lumagenerate',
            name='in_generation',
        ),
        migrations.AddField(
            model_name='lumagenerate',
            name='status',
            field=models.CharField(blank=True, choices=[('initial', 'initial'), ('generated_presign_url', 'generated_presign_url'), ('uploaded_image', 'uploaded_image'), ('is_generating', 'is_generating'), ('finished', 'finished')], default='initial'),
        ),
    ]
