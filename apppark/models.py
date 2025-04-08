from django.db import models
from userapp.models import CustomUser 

class Parking(models.Model):

    class TypeEnum(models.TextChoices):
        FREE = 'free', 'Free' 
        PAID = 'paid', 'Paid'  

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TypeEnum.choices, default=TypeEnum.PAID)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return self.title

class Floor(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    number = models.IntegerField()
    suffix = models.CharField(max_length=2)

    def __str__(self):
        return self.suffix

class Slot(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    number = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

class Booking(models.Model):

    class StatusEnum(models.TextChoices):
        BOOKED='booked'
        ARRIVED='arrived'
        LEFT='left'
        REJECTED='rejected'


    car_number = models.CharField(max_length=100)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booked_time = models.DateTimeField(auto_now_add=True)
    arrived_time = models.DateTimeField(blank=True,null=True) 
    left_time = models.DateTimeField(null=True, blank=True)    
    rejected_time = models.DateTimeField(null=True, blank=True)  
    status=models.CharField(max_length=100,choices=StatusEnum.choices,default=StatusEnum.BOOKED)

    def __str__(self):
        return str(self.car_number)

    
