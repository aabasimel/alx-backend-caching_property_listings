from django.db import models

class Property(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    prince=models.DecimalField(decimal_places=2,max_digits=10)
    location=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

