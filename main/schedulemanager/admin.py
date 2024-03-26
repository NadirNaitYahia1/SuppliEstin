from django.contrib import admin
from .models import Enseignant
from .models import Institution
from .models import Session
from .models import TabMois
# from .models import VolumeAutorise
from .models import AdminMois
from .models import AnneeUniv

# Register your models here.
admin.site.register(Enseignant)
admin.site.register(Institution)
admin.site.register(Session)
admin.site.register(TabMois)
# admin.site.register(VolumeAutorise)
admin.site.register(AdminMois)
admin.site.register(AnneeUniv)




