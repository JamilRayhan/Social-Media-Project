# Generated by Django 4.1.1 on 2023-06-08 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Post', '0008_alter_comment_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-post__upload_date', '-timestamp']},
        ),
    ]