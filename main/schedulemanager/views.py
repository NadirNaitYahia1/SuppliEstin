from django.shortcuts import render
from .models import AnneeUniv, AdminMois,Enseignant,TabMois,Session
import calendar
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
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


def get_list_enseignants(typeEnseignant):
    return Enseignant.get_profs(typeEnseignant )

def get_list_nb_semaines_mois_annee(year, month):
    return AdminMois.get_nb_semaine_mois_annee(month, year)

def get_list_heurs_supps_enseignants(profs, idAdminMois):
    return TabMois.get_heursSupps(profs, idAdminMois) 


def get_months_anneeUnivs( ):
    return AdminMois.get_months_anneeUnivs()


def fiche_heurs_supps(request, type, year, month):
    list = []
    if type[0:1].upper() in ['V', 'P']:
        
        listEnseignants = get_list_enseignants(type[0:1].upper())

        if listEnseignants:

            objAdminMois = get_list_nb_semaines_mois_annee(year, month)
            nbSemainesMonthYear = objAdminMois[0].nbSemaines

            idMois = objAdminMois[0].idMois
            listHeurSupps = get_list_heurs_supps_enseignants(listEnseignants, idMois)  



            listMoisAnnee = get_months_anneeUnivs()
            anneeUnniv =[]

            for item in listMoisAnnee:
                if item.anneeUniv.annee_univ not in [annee[0] for annee in anneeUnniv]:
                    mois_annee = [mois_item.nomMois for mois_item in listMoisAnnee if mois_item.anneeUniv.annee_univ == item.anneeUniv.annee_univ]
                    anneeUnniv.append([item.anneeUniv.annee_univ, mois_annee])


            print('agenda',anneeUnniv)

            print('listHeurSupps',listHeurSupps) 
    

            for prof in listEnseignants:
                item = {}
                item['nom'] = prof.nom
                item['prenom'] = prof.prenom
                item['grade'] = prof.grade
                item['volumeAutorise'] = prof.VolumeAutorise
                item['nbSemaine'] = nbSemainesMonthYear
                if listHeurSupps:
                    for heurSupp in listHeurSupps:
                        if heurSupp[0] == prof:
                            item['heursSupps'] = heurSupp[0].heursSupps
                        else:
                            item['heursSupps'] = 0
                    list.append(item)
                else:
                    item['heursSupps'] = 0
                    list.append(item)
            print(list)
            context = {
                'type': type, 
                'year': year,
                'month': month,
                'list': list,
                'anneeUnniv':   anneeUnniv ,
                'nbSemainesMonthYear': nbSemainesMonthYear,
        
            }
            print('context',context["nbSemainesMonthYear"])
            return render(request, 'fiche_heurs_supps.html', context)
    else:   
        return HttpResponse('Type de professeur non valide : V pour vacataire et P pour permanent')

        
# _________________________________________________________________________________________________________________________________________________________  
         
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
    tab_mois = TabMois.objects.filter(idEnseignat=enseignant, idMois=admin_mois).first()
    isNew = False
    semaines = []
    sessions = None
    if request.method == 'POST':
        try:
            data = json.loads(request.body)['newSessions']
            for i in range(len(data)):
                for session in data[i]:
                    print("the session: ", session)
                    new_session = Session(idEnseignat=enseignant, typeSession=session['type'], idTabMois=tab_mois, numSemaine=i+1, Date=session['date'], heurDebut=session['start'], heurFin=session['end'], heurs=session['heurs'], minutes=session['minutes'])
                    new_session.save()
                    tab_mois.heursSupps += session['heurs']
                    if tab_mois.minutesSupps + session['minutes'] >= 60:
                        tab_mois.heursSupps += 1
                        tab_mois.minutesSupps = (tab_mois.minutesSupps + session['minutes']) - 60
                    else:
                        tab_mois.minutesSupps += session['minutes']
            tab_mois.save()
            return JsonResponse({'message': 'Vots séances a été ajoutée avec succès'})
        except Exception as e:
            print(e)
            return JsonResponse({'message': "erreur lors de l'ajout de la séance"})
    if not tab_mois:
        isNew = True
    else:
        tab_mois = tab_mois
        sessions = Session.objects.filter(idTabMois=tab_mois)
        if sessions:
            for i in range(1, admin_mois.nbSemaines+1):
                semaines.append({"numSemaine": i, "sessions": []})
                for session in sessions:
                    if session.numSemaine == i:
                        semaines[i-1]["sessions"].append((i, session.Date.strftime("%d/%m/%Y"), session.heurDebut.strftime("%H:%M"), session.heurFin.strftime("%H:%M"), session.typeSession, session.heurs, session.minutes))
        else:
            for i in range(1, admin_mois.nbSemaines+1):
                semaines.append({"numSemaine": i, "sessions": []})



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
    