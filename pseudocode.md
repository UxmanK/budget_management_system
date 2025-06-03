# Budget Management System Pseudocode

## System Overview
/*
This system manages advertising budgets at two levels:
1. Brand Level - Controls overall spending limits
2. Campaign Level - Controls individual campaign spending

Key Features:
- Hierarchical budget management
- Time-based campaign scheduling
- Automated budget monitoring
- Automatic resets and maintenance
*/

## Core Entities

### Brand Entity
/*
Represents an advertising brand that owns multiple campaigns.
Manages both daily and monthly budget constraints.
Provides budget availability checks for its campaigns.
*/

# Budget verification methods
Methods:
    # Checks if daily spending limit hasn't been reached
    has_daily_budget():
        return current_daily_spend < daily_budget
    
    # Checks if monthly spending limit hasn't been reached
    has_monthly_budget():
        return current_monthly_spend < monthly_budget
    
    # Comprehensive check for campaign activation eligibility
    can_activate_campaigns():
        return is_active AND has_daily_budget() AND has_monthly_budget()

### Campaign Entity
/*
Represents an individual advertising campaign.
Manages its own budget while respecting parent brand's constraints.
Integrates with scheduling system for time-based activation.
*/
# Core campaign operations
Methods:
    # Records spending and triggers budget checks
    record_spend(amount):
        # Update all spending counters
        current_daily_spend += amount
        brand.current_daily_spend += amount
        brand.current_monthly_spend += amount
        save changes to database
        
        # Log the transaction
        create spend log
        
        # Trigger asynchronous budget verification
        trigger async budget check
    
    # Determines if campaign should be running based on all constraints
    should_be_active():
        current_time = get current time
        # Check if current time falls within any scheduled periods
        schedule_active = check if current time falls within dayparting schedule
        
        # Comprehensive activation check
        return schedule_active AND
               is_active AND
               brand.can_activate_campaigns() AND
               current_daily_spend < daily_budget


### Supporting Entities

#### DaypartingSchedule
/*
Defines time windows when a campaign can be active.
Supports complex scheduling patterns across different days.
*/


#### SpendLog
/*
Tracks all spending activities for auditing and reporting.
Supports both daily and monthly spend tracking.
*/


## Business Logic

### Ad Impression Processing
/*
Handles incoming ad impressions and their associated costs.
Ensures proper budget tracking and campaign status verification.
*/

    # Verify campaign eligibility
    if campaign is active AND campaign's brand is active:
        record spend for campaign
        return success
    return failure
catch campaign not found:
    return null


### Automated Tasks

#### Budget Verification
/*
Asynchronous task that verifies budget compliance.
Deactivates campaigns that exceed their limits.
*/

    # Check all budget constraints
    if campaign daily spend >= campaign daily budget OR
       brand has no daily budget OR
       brand has no monthly budget:
           deactivate campaign
catch campaign not found:
    do nothing


#### Daily Maintenance
/*
Resets daily counters and reactivates eligible campaigns.
Runs at the start of each day.
*/

# Reactivate campaigns where possible
for each active brand:
    if brand has daily and monthly budget:
        reactivate all inactive campaigns

# Ensure proper scheduling
trigger check_dayparting task


#### Monthly Maintenance
/*
Resets monthly counters and reactivates all entities.
Runs at the start of each month.
*/

# Fresh start for all entities
activate all brands
activate all campaigns

# Ensure proper scheduling
trigger check_dayparting task


#### Schedule Enforcement
/*
Enforces dayparting schedules across all campaigns.
Ensures campaigns are only active during their scheduled times.
*/

# Process all scheduled campaigns
find all campaigns with dayparting schedules

for each campaign:
    check if campaign should be active
    if current active status != should_be_active:
        update campaign active status
