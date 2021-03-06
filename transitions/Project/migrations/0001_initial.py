# Generated by Django 3.1.1 on 2020-12-07 05:43

from django.db import migrations, models
import django.db.models.deletion
import transitions.Project.custom_fields.fields.MultiEmailFields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerEmail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('cc', transitions.Project.custom_fields.fields.MultiEmailFields.MultiEmailField(blank=True, default=None, null=True)),
                ('email', transitions.Project.custom_fields.fields.MultiEmailFields.MultiEmailField(default=[])),
                ('subject', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('body_type', models.CharField(choices=[('text', 'text'), ('html', 'html')], default='text', max_length=10)),
            ],
            options={
                'db_table': 'customer_email',
                'permissions': (('can_add_customer_email', 'Can add customer email'), ('can_view_customer_email', 'Can view customer email'), ('can_change_customer_email', 'Can change customer email'), ('can_delete_customer_email', 'Can delete customer email')),
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('path', models.CharField(db_column='path', max_length=10)),
                ('request_body', models.CharField(max_length=100)),
                ('response_body', models.CharField(max_length=100)),
                ('ip', models.CharField(db_column='ip', max_length=20)),
                ('request_date', models.DateTimeField()),
                ('response_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'log',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('type', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('templates', models.TextField()),
            ],
            options={
                'db_table': 'template',
                'permissions': (('can_add_customer_template', 'Can add customer template'), ('can_view_customer_template', 'Can view customer template'), ('can_change_customer_template', 'Can change customer template'), ('can_delete_customer_template', 'Can delete customer template')),
            },
        ),
        migrations.CreateModel(
            name='CustomerMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=15)),
                ('text', models.TextField()),
                ('kind', models.CharField(max_length=20)),
                ('type_template', models.ForeignKey(blank=True, db_column='type_template', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Project.template')),
            ],
            options={
                'db_table': 'customer_message',
                'permissions': (('can_add_customer_message', 'Can add customer message'), ('can_view_customer_message', 'Can view customer message'), ('can_change_customer_message', 'Can change customer message'), ('can_delete_customer_message', 'Can delete customer message')),
            },
        ),
    ]
