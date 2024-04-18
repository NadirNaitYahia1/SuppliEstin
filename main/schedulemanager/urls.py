from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('set-months-by-admin/<str:year>/', views.set_months, name='set_months'),
    path('fiche-heurs-supps/<str:type>/<str:year>/<str:month>/', views.fiche_heurs_supps, name='fiche_heurs_supps_vacataires'),
    path('form/<str:enseignant>/<str:year>/<str:month>/', views.fiche_heurs_supps_enseignant, name='fiche_heurs_supps_enseignant'),
    path('fiche-heurs-supps/save/', views.save, name='save'),
    # path('heurs-supps-form/<int:enseignant>/<str:year>/<int:month>/', views.fiche_heurs_supps_enseignant, name='fiche_heurs_supps_enseignant'),
]