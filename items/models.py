from django.db import models
from django.conf import settings

class Laptop(models.Model):
    title = models.CharField(max_length=100, default="Default Laptop")
    model = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True) 
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="laptops"
    )

    def __str__(self):
        return self.title
