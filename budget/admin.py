from django.contrib import admin
from .models import Brand, Campaign, SpendLog, DaypartingSchedule

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_budget', 'monthly_budget', 
                   'current_daily_spend', 'current_monthly_spend', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'daily_budget', 
                   'current_daily_spend', 'is_active')
    list_filter = ('is_active', 'brand')
    search_fields = ('name', 'brand__name')

@admin.register(SpendLog)
class SpendLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'amount', 'timestamp', 'spend_type')
    list_filter = ('spend_type', 'timestamp')
    search_fields = ('campaign__name',)

@admin.register(DaypartingSchedule)
class DaypartingScheduleAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'start_time', 'end_time', 'days_of_week')
    search_fields = ('campaign__name',)