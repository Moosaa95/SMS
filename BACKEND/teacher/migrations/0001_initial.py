# Generated by Django 4.1.3 on 2022-11-15 10:28

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=15, region=None)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=10, unique=True)),
                ('department', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('post', models.CharField(max_length=100, null=True)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teacher.address')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('class_taken', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.class')),
                ('teacher', models.ManyToManyField(to='teacher.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='form_master',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.teacher'),
        ),
    ]