from typing import Optional
from .models import Campaign

def record_ad_impression(campaign_id: int, cost: float) -> Optional[bool]:
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        if campaign.is_active and campaign.brand.is_active:
            campaign.record_spend(cost)
            return True
        return False
    except Campaign.DoesNotExist:
        return None