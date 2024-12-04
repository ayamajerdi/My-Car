from django.urls import path
from .views import RegisterView, LoginView, DashboardView, LogoutView, AddClientView, ListClientView, DeleteClientView, UpdateClientView, GetClientView, AddChauffeurView
from .views import ListChauffeurView,  DeleteChauffeurView, GetChauffeurView, UpdateChauffeurView
from .views import  AddVehiculeView,ListVehiculeView, GetVehiculeView,UpdateVehiculeView, DeleteVehiculeView

from .views import AddCourseView, ListCourseView, GetCourseView, UpdateCourseView, DeleteCourseView
from .views import MonCompteView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-client/', AddClientView.as_view(), name='add-client'),
    path('list-clients/', ListClientView.as_view(), name='list-clients'),
    path('delete-client/<int:client_id>/', DeleteClientView.as_view(), name='delete-client'),
    path('update-client/<int:client_id>/', UpdateClientView.as_view(), name='update-client'),
    path('get-client/<int:client_id>/', GetClientView.as_view(), name='get-client'),
    path('add-chauffeur/', AddChauffeurView.as_view(), name='add-chauffeur'),
    path("list-chauffeurs/", ListChauffeurView.as_view(), name="list-chauffeurs"),
    path("delete-chauffeur/<int:chauffeur_id>/", DeleteChauffeurView.as_view(), name="delete-chauffeur"),
    path("get-chauffeur/<int:chauffeur_id>/", GetChauffeurView.as_view(), name="get-chauffeur"),
    path("update-chauffeur/<int:chauffeur_id>/", UpdateChauffeurView.as_view(), name="update-chauffeur"),
    path('vehicule/add/', AddVehiculeView.as_view(), name='add_vehicule'),
path('vehicule/list/', ListVehiculeView.as_view(), name='list_vehicules'),
    path('vehicule/<int:vehicule_id>/', GetVehiculeView.as_view(), name='get_vehicule'),
     path('vehicule/update/<int:vehicule_id>/', UpdateVehiculeView.as_view(), name='update_vehicule'),
    path('vehicule/delete/<int:vehicule_id>/', DeleteVehiculeView.as_view(), name='delete_vehicule'),
path('course/add/', AddCourseView.as_view(), name='add_course'),
    path('course/list/', ListCourseView.as_view(), name='list_courses'),
    path('course/<int:pk>/', GetCourseView.as_view(), name='get_course'),
    path('course/update/<int:pk>/', UpdateCourseView.as_view(), name='update_course'),
    path('course/delete/<int:pk>/', DeleteCourseView.as_view(), name='delete_course'),
        path('api/mon-compte/', MonCompteView.as_view(), name='mon-compte'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)