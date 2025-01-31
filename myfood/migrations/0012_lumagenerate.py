# Generated by Django 5.0.7 on 2024-07-21 21:13

import myfood.storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfood', '0011_imageupload_alter_openaiimagegeneration_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='LumaGenerate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('s3_file', models.FileField(storage=myfood.storages.S3Storage, upload_to='')),
                ('access_token', models.CharField(max_length=1024)),
                ('luma_id', models.CharField(blank=True, max_length=1024, null=True)),
                ('luma_presigned_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('luma_image_public_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('luma_video_public_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('result_video', models.FileField(blank=True, null=True, storage=myfood.storages.S3Storage, upload_to='')),
            ],
        ),
    ]
