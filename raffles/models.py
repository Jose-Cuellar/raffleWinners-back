from django.db import models

# Create your models here.
class Raffle(models.Model):
    raffle_title = models.CharField(max_length=255)
    raffle_description = models.CharField(max_length=255)
    raffle_fecha = models.DateField()
    raffle_price = models.IntegerField()
    raffle_image = models.ImageField(upload_to='raffle_images/', null=True, blank=True)