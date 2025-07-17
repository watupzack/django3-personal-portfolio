# from django.contrib import admin
# from .models import Project

# admin.site.register(Project)

from django.contrib import admin
from .models import Project, CV, Portfolio, ProfilePhoto, ProfileText

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')  # Show in list view
    fields = ('title', 'description', 'image', 'url', 'created')  # Editable in form

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

@admin.register(ProfilePhoto)
class ProfilePhotoAdmin(admin.ModelAdmin):
    list_display = ('version', 'uploaded_at', 'show_in_slideshow', 'slideshow_order')
    list_editable = ('show_in_slideshow', 'slideshow_order')
    ordering = ('slideshow_order',)

admin.site.register(ProfileText)