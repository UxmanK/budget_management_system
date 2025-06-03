from celery import shared_task
from typing import Optional
from datetime import datetime, time
from django.utils import timezone
from .models import Campaign, Brand

@shared_task
def check_all_campaign_budgets(campaign_id: int) -> None:
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        brand = campaign.brand
        
        # Check if campaign needs to be deactivated
        if (campaign.current_daily_spend >= campaign.daily_budget or
            not brand.has_daily_budget() or
            not brand.has_monthly_budget()):
            campaign.is_active = False
            campaign.save()
            
    except Campaign.DoesNotExist:
        pass

@shared_task
def daily_reset() -> None:
    # Reset all daily spends
    Brand.objects.all().update(current_daily_spend=0)
    Campaign.objects.all().update(current_daily_spend=0)
    
    # Reactivate eligible campaigns
    for brand in Brand.objects.filter(is_active=True):
        if brand.has_daily_budget() and brand.has_monthly_budget():
            brand.campaigns.filter(is_active=False).update(is_active=True)
    
    # Check dayparting for all campaigns
    check_dayparting.delay()

@shared_task
def monthly_reset() -> None:
    # Reset all monthly spends
    Brand.objects.all().update(current_monthly_spend=0)
    
    # Reactivate all brands and their campaigns
    Brand.objects.update(is_active=True)
    Campaign.objects.update(is_active=True)
    
    # Check dayparting for all campaigns
    check_dayparting.delay()

@shared_task
def check_dayparting() -> None:
    now = timezone.now()
    current_time = now.time()
    current_weekday = now.weekday()
    
    # Get all campaigns with dayparting schedules
    campaigns = Campaign.objects.filter(
        dayparting_schedules__isnull=False
    ).distinct()
    
    for campaign in campaigns:
        should_be_active = campaign.should_be_active()
        if campaign.is_active != should_be_active:
            campaign.is_active = should_be_active
            campaign.save()