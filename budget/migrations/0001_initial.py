# Generated by Django 4.2.7 on 2025-05-29 20:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('daily_budget', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('monthly_budget', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('current_daily_spend', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('current_monthly_spend', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('daily_budget', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('current_daily_spend', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='budget.brand')),
            ],
        ),
        migrations.CreateModel(
            name='SpendLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('spend_type', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly')], max_length=10)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spend_logs', to='budget.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='DaypartingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('days_of_week', models.JSONField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dayparting_schedules', to='budget.campaign')),
            ],
        ),
    ]
