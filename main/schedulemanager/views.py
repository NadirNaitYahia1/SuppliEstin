from django.shortcuts import render
from .models import AnneeUniv, AdminMois,Enseignant,TabMois
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
                months.append((month.numMois, calendar.month_abbr[month.numMois]))
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


def fiche_heurs_supps(request, type, year, month):
    list = []
    if type[0:1].upper() in ['V', 'P']:
        
        listEnseignants = get_list_enseignants(type[0:1].upper())

        if listEnseignants:

            objAdminMois = get_list_nb_semaines_mois_annee(year, month)
            nbSemainesMonthYear = objAdminMois[0].nbSemaines

            idMois = objAdminMois[0].idMois
            listHeurSupps = get_list_heurs_supps_enseignants(listEnseignants, idMois)  


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
                        if heurSupp[0].idEnseignat.matricule == prof.matricule:
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
                'nbSemainesMonthYear': nbSemainesMonthYear,
        
            }
            print('context',context["nbSemainesMonthYear"])
            return render(request, 'fiche_heurs_supps.html', context)
    else:   
        return render(request, '404.html')
        
        
    
         



# _______________________________________________________________________________________________________



def fiche_heurs_supps_enseignant(request, enseignant, year, month):
    return render(request, 'fiche_heurs_supps_enseignant.html')