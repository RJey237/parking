from django.contrib import admin
from .models import Parking,Floor,Slot,Booking


admin.site.register(Parking)
admin.site.register(Floor)
admin.site.register(Slot)

admin.site.register(Booking)
