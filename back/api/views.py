from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from django.db.models import Sum
from .models import Client, Course, Chauffeur, Vehicule, Course
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from .serializers import AddClientSerializer
from .serializers import AddChauffeurSerializer
from .serializers import VehiculeSerializer
from .serializers import CourseSerializer
from .serializers import UserSerializer
from django.db.models import Sum


#register
# views.py
# views.py
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#login
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email et mot de passe sont requis.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Connexion réussie !',
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Email ou mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)
    #Logout

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Déconnexion réussie !'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
class MonCompteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Récupérer les détails de l'utilisateur connecté"""
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        """Mettre à jour les informations de l'utilisateur connecté"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profil mis à jour avec succès.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
#Dashboard

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            total_clients = Client.objects.count()
            total_courses = Course.objects.filter(status="en cours").count()
            total_chauffeurs = Chauffeur.objects.filter(is_active=True).count()
            total_vehicules = Vehicule.objects.count()
            benefices = Course.objects.aggregate(total_tarif=Sum('tarif')).get('total_tarif', 0) or 0

            user = request.user
            image_url = request.build_absolute_uri(user.image.url) if user.image else None

            return Response({
                "total_clients": total_clients,
                "total_courses": total_courses,
                "total_chauffeurs": total_chauffeurs,
                "total_vehicules": total_vehicules,
                "benefices": benefices,
                "mon_compte": {
                    "email": user.email,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "image_url": image_url,
                },
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#client

class AddClientView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = AddClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Client ajouté avec succès !'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ListClientView(APIView):
     permission_classes = [AllowAny]
     def get(self, request):  
        clients = Client.objects.all()
        serializer = AddClientSerializer(clients, many=True, context={'request': request})
        return Response(serializer.data)
class DeleteClientView(APIView):
    def delete(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return Response({"message": "Client supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response({"error": "Client introuvable."}, status=status.HTTP_404_NOT_FOUND)
        
        
        
class UpdateClientView(APIView):
    
    def put(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            print("Données reçues :", request.data) 
            serializer = AddClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Client mis à jour avec succès !", "data": serializer.data}, status=status.HTTP_200_OK)
            print("Erreurs de validation :", serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response({"error": "Client introuvable."}, status=status.HTTP_404_NOT_FOUND)

class GetClientView(APIView):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        serializer = AddClientSerializer(client, context={'request': request})
        return Response(serializer.data)


#Chauffeur
class AddChauffeurView(APIView):
   
    permission_classes = [AllowAny]    
    def post(self, request):
        serializer = AddChauffeurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Chauffeur ajouté avec succès !", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ListChauffeurView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        chauffeurs = Chauffeur.objects.all()
        serializer = AddChauffeurSerializer(chauffeurs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteChauffeurView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, chauffeur_id):
        try:
            chauffeur = Chauffeur.objects.get(id=chauffeur_id)
            chauffeur.delete()
            return Response({"message": "Chauffeur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Chauffeur.DoesNotExist:
            return Response({"error": "Chauffeur introuvable."}, status=status.HTTP_404_NOT_FOUND)
class GetChauffeurView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, chauffeur_id):
        try:
            chauffeur = Chauffeur.objects.get(id=chauffeur_id)
            serializer = AddChauffeurSerializer(chauffeur)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Chauffeur.DoesNotExist:
            return Response({"error": "Chauffeur introuvable."}, status=status.HTTP_404_NOT_FOUND)

class UpdateChauffeurView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, chauffeur_id):
        try:
            chauffeur = Chauffeur.objects.get(id=chauffeur_id)
            print("Données reçues :", request.data)  
            serializer = AddChauffeurSerializer(chauffeur, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Chauffeur mis à jour avec succès !", "data": serializer.data}, status=status.HTTP_200_OK)
            print("Erreurs de validation :", serializer.errors)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Chauffeur.DoesNotExist:
            return Response({"error": "Chauffeur introuvable."}, status=status.HTTP_404_NOT_FOUND)

#  Vehicle

class AddVehiculeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VehiculeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Véhicule ajouté avec succès !", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ListVehiculeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        vehicules = Vehicule.objects.all()
        serializer = VehiculeSerializer(vehicules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class GetVehiculeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, vehicule_id):
        try:
            vehicule = Vehicule.objects.get(id=vehicule_id)
            serializer = VehiculeSerializer(vehicule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehicule.DoesNotExist:
            return Response({"error": "Véhicule introuvable."}, status=status.HTTP_404_NOT_FOUND)
class UpdateVehiculeView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, vehicule_id):
        try:
            vehicule = Vehicule.objects.get(id=vehicule_id)
            serializer = VehiculeSerializer(vehicule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Véhicule mis à jour avec succès !", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehicule.DoesNotExist:
            return Response({"error": "Véhicule introuvable."}, status=status.HTTP_404_NOT_FOUND)


class DeleteVehiculeView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, vehicule_id):
        try:
            vehicule = Vehicule.objects.get(id=vehicule_id)
            vehicule.delete()
            return Response({"message": "Véhicule supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Vehicule.DoesNotExist:
            return Response({"error": "Véhicule introuvable."}, status=status.HTTP_404_NOT_FOUND)



#Courses
class AddCourseView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                chauffeur = serializer.validated_data['chauffeur']
                vehicule = serializer.validated_data.get('vehicule')

              
                if not chauffeur.is_available:
                    return Response({"error": "Chauffeur non disponible."}, status=status.HTTP_400_BAD_REQUEST)
            
                if vehicule and vehicule.status != "active":
                    return Response({"error": "Véhicule non actif."}, status=status.HTTP_400_BAD_REQUEST)
                print("Erreurs de validation :", serializer.errors)
               
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCourseView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCourseView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course introuvable."}, status=status.HTTP_404_NOT_FOUND)


class UpdateCourseView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({"error": "Course introuvable."}, status=status.HTTP_404_NOT_FOUND)


class DeleteCourseView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({"message": "Course supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"error": "Course introuvable."}, status=status.HTTP_404_NOT_FOUND)