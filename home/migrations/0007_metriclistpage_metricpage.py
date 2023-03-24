# Generated by Django 4.1.7 on 2023-03-24 11:49

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('home', '0006_alter_class_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetricListPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Оценка эффективности',
                'verbose_name_plural': 'Оценки эффективности',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='MetricPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Страница метрики',
                'verbose_name_plural': 'Страницы метрик',
            },
            bases=('wagtailcore.page',),
        ),
    ]
