# Generated by Django 4.1.7 on 2023-03-24 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_class_description_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.class'),
        ),
    ]
