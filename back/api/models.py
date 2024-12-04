from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
# models.py
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    REQUIRED_FIELDS = ['nom', 'prenom']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email





class Client(models.Model):
   
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    adresse = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='client_images/', null=True, blank=True)
def __str__(self):
  return f"{self.nom} {self.prenom}"
@property
def benefices(self):
        from .models import Course  
        return Course.objects.filter(client=self).aggregate(total_tarif=Sum('tarif')).get('total_tarif', 0) or 0








class Chauffeur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15)
    adresse = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chauffeur_images/', null=True, blank=True)
    documentation = models.FileField(upload_to='chauffeur_docs/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"




class Vehicule(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('en attente', 'En Attente'),
        ('en parking', 'En Parking'),
    ]
    reference = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en attente')
    image = models.ImageField(upload_to='vehicule_images/', null=True, blank=True)

    def __str__(self):
        return f"Véhicule {self.reference} - {self.get_status_display()}"


class Course(models.Model):
    STATUS_CHOICES = [
        ('en cours', 'En Cours'),
        ('terminée', 'Terminée'),
    ]
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE, related_name='courses')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='courses')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en cours')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    tarif = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        return None

    def __str__(self):
        return f"Course {self.id} - {self.status}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chauffeur', 'client', 'start_time'], name='unique_course_per_chauffeur_client')
        ]
