from rest_framework import serializers
from .models import Device,Attendance,User

class AddAttendanceSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(write_only = True)
    device_addr = serializers.CharField(write_only = True)
    attendance_type = serializers.CharField()
    activity = serializers.CharField(allow_blank=True)

    class Meta:
        model = Attendance
        fields = "__all__"

    def create(self,validated_data):
        device_name = validated_data.pop("device_name")
        device_addr = validated_data.pop("device_addr")
        attendance_type = validated_data.pop("attendance_type")
        activity = validated_data.pop("activity")

        user = None
        request = self.context.get("request")
        if request and hasattr(request,"user"):
            if not request.user.is_anonymous:
                user = request.user
            else:
                raise serializers.ValidationError("Plese Login To access The system!")
        
        if Device.objects.filter(address=device_addr).exists():
            device = Device.objects.filter(address=device_addr).first()
            device.name = device_name
            device.save()
        else:
            device = Device.objects.create(name=device_name,address=device_addr)
        
        instance = Attendance.objects.create(user=user,device=device,
            attendance_type=attendance_type,activity=activity)
        return instance


class DeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Device
        fields = "__all__"

class AttendanceSerializer(serializers.ModelSerializer):
    device =  DeviceSerializer()
    class Meta:
        model = Attendance
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer): 
    name = serializers.CharField()

    class Meta:
        model = User
        fields = "__all__"
