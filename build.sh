#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to the Django project directory where manage.py is located
cd herbal_garden

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Seed database with initial Ayurvedic plant data if database is empty
python seed_ayurveda.py
