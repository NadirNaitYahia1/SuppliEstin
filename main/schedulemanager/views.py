from django.shortcuts import render
from .models import AnneeUniv, AdminMois
import calendar
from datetime import datetime, timedelta

# Create your views here.

def index(request):
    
    return render(request, 'index.html')


# ____________________________________________________________________________________________________________________________________

def set_months(request,year):
    annee_univ = AnneeUniv.objects.get(annee_univ=year)
    registered_months = AdminMois.objects.filter(anneeUniv=annee_univ)
    is_new = False
    months = []
    if len(registered_months) == 0:
        is_new = True
        current_date = annee_univ.debut
        while current_date < annee_univ.fin:
            months.append((current_date.month,calendar.month_abbr[current_date.month]))
            current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
    else:
        months = registered_months
    context = {
        'year': year,
        'months': months,
        'is_new': is_new
    }

    return render(request, 'set_months.html',context)

# ____________________________________________________________________________________________________________________________________

def fiche_heurs_supps(request, type,year, month):
    context = {
        'type': type, # 'vacataires' or 'permanent
        'year': year,
        'month': month
    
    }
    return render(request, 'fiche_heurs_supps.html', context)

def fiche_heurs_supps_enseignant(request, enseignant, year, month):
    return render(request, 'fiche_heurs_supps_enseignant.html')