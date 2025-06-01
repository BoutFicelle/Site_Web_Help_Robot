# errors/views.py
from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from .models import ErrorCodeFanuc

def home(request):
    context = {
        'page_title': _('Home'),
        'fanuc_status': _('Fanuc error search is functional.'),
        'abb_status': _('ABB support is under development.'),
    }
    return render(request, 'home.html', context)

def fanuc_search(request):
    query = request.GET.get('q', '')
    # Nouveau : langue spécifique pour les résultats d'erreur
    error_language = request.GET.get('error_lang', 'en')  # par défaut anglais
    
    results = []
    
    if query:
        results = ErrorCodeFanuc.objects.filter(
            Q(code__icontains=query) | 
            Q(title__icontains=query) |
            Q(cause_en__icontains=query) |
            Q(cause_fr__icontains=query)
        )[:10]  # Limiter à 10 résultats
    
    context = {
        'query': query,
        'results': results,
        'current_language': get_language(),  # Langue du site
        'error_language': error_language,    # Langue des erreurs
        'page_title': _('Fanuc Error Search'),
    }
    return render(request, 'errors/fanuc_search.html', context)

def abb_coming_soon(request):
    context = {
        'brand': 'ABB',
        'message': _('ABB error search is under development.'),
        'page_title': _('ABB Errors'),
    }
    return render(request, 'coming_soon.html', context)

def kuka_coming_soon(request):
    context = {
        'brand': 'Kuka',
        'message': _('Kuka error search is under development.'),
        'page_title': _('Kuka Errors'),
    }
    return render(request, 'coming_soon.html', context)