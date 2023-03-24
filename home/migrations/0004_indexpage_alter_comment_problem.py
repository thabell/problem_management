# Generated by Django 4.1.7 on 2023-03-24 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('home', '0003_class_metric_priority_problem_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главные страницы',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='comment',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='home.problem'),
        ),
    ]