from django.db import models

class ContactConfig(models.Model):
    email_to = models.EmailField()
    telegram_bot_token = models.CharField(max_length=150)
    telegram_chat_id = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Contact Settings"