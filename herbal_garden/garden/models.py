from django.db import models

class Plant(models.Model):
    CATEGORY_CHOICES = [
        ('immunity', 'Immunity Boosting Plants'),
        ('medicinal_herbs', 'Medicinal Herbs'),
        ('digestion', 'Digestive Health Plants'),
        ('respiratory', 'Respiratory Health Plants'),
        ('skin', 'Skin Care Plants'),
        ('hair', 'Hair Care Plants'),
        ('anti_inflammatory', 'Anti-inflammatory Plants'),
        ('stress', 'Stress Relief Plants'),
        ('trees', 'Ayurvedic Trees'),
        ('sacred', 'Sacred Plants'),
        ('kitchen', 'Kitchen Medicinal Herbs'),
        ('womens_health', "Women's Health Plants"),
        ('mens_health', "Men's Health Plants"),
        ('diabetes', 'Diabetes Support Plants'),
        ('heart', 'Heart Health Plants'),
        ('detox', 'Detoxifying Plants'),
        ('aromatic', 'Aromatic Medicinal Plants'),
        ('traditional', 'Traditional Indian Medicinal Plants'),
        ('rare', 'Rare Ayurvedic Plants'),
    ]

    # Core Identifiers
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150)
    sanskrit_name = models.CharField(max_length=150, blank=True, null=True)
    telugu_name = models.CharField(max_length=150, blank=True, null=True)
    hindi_name = models.CharField(max_length=150, blank=True, null=True)
    family = models.CharField(max_length=150, blank=True, null=True)
    native_region = models.CharField(max_length=150, blank=True, null=True)
    
    # Original Fields
    uses = models.TextField()
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='medicinal_herbs')
    is_user_added = models.BooleanField(default=False)

    # Images
    image_url = models.URLField(max_length=500, blank=True, null=True)
    leaf_image_url = models.URLField(max_length=500, blank=True, null=True)
    flower_image_url = models.URLField(max_length=500, blank=True, null=True)
    fruit_image_url = models.URLField(max_length=500, blank=True, null=True)

    # Ayurvedic Info
    ayurvedic_classification = models.CharField(max_length=250, blank=True, null=True) # e.g. Rasayana, Deepana
    ayurvedic_properties = models.TextField(blank=True, null=True) # Rasa, Guna, Virya, Vipaka
    traditional_uses = models.TextField(blank=True, null=True)
    modern_uses = models.TextField(blank=True, null=True)

    # Dosha Scores (0 to 100)
    dosha_vata = models.IntegerField(default=50)
    dosha_pitta = models.IntegerField(default=50)
    dosha_kapha = models.IntegerField(default=50)

    # Medicinal Strength (0 to 100)
    strength_immunity = models.IntegerField(default=50)
    strength_anti_inflammatory = models.IntegerField(default=50)
    strength_digestive = models.IntegerField(default=50)
    strength_respiratory = models.IntegerField(default=50)

    # Cultivation Info
    climate_requirements = models.TextField(blank=True, null=True)
    soil_requirements = models.TextField(blank=True, null=True)
    water_requirements = models.TextField(blank=True, null=True)
    sunlight_requirements = models.TextField(blank=True, null=True)
    growth_conditions = models.TextField(blank=True, null=True)

    # Safety Info
    precautions = models.TextField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)
    contraindications = models.TextField(blank=True, null=True)
    recommended_usage = models.TextField(blank=True, null=True)

    # Historical & Cultural Info
    historical_significance = models.TextField(blank=True, null=True)
    ayurvedic_importance = models.TextField(blank=True, null=True)
    cultural_relevance = models.TextField(blank=True, null=True)

    @property
    def vata_pacifying(self):
        return 100 - self.dosha_vata

    @property
    def pitta_pacifying(self):
        return 100 - self.dosha_pitta

    @property
    def kapha_pacifying(self):
        return 100 - self.dosha_kapha

    def __str__(self):
        return self.name