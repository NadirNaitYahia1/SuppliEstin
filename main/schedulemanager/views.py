from django.shortcuts import render
from .models import AnneeUniv, AdminMois,Enseignant,TabMois,Session
import calendar
from datetime import datetime, timedelta
from django.http import JsonResponse
import json

# Create your views here.

def index(request):
    
    return render(request, 'index.html')


# ____________________________________________________________________________________________________________________________________

def set_months(request,year):

    annee_univ = AnneeUniv.objects.get(annee_univ=year)
    if request.method == 'POST':
        data = json.loads(request.body)['data']
        updating = False
        for month in data:
            month_abbr_list = list(calendar.month_abbr)
            admin_mois_obj = AdminMois.objects.filter(anneeUniv=annee_univ, numMois=month_abbr_list.index(month['nomMois'])).first()
            if admin_mois_obj:
                admin_mois_obj.nbSemaines = month['nbSemaines']
                admin_mois_obj.save()
                updating = True
            else:
                AdminMois.objects.create(anneeUniv=annee_univ, nomMois=calendar.month_name[month_abbr_list.index(month['nomMois'])], nbSemaines=month['nbSemaines'], numMois=month_abbr_list.index(month['nomMois']))
        if updating:    
            return JsonResponse({'message': 'successfuly updated the months of the year '+str(year) + ' in the database'})
        else:
            return JsonResponse({'message': 'successfuly added the months of the year '+str(year) + ' in the database'})
    else:
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
            for month in registered_months:
                months.append((month.numMois, calendar.month_abbr[month.numMois],month.nbSemaines))
        context = {
            'year': year,
            'months': months,
            'is_new': is_new
        }
        return render(request, 'set_months.html',context)
# ____________________________________________________________________________________________________________________________________

def fiche_heurs_supps(request, type,year, month):
    print(type[0:1])
    if type[0:1].upper() in ['V','P']:
        profs = Enseignant.get_profs(type[0:1].upper())
    else:   
        return render(request, '404.html')
    
    for prof in profs:
        print(prof.grade)

    context = {
        'type': type, # 'vacataires' or 'permanent
        'year': year,
        'month': month,
        'profs': profs,
    
    }
    return render(request, 'fiche_heurs_supps.html', context)


# ____________________________________________________________________________________________________________________________________

def fiche_heurs_supps_enseignant(request, enseignant, year, month):
    enseignant = Enseignant.objects.get(id=enseignant)
    if not enseignant:
        return render(request, '404.html', {'message': 'Enseignant non trouvé'})
    admin_mois = AdminMois.objects.get(anneeUniv=AnneeUniv.objects.get(annee_univ=year), nomMois=month)
    if not admin_mois:
        return render(request, '404.html', {'message': 'Mois non trouvé'})
    year = AnneeUniv.objects.get(annee_univ=year)
    if not year:
        return render(request, '404.html', {'message': 'Année non trouvée'})
    tab_mois = TabMois.objects.filter(idEnseignat=enseignant, idMois=admin_mois)
    isNew = False
    semaines = []
    sessions = None
    if not tab_mois:
        isNew = True
    else:
        tab_mois = tab_mois.first()
        sessions = Session.objects.filter(idTabMois=tab_mois)
        if sessions:
            for i in range(1, admin_mois.nbSemaines+1):
                semaines.append({"numSemaine": i, "sessions": []})
                for session in sessions:
                    if session.numSemaine == i:
                        semaines[i-1]["sessions"].append((i, session.Date.strftime("%d/%m/%Y"), session.heurDebut.strftime("%H:%M"), session.heurFin.strftime("%H:%M"), session.typeSession, session.heurs, session.minutes))
    print("Semaines: ",semaines)


    context = {
        "nom_enseignant": enseignant.nom,
        "prenom_enseignant": enseignant.prenom,
        "grade_enseignant": enseignant.grade,
        "statut_enseignant": enseignant.statut,
        "semaines": semaines,   
        "is_editable": admin_mois.isEditable,
        "is_new": isNew,
        'year': year,
        'month': month,
        'nbSemaines': admin_mois.nbSemaines,
    }
    return render(request, 'fiche_heurs_supps_enseignant.html', context)

#Semaines:  [(1, datetime.date(2024, 1, 9), datetime.time(9, 30, 18), datetime.time(11, 0), 'Cours', 2, 0), 
#            (1, datetime.date(2024, 3, 26), datetime.time(11, 7, 5), datetime.time(11, 7, 8), 'TD', 1, 30)]

