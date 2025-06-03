# Budget Management System

A Django + Celery application for tracking advertising budgets with automated campaign controls.

## Features

- Daily/monthly budget tracking
- Automatic campaign activation/deactivation
- Dayparting (time-based scheduling)
- Redis-backed task queue
- PostgreSQL database
- Dockerized environment

## Prerequisites

- Docker Desktop
- Python 3.9+
- Git

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/uxmanK/budget_management_system.git
cd budget_management_system
```
### 2. Build and run the Docker containers
```bash
docker-compose build
docker-compose up -d
```
### 3. Verify the containers are running
```bash
docker-compose ps
```
### 3. Initialize the database
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
## 4. Database Seeding
The system comes with sample test data:

```bash
# Run migrations (includes seed data)
docker-compose exec web python manage.py migrate

### 4. Access Services
Service	URL	Credentials
Django Admin	http://localhost:8000/admin	Your superuser creds
Redis Commander	http://localhost:8081	None
Flower Dashboard	http://localhost:5555	None