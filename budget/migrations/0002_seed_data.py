from django.db import migrations

def create_initial_data(apps, schema_editor):
    Brand = apps.get_model('budget', 'Brand')
    Campaign = apps.get_model('budget', 'Campaign')
    DaypartingSchedule = apps.get_model('budget', 'DaypartingSchedule')

    # Create brands
    brand1 = Brand.objects.create(
        name="Nike",
        daily_budget=10000,
        monthly_budget=300000,
        is_active=True
    )
    
    brand2 = Brand.objects.create(
        name="Adidas",
        daily_budget=8000,
        monthly_budget=240000,
        is_active=True
    )

    # Create campaigns
    campaign1 = Campaign.objects.create(
        brand=brand1,
        name="Summer Collection",
        daily_budget=5000,
        is_active=True
    )
    
    campaign2 = Campaign.objects.create(
        brand=brand1,
        name="Winter Collection",
        daily_budget=3000,
        is_active=True
    )

    # Create dayparting schedules
    DaypartingSchedule.objects.create(
        campaign=campaign1,
        start_time="09:00:00",
        end_time="17:00:00",
        days_of_week=[0, 1, 2, 3, 4]  # Monday-Friday
    )

class Migration(migrations.Migration):
    dependencies = [
        ('budget', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]