# Semaines:  [(1, datetime.date(2024, 1, 9), datetime.time(9, 30, 18), datetime.time(11, 0), 'Cours', 2, 0), 
#             (1, datetime.date(2024, 3, 26), datetime.time(11, 7, 5), datetime.time(11, 7, 8), 'TD', 1, 30), 
#             (2, datetime.date(2024, 3, 26), datetime.time(11, 8, 30), datetime.time(11, 8, 31), 'TP', 1, 8)]

# _________________ SESSION ______________________________
    # idEnseignat = models.ForeignKey('Enseignant', on_delete=models.CASCADE)
    # typeSession = models.CharField(max_length=20, choices=SESSION_TYPE, default='Cours', null=True)
    # idSeance    = models.AutoField(primary_key=True)
    # idTabMois   = models.ForeignKey('TabMois', on_delete=models.CASCADE)
    # numSemaine  = models.IntegerField(default=1)
    # Date        = models.DateField(null=True)
    # heurDebut  = models.TimeField(null=True)
    # heurFin    = models.TimeField(null=True)
    # heurs    = models.IntegerField()
    # minutes = models.IntegerField()

# ________________ ANNEEUNIV ______________________________
    # annee_univ=models.CharField(max_length=9, unique=True, primary_key=True)
    # debut=models.DateField()
    # fin=models.DateField()
    # encours=models.BooleanField(default=False,  blank=True)

# ________________ TABMOIS ______________________________
    # idTabMois    = models.AutoField(primary_key=True)
    # idEnseignat  = models.OneToOneField('Enseignant', on_delete=models.CASCADE)
    # nomMois      = models.CharField(max_length=20)
    # heursSupps   = models.IntegerField()
    # minutesSupps  = models.IntegerField()
    # idMois = models.ForeignKey('AdminMois', on_delete=models.CASCADE)
    # isEditable = models.BooleanField(default=True)

    # ________________ ADMINMOIS ______________________________
    # idMois = models.AutoField(primary_key=True)
    # numMois = models.IntegerField()
    # nomMois= models.CharField(max_length=20)
    # nbSemaines = models.IntegerField()
    # anneeUniv = models.ForeignKey('AnneeUniv', on_delete=models.CASCADE)
    # isEditable = models.BooleanField(default=True) 


    # ________________ ENSEIGNANT ______________________________
    # user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    # nom=models.CharField(max_length=50)
    # eps=models.CharField(max_length=50, null=True, blank=True)
    # prenom=models.CharField(max_length=50)
    # nom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom en arabe")
    # eps_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Eps en arabe")
    # prenom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom en arabe")
    # sexe=models.CharField(max_length=1, choices=SEXE, null=True, blank=True)
    # tel=models.CharField(max_length=15, null=True, blank=True)
    # grade=models.CharField(max_length=4, choices=GRADE, null=True, blank=True)
    # charge_statut=models.DecimalField(max_digits=5, decimal_places=2, default=288, blank=True)
    # situation=models.CharField(max_length=1, null=True, blank=True, choices=SITUATION, default='A')
    # statut=models.CharField(max_length=1, null=True, blank=True, choices = STATUT, default='P')
    # bureau=models.CharField(max_length=10, null=True, blank=True)
    # bal=models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Boîte aux lettres')
    # edt=models.TextField(null=True,blank=True, verbose_name="Emploi du temps")
    # webpage=models.URLField(null=True, blank=True)
    # otp=models.CharField(max_length=6, null=True, blank=True, default='')
    # photo=models.ImageField(upload_to='photos',null=True,blank=True, validators=[validate_image])
    # public_profile=models.BooleanField(default=False, verbose_name='Profil public')
    # bio=models.TextField(null=True,blank=True)
    # publications=models.TextField(null=True,blank=True, validators=[validate_url_list], verbose_name="URLs des profils scientifiques (Google Scholar, ResearchGate, DBLP, ..), séparées par des sauts de ligne")
    # date_naissance=models.DateField(null=True, blank=True,verbose_name='Date de naissance')
    # date_embauche=models.DateField(null=True, blank=True,verbose_name="Date d'embauche")
    # matricule=models.CharField(max_length=20, null=True, blank=True)
    # organisme=models.ForeignKey('Organisme', on_delete=models.SET_NULL, null=True, blank=True, related_name='enseignants', verbose_name="Laboratoire/service/..")
    