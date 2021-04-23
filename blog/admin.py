from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Admin,Plat,Cart,CartPlat,Order,Customer])