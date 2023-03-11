from django.contrib import admin

# Register your models here.
from .models import store,categoria,books,customer,order,ordenDetalle
admin.site.register([store,categoria,books,customer,order,ordenDetalle])
