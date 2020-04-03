# Generated by Django 3.0.4 on 2020-03-25 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guard',
            fields=[
                ('employee_id', models.CharField(max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('employee_id', models.CharField(max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='FloorPass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_ids', models.TextField()),
                ('remarks', models.TextField()),
                ('time_in', models.DateTimeField()),
                ('time_out', models.DateTimeField()),
                ('guard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineFloorPass.Guard')),
                ('supervisor',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineFloorPass.Supervisor')),
            ],
        ),
    ]