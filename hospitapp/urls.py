from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('faqs', views.faqs, name='faqs'),
    path('services', views.services, name='services'),
    path('specialties', views.specialties, name='specialties'),
    path('doctors', views.doctors, name='doctors'),
    path('testimonials', views.testimonials, name='testimonials'),
    #path('login/',  LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('loginuser/', views.loginuser, name = 'loginuser'),
    path('logout/', LogoutView.as_view(),name = 'logout'),
    path('register_patient/', views.register_patient, name = 'register_patient'),
    path('list_appointment/<int:id>/', views.list_appointment, name = 'list_appointment'),
    path('register_appointment/<int:id>/', views.register_appointment, name = 'register_appointment'),
    path('register_medical_history/<int:id>/', views.register_medical_history, name = 'register_medical_history'),
    path('register_gynecological_history/<int:id>/', views.register_gynecological_history, name = 'register_gynecological_history'),
    path('remove_appointment/<int:id>/', views.remove_appointment, name = 'remove_appointment'),
    path('patient_profile/<int:id>/', views.patient_profile, name = 'patient_profile'),
    path('medical_profile/<int:id>/', views.medical_profile, name = 'medical_profile'),
    path('user_profile/<int:id>/', views.user_profile, name = 'user_profile'),
    path('alergies_patient/<int:id>/', views.alergies_patient, name = 'alergies_patient'),
    path('operations_history_patient/<int:id>/', views.operations_history_patient, name = 'operations_history_patient'),
    path('indicators_pre/<int:id>/', views.indicators_pre, name = 'indicators_pre'),
    path('search_patients/<int:id>/', views.search_patients, name = 'search_patients'),
    path('appointment_doctor/<int:id>/', views.appointment_doctor, name = 'appointment_doctor'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)