# Generated by Django 4.0.2 on 2022-03-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_alter_book_cover_art_bookprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='bookprogress',
            name='items',
            field=models.ManyToManyField(to='book.Item'),
        ),
    ]
