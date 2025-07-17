from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import ContactForm
from .models import ContactConfig
import requests

def contact_view(request):
    config = ContactConfig.objects.first()
    if not config:
        return render(request, 'contact/contact.html', {'error': 'Contact not configured.'})

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        
        print("Form data:", request.POST)  # Debug print
        print("Form is valid:", form.is_valid())  # Debug print
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            attachment = request.FILES.get('attachment')

            try:
                # 📨 Email to you
                body = f"From: {name} <{email}>\n\nMessage:\n{message}"
                email_msg = EmailMessage(subject, body, to=[config.email_to])

                if attachment:
                    attachment.seek(0)  # Ensure we're at the beginning of the file
                    email_msg.attach(attachment.name, attachment.read(), attachment.content_type)

                email_msg.send()

                # ✅ Confirmation reply to user
                confirmation_subject = "Thanks for contacting Maxim"
                confirmation_body = (
                    "Hi!\n\n"
                    "Thanks for reaching out\n"
                    "I will try to answer you ASAP!\n\n"
                    "Best regards,\n"
                    "Maxim's Bot"
                )
                
                confirmation = EmailMessage(confirmation_subject, confirmation_body, to=[email])
                confirmation.send()

                # 💬 Telegram text
                tg_msg = f"📬 New contact message:\n\n👤 {name}\n✉️ {email}\n📌 Subject: {subject}\n\n📝 {message}"
                tg_response = requests.post(
                    f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage",
                    data={'chat_id': config.telegram_chat_id, 'text': tg_msg}
                )
                print("Telegram message response:", tg_response.json())  # Debug print

                # 📎 Telegram file (with intro message)
                if attachment:
                    # Send intro message first
                    requests.post(
                        f'https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage',
                        data={
                            'chat_id': config.telegram_chat_id,
                            'text': "📎 This message also contains an attachment:"
                        }
                    )

                    # Then send the file
                    attachment.seek(0)  # Reset file pointer
                    file_response = requests.post(
                        f'https://api.telegram.org/bot{config.telegram_bot_token}/sendDocument',
                        data={'chat_id': config.telegram_chat_id},
                        files={'document': (attachment.name, attachment, attachment.content_type)}
                    )
                    print("Telegram file response:", file_response.json())  # Debug print

                messages.success(request, "Your message was sent successfully!")
                return redirect('contact')
                
            except Exception as e:
                print(f"Error sending message: {e}")  # Debug print
                messages.error(request, "There was an error sending your message. Please try again.")
                return render(request, 'contact/contact.html', {'form': form})
        else:
            # Form not valid: render template with errors
            print("Form errors:", form.errors)  # Debug print
            return render(request, 'contact/contact.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})