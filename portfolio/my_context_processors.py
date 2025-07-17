from .models import CV, Portfolio

def latest_cv(request):
    latest = CV.objects.order_by('-uploaded_at').first()
    return {'latest_cv': latest}

def latest_portfolio(request):
    latest = Portfolio.objects.order_by('-uploaded_at').first()
    return {'latest_portfolio': latest}

