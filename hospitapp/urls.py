from django.conf import settings
from .import views
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
    #path('logon', views.logon, name='logon'),
    path('login/',  LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(),name = 'logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)