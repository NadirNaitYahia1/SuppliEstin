from django.contrib import admin
from .models import Enseignant
from .models import Institution

# Register your models here.
admin.site.register(Enseignant)
admin.site.register(Institution)