# Generated by Django 3.1.4 on 2020-12-10 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0006_return'),
    ]

    operations = [
        migrations.RenameField(
            model_name='return',
            old_name='book',
            new_name='returned_book',
        ),
    ]