from django.core.exceptions import ValidationError
from django import forms
import requests
from django.conf import settings 

MAX_UPLOAD_SIZE_MB = 24

from django.core.exceptions import ValidationError
from django import forms
import requests
from django.conf import settings 

MAX_UPLOAD_SIZE_MB = 24

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Changed from EmailInput to TextInput
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    attachment = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file and file.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise ValidationError("File size must be under 25 MB.")
        return file

    def clean(self):
        cleaned_data = super().clean()
        
        # Get the reCAPTCHA response from POST data
        token = self.data.get('g-recaptcha-response')
        if not token:
            raise forms.ValidationError("Please complete the CAPTCHA.")
        
        # Verify the CAPTCHA with Google
        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': token
            })
            result = r.json()
            print("CAPTCHA response:", result)  # For debugging
            
            if not result.get('success'):
                raise forms.ValidationError("Invalid CAPTCHA. Please try again.")
        except requests.RequestException:
            raise forms.ValidationError("CAPTCHA verification failed. Please try again.")
        
        return cleaned_data