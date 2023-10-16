# product_catalog/models.py
from django.db import models

class Product(models.Model):
    PID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return self.name
        """ The __str__ method is defined to return the name of the product 
        when you call str(product_instance)`, making it more readable when used in the
        Django admin interface or other places that need to display the product. """


