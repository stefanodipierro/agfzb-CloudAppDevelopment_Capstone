from django.contrib import admin
# from .models import related models
from .models import Dealership, Review, CarMake, CarModel



# Register your models here.

# <HINT> Register your models here
admin.site.register(Dealership)
admin.site.register(Review)
admin.site.register(CarMake)
admin.site.register(CarModel)

