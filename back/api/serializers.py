from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Client, Chauffeur, Vehicule
from .models import Course

# serializers.py
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nom', 'prenom', 'password', 'image']
        extra_kwargs = {
            'password': {'write_only': True},
            'image': {'required': False},  
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data)

    
class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'nom', 'prenom', 'email', 'image', 'image_url']
        read_only_fields = ['email']  

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    
class AddClientSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'nom', 'prenom', 'email', 'phone', 'adresse', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class AddChauffeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chauffeur
        fields = ['id', 'nom', 'prenom', 'email', 'phone', 'adresse', 'image', 'documentation', 'is_active', 'is_available']
        
        
class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = '__all__'
        
        
class CourseSerializer(serializers.ModelSerializer):
    chauffeur_name = serializers.ReadOnlyField(source='chauffeur.nom')
    client_name = serializers.ReadOnlyField(source='client.nom')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    vehicule_reference = serializers.ReadOnlyField(source='vehicule.reference')

    class Meta:
        model = Course
        fields = [
            "id",
            "chauffeur",
            "chauffeur_name",
            "client",
            "client_name",
            "client_phone",
            "vehicule",
            "vehicule_reference",
            "status",
            "start_time",
            "end_time",
            "tarif",
        ]

