from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')


# ______________________________________________________________________________________________________________________
def set_months(request,year):
    context = {
        'year': year
    }
    
    return render(request, 'set_months.html',context)

def fiche_heurs_supps(request, type,year, month):
    context = {
        'type': type, # 'vacataires' or 'permanent
        'year': year,
        'month': month
    
    }
    return render(request, 'fiche_heurs_supps.html', context)

def fiche_heurs_supps_enseignant(request, enseignant, year, month):
    return render(request, 'fiche_heurs_supps_enseignant.html')