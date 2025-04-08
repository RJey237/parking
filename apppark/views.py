from rest_framework.viewsets import ViewSet,ModelViewSet
from  .serializers import RegisterParkingSerializer,BookingSerializer,BookingDetailSerializer,ParkingShortSerializer,ParkingDetailSerializer
from .models import Parking,Booking
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action 
from rest_framework.response import Response
from django.db.models import Q,Count
from rest_framework import status
from django.utils import timezone

class RegisterParkingViewset(ModelViewSet):
    serializer_class=RegisterParkingSerializer
    http_method_names=['get','post']
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Parking.objects.filter(owner=self.request.user)


    def perform_create(self, serializer):
        data =serializer.save(owner=self.request.user)
        return data
    

class BookingSlotViewSet(ViewSet):
    @action(methods=['POST'],detail=False)
    def book(self,request,*args,**kwargs):
        serializer=BookingSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        data=serializer.save()
        detail_serializer=BookingDetailSerializer(data)
        # ss=BookingSerializer(data)
        return Response(detail_serializer.data)


    @action(methods=['POST'], detail=True)
    def arrive(self, request, pk=None, *args, **kwargs):
        booking = self.get_booking(pk)
        if not booking:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != Booking.StatusEnum.BOOKED:
            return Response({"detail": "Booking is not in 'booked' state."}, status=status.HTTP_400_BAD_REQUEST)

        booking.arrived_time = timezone.now()
        booking.status = Booking.StatusEnum.ARRIVED
        booking.save()

        detail_serializer = BookingDetailSerializer(booking)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def left(self, request, pk=None, *args, **kwargs):

        booking = self.get_booking(pk)
        if not booking:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != Booking.StatusEnum.ARRIVED:
            return Response({"detail": "Booking is not in 'arrived' state."}, status=status.HTTP_400_BAD_REQUEST)

        booking.left_time = timezone.now()
        booking.status = Booking.StatusEnum.LEFT

        duration = booking.left_time - booking.arrived_time
        duration_in_hours = duration.total_seconds() / 3600





        booking.save() 

        detail_serializer = BookingDetailSerializer(booking)

        response_data = detail_serializer.data


        return Response(response_data, status=status.HTTP_200_OK)  
    @action(methods=['POST'], detail=True)
    def reject(self, request, pk=None, *args, **kwargs):
        booking = self.get_booking(pk)
        if not booking:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != Booking.StatusEnum.BOOKED:
            return Response({"detail": "Booking is not in 'booked' state."}, status=status.HTTP_400_BAD_REQUEST)

        booking.rejected_time = timezone.now()
        booking.status = Booking.StatusEnum.REJECTED


        booking.slot.status = False  
        booking.slot.save()

        if booking.arrived_time:
            duration = booking.rejected_time - booking.arrived_time
        else:
            duration = booking.rejected_time - booking.booked_time
        duration_in_hours = duration.total_seconds() / 3600


   
        booking.save()

        detail_serializer = BookingDetailSerializer(booking)

        response_data = detail_serializer.data


        return Response(response_data, status=status.HTTP_200_OK)
    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return None


class ParkingViewSet(ViewSet):
    def list(self,request):
        parkings=Parking.objects.all()
        serializer=ParkingShortSerializer(parkings,many=True)
        return Response(serializer.data)
    

    @action(methods=['POST'],detail=False)
    def parking_detail(self,request,*args,**kwargs):
        parking_id=request.data.get('parking_id',None)
        parking=Parking.objects.annotate(floor_count=Count('floors',distance=True))
        serializer=ParkingDetailSerializer(parking)
        return Response(serializer.data)


    