from django.db import models

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,blank=False,null=False)
    description = models.TextField(default='NA',blank=False,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0,blank=False,null=False)
    stock_quantity = models.PositiveIntegerField(default=0,blank=False,null=False)
    version = models.PositiveIntegerField(default=1)  # field for optimistic locking
    
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, default='SYSTEM')
    updation_date = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=60,default='SYSTEM')

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['id']), # we can add more fields here for indexing when we have more unique fields
        ]
