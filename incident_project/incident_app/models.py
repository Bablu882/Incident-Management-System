from django.db import models
from django.contrib.auth.models import User
import datetime
import random

class Incident(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]
    
    incident_id = models.CharField(max_length=15, unique=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    incident_details = models.TextField()
    reporter_name=models.CharField(max_length=50)
    reported_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    incident_status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    
    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = self.generate_incident_id()
        super().save(*args, **kwargs)
    
    def generate_incident_id(self):
        current_year = datetime.datetime.now().year
        incident_id = f'RMG{random.randint(10000, 99999)}{current_year}'

        # Check if incident ID already exists
        while Incident.objects.filter(incident_id=incident_id).exists():
            incident_id = f'RMG{random.randint(10000, 99999)}{current_year}'

        return incident_id