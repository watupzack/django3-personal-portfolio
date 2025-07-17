from django.contrib import admin
from .models import ContactConfig

@admin.register(ContactConfig)
class ContactConfigAdmin(admin.ModelAdmin):
    list_display = ('email_to', 'telegram_chat_id', 'updated_at')
