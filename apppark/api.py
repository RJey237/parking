from rest_framework.routers import SimpleRouter,DefaultRouter
app=DefaultRouter()
from .views import RegisterParkingViewset,BookingSlotViewSet,ParkingViewSet,BookingSlotViewSet
from django.urls import path, include

app.register(r"register-parking",RegisterParkingViewset,basename="register-parking")
app.register(r'book-slot', BookingSlotViewSet, basename='book-slot')
app.register(r'parkings', ParkingViewSet, basename='parkings') 
 

urlpatterns=[
    path('',include(app.urls)),
]