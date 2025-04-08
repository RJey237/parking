from django.contrib import admin
from .models import CustomUser,Card,Admin,Driver,Owner
admin.site.register(CustomUser)
admin.site.register(Card)
admin.site.register(Admin)
admin.site.register(Driver)
admin.site.register(Owner)
