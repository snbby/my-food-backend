# Generated by Django 5.0.7 on 2024-07-25 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfood', '0017_rename_image_link_modelopenaiimagegeneration_openai_temp_image_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelopenaiimagegeneration',
            name='size',
        ),
        migrations.AddField(
            model_name='modelopenaiimagegeneration',
            name='image_resolution',
            field=models.CharField(choices=[('s256x256', '256x256'), ('s512x512', '512x512'), ('s1024x1024', '1024x1024'), ('s1792x1024', '1792x1024')], default='256x256', help_text='If Dalle3-E model is used the resolution can be only 1024x1024', max_length=32),
        ),
    ]
