from rest_framework import serializers
from .models import Parking, Floor, Slot, Booking


class RegisterParkingSerializer(serializers.ModelSerializer):
    floors = serializers.ListField(write_only=True)

    class Meta:
        model = Parking
        exclude = ['owner', 'status']

    def create(self, validated_data):
        floors = validated_data.pop('floors', [])
        parking = super().create(validated_data)

        for floor_data in floors:
            slots_count = floor_data.pop("slots")
            floor = Floor.objects.create(**floor_data, parking=parking)
            slots = [Slot(floor=floor, number=i) for i in range(1, slots_count + 1)]
            Slot.objects.bulk_create(slots, batch_size=500)

        return parking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['car_number', 'slot']
        extra_kwargs = {
            'car_number': {'required': False}
        }

    def save(self, **kwargs):
        user = self.context['request'].user
        slot=self.validated_data['slot']

        slot.status=True
        slot.save() 

        if user.is_authenticated:
            self.validated_data['car_number'] = user.car_number
        else:
            if not self.validated_data.get("car_number", None):
                raise serializers.ValidationError("car_number must be set")
        
        booking,_=Booking.objects.get_or_create(**self.validated_data,status='booked')
        return booking

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields="__all__"

        depth=3

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'number', 'status']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'number', 'suffix'] 


class ParkingShortSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Parking
        fields = ['id', 'title', 'address', 'type_display', 'latitude', 'longitude', 'price']


class ParkingDetailSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    floor_set = FloorSerializer(many=True, read_only=True) 

    class Meta:
        model = Parking
        fields = [
            'id',
            'owner',
            'title',
            'type',
            'type_display',
            'address',
            'status',
            'latitude',
            'longitude',
            'price',
            'floor_set',
        ]