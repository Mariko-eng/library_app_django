from rest_framework import serializers
from .models import Attendance, User

class AttendanceSerializer(serializers.ModelSerializer):
    item = serializers.CharField(required=False,allow_blank=True)

    class Meta:
        model = Attendance
        fields = "__all__"

    def create(self,validated_data):
        item = validated_data.pop("item")
        user = None
        request = self.context.get("request")
        if request and hasattr(request,"user"):
            if not request.user.is_anonymous:
                user = request.user
            else:
                raise serializers.ValidationError("Plese Login To access The system!")
        
        instance = Attendance.objects.create(user=user,item=item)
        return instance


class UserSerializer(serializers.ModelSerializer): 

    class Meta:
        model = User
        fields = "__all__"
