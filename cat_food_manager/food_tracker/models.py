from django.db import models
from django.utils.timezone import now
class FoodStock(models.Model):
    quantity = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.quantity} kg of cat food is available"

class FeedingLog(models.Model):
    action = models.CharField(max_length=10)
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.action} {self.amount}kg at {self.timestamp}"