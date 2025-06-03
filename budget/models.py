from django.db import models
from django.core.validators import MinValueValidator
from typing import List, Dict, Optional, Literal
from django.utils import timezone
from datetime import time

class Brand(models.Model):
    name = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    current_daily_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_monthly_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name
    
    def has_daily_budget(self) -> bool:
        return self.current_daily_spend < self.daily_budget
    
    def has_monthly_budget(self) -> bool:
        return self.current_monthly_spend < self.monthly_budget
    
    def can_activate_campaigns(self) -> bool:
        return self.is_active and self.has_daily_budget() and self.has_monthly_budget()

class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    current_daily_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.brand})"
    
    def record_spend(self, amount: float) -> None:
        from .tasks import check_all_campaign_budgets
        
        self.current_daily_spend += amount
        self.brand.current_daily_spend += amount
        self.brand.current_monthly_spend += amount
        self.save()
        self.brand.save()
        
        SpendLog.objects.create(
            campaign=self,
            amount=amount,
            spend_type='daily'
        )
        
        check_all_campaign_budgets.delay(self.id)
    
    def should_be_active(self) -> bool:
        now = timezone.now()
        in_schedule = self.dayparting_schedules.filter(
            start_time__lte=now.time(),
            end_time__gte=now.time(),
            days_of_week__contains=now.weekday()
        ).exists()
        
        return (
            in_schedule and
            self.is_active and
            self.brand.can_activate_campaigns() and
            self.current_daily_spend < self.daily_budget
        )

class SpendLog(models.Model):
    SPEND_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='spend_logs')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    spend_type = models.CharField(max_length=10, choices=SPEND_TYPE_CHOICES)
    
    def __str__(self) -> str:
        return f"{self.amount} for {self.campaign} ({self.spend_type})"

class DaypartingSchedule(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='dayparting_schedules')
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.JSONField()  # Stores list of weekdays (0-6)
    
    def __str__(self) -> str:
        return f"{self.campaign}: {self.start_time}-{self.end_time} on days {self.days_of_week}"