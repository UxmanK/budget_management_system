from django.core.management.base import BaseCommand
from budget.models import Brand, Campaign, DaypartingSchedule
import pytz
from datetime import time

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")
        
        # Clear existing data
        Brand.objects.all().delete()
        
        # Create brands
        brand1 = Brand.objects.create(
            name="Nike",
            daily_budget=10000,
            monthly_budget=300000,
            is_active=True
        )
        
        # Create campaigns (remaining code same as migration)
        
        self.stdout.write(self.style.SUCCESS("Successfully seeded data"))