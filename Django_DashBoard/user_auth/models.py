from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Custom User Model
class User(AbstractUser):
    PROFILE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    speciality = (
        ('Neuro', 'Neuro'),
        ('Cardio', 'Cardio'),
        ('Pediatrics', 'Pediatrics'),
    )
    speciality = models.CharField(max_length=15, choices=speciality, default=None, null=True, blank=True)
    profile_type = models.CharField(max_length=10, choices=PROFILE_CHOICES, default = 'patient')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.username



# Category Model

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Blog Model

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    blog_picture = models.ImageField(upload_to='blog_pics/' , default='user_auth/default_images/default-blog-image.png')
    content = models.TextField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        words = self.content.split()[:15]
        return ' '.join(words)

        

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', default=None, null=True)
    chosen_date = models.DateField(default=None, blank=True, null=True)
    chosen_time = models.TimeField(default=None, blank=True, null=True)
    end_time = models.TimeField(default=datetime.time(12, 45),blank=True) 
    speciality = (
        ('Neuro', 'Neuro'),
        ('Cardio', 'Cardio'),
        ('Pediatrics', 'Pediatrics'),
    )
    google_url = models.URLField(max_length=300)
    required_speciality = models.CharField(max_length=15, choices=speciality, default="Neuro")
    patient_docs    = models.FileField(upload_to="patient-docs",default=None, blank=True)
    patient_desc    = models.TextField(default=None)
    meeting_url = models.URLField(max_length=300,blank=True,default=None,null=True)