from django.db import models

# Create your models here.
class Apartment(models.Model):
    # id = models.BigIntegerField(primary_key=True, unique=True)
    # price = models.FloatField(null=True, blank=True)
    min_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    cats = models.BooleanField(default=False, blank=True, null=True)
    dogs = models.BooleanField(default=False, blank=True, null=True)
    pet_policy_text = models.TextField(blank=True, null=True)
    # beds = models.IntegerField(null=True, blank=True)
    min_beds = models.FloatField(null=True, blank=True)
    max_beds = models.FloatField(null=True, blank=True)
    # baths = models.IntegerField(null=True, blank=True)
    min_baths = models.FloatField(null=True, blank=True)
    max_baths = models.FloatField(null=True, blank=True)
    house_type = models.CharField(max_length=100, null=True, blank=True)
    # sqft = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pictures = models.URLField()
    pictures1 = models.URLField()
    county = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.address}'