from django.urls import path
from . import views

# 
urlpatterns = [
    path('', views.index, name='index'),
    path('set-months-by-admin/<str:year>/', views.set_months, name='set_months'),
    path('fiche-heurs-supps-vacataires/<str:year>/<str:month>/', views.fiche_heurs_supps, name='fiche_heurs_supps_vacataires'),
    path('fiche-heurs-supps-permanents/<str:year>/<int:month>/', views.fiche_heurs_supps, name='fiche_heurs_supps_permanents'),
    path('fiche-heurs-supps/<int:enseignant>/<str:year>/<int:month>/', views.fiche_heurs_supps_enseignant, name='fiche_heurs_supps_enseignant'),
]