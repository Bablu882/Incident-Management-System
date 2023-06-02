
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Incident
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(
        min_length=3,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already exists.")]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        if password is None:
            raise serializers.ValidationError("Password is required.")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user




class IncidentSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = Incident
        fields = ('id', 'incident_id', 'incident_details', 'reported_date', 'priority', 'incident_status','reporter_name','reporter')
        read_only_fields = ('id', 'incident_id', 'reported_date')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        validated_data.pop('reporter')
        incident = Incident.objects.create(reporter=user, **validated_data)
        return incident




class IncidentSerializerput(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = Incident
        fields = ('id', 'incident_id', 'incident_details', 'reported_date', 'priority', 'incident_status','reporter_name','reporter')        