from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.gene)
admin.site.register(models.compound)
admin.site.register(models.pdb)
admin.site.register(models.figc)
admin.site.register(models.figd)