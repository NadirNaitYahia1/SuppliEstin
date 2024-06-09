from django.contrib import admin
from .models import Enseignant
from .models import Institution
from .models import Session
from .models import TabMois
from .models import Activite
# from .models import VolumeAutorise
from .models import AdminMois
from .models import AnneeUniv
from .models import User
from .models import Module
from .models import Matiere

# Register your models here.
admin.site.register(Enseignant)
admin.site.register(Institution)
admin.site.register(Session)
admin.site.register(TabMois)
# admin.site.register(VolumeAutorise)
admin.site.register(AdminMois)
admin.site.register(AnneeUniv)
admin.site.register(User)
admin.site.register(Activite)
admin.site.register(Module)
admin.site.register(Matiere)