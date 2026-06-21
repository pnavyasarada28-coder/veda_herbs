import csv
from garden.models import Plant

def get_category(uses):
    uses = uses.lower()

    if 'immunity' in uses or 'cold' in uses:
        return 'immunity'
    elif 'skin' in uses or 'wound' in uses:
        return 'skin'
    elif 'digestion' in uses or 'gas' in uses:
        return 'digestion'
    elif 'respiratory' in uses or 'cough' in uses:
        return 'respiratory'
    elif 'stress' in uses or 'sleep' in uses:
        return 'stress'
    else:
        return 'general'

with open('plants.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        category = get_category(row['uses'])

        Plant.objects.create(
            name=row['name'],
            scientific_name=row['scientific_name'],
            uses=row['uses'],
            description=row['description'],
            category=category   
        )

print("✅ Data Loaded with Categories!")