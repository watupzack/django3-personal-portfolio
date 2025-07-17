from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio/images/')
    url = models.URLField(blank=True)
    created = models.DateTimeField(default=timezone.now)  # ✅ editable

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created'] # new projects first

class CV(models.Model):
    title = models.CharField(max_length=100, default="My CV")
    file = models.FileField(upload_to='portfolio/cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.uploaded_at.strftime('%Y-%m-%d')})"
    
class Portfolio(models.Model):
    title = models.CharField(max_length=100, default="My Portfolio")
    file = models.FileField(upload_to='portfolio/portfolios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.uploaded_at.strftime('%Y-%m-%d')})"
    
class ProfilePhoto(models.Model):
    image = models.ImageField(upload_to='portfolio/profile/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(editable=False, unique=True)
    show_in_slideshow = models.BooleanField(default=False)  # ✅ mark photo for slideshow
    slideshow_order = models.PositiveIntegerField(default=0)  # ✅ position in slideshow

    def save(self, *args, **kwargs):
        if not self.pk:
            last = ProfilePhoto.objects.order_by('-version').first()
            self.version = (last.version + 1) if last else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile photo v{self.version} ({self.uploaded_at.strftime('%Y-%m-%d')})"
    

class ProfileText(models.Model):
    title = models.CharField(max_length=200, default="Maxim Rezan | Engineering student")
    description = models.TextField(default="This site was created by me, using Django3 framework")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Profile Text"