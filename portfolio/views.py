from django.shortcuts import render
from .models import Project, ProfilePhoto, ProfileText

# Create your views here.
def home(request):
    projects = Project.objects.all()
    profile_text = ProfileText.objects.first()
    slideshow_photos = ProfilePhoto.objects.filter(show_in_slideshow=True).order_by('slideshow_order')
    return render(request, 'portfolio/home.html',
                  {'projects':projects,
                   'slideshow_photos': slideshow_photos,
                   'profile_text': profile_text})
