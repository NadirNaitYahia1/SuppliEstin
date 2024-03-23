from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def set_months(request,year):
    context = {
        'year': year
    }
    return render(request, 'set_months.html',context)

def fiche_heurs_supps(request, year, month):
    context = {
        'year': year,
        'month': month
    
    }
    return render(request, 'fiche_heurs_supps.html', context)

def fiche_heurs_supps_enseignant(request, enseignant, year, month):
    return render(request, 'fiche_heurs_supps_enseignant.html')