from distutils import errors
from django.contrib.auth import get_user_model
from re import TEMPLATE
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.conf import settings
from . import forms
from .forms import LoginForm, PacienteRegisterForm, RegistroCitasForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

""""
####################### MODO - COMPLETO ######################
messages.add_message(request, messages.INFO, 'Le quedan 2 intentos más.')
###################### MODO - ABREVIADO ######################
messages.debug(request, 'Se ejecutaron las sentencias SQL.')
messages.info(request, 'Le quedan 2 intentos más.')
messages.success(request, 'El producto fue creado correctamente.')
messages.warning(request, 'Tu cuenta caduca en tres días.')
messages.error(request, 'Documento eliminado.')
"""

User = get_user_model()

# Create your views here.
# El home de la pagina donde se cambian los menus por usuario.
def home(request):
    username_post = request.user['username']
    password_post = request.user['password']
    if user.is_authenticated:
        query = User.objects.get(username = request.User)
        print(query)
    else:
        user = authenticate(request, username=username_post, password=password_post)
        query = User.objects.get(username = request.User)
        print(query)
    else:
        query = None
        User.is_authenticated = False
    
    if User.is_authenticated:
        if query.is_superuser == True:
            # MENU SUPERUSER
            print('Super')
            menu = 0
        else:
            if query.es_admin == True:
                # MENU ADMIN-SISTEMA
                print('Admin')
                menu = 1
                if query.es_doctor:
                    # MENU ADMIN-DOCTOR
                    print('Admin Doc')
                    menu = 2
                elif query.es_enfermera == True:
                    # MENU ADMIN-ENFERMERA
                    print('Admin Enfer')
                    menu = 3
                elif query.es_farmacia == True:
                    # MENU ADMIN-FARMACIA
                    print('Admin Farm')
                    menu = 4
            elif query.es_paciente == True:
                # MENU PACIENTE
                print('Paciente')
                menu  = 5
            elif query.es_doctor == True:
                print('Doc')
                # MENU DOCTOR
                menu = 6
            elif query.es_enfermera == True:
                #MENU ENFERMERA
                print('Enfermera')
                menu = 7
            elif query.es_farmacia == True:
                # MENU FARMACIA
                print('Farmacia')
                menu = 8
            elif query.es_secretaria == True:
                # MENU SECRETARIA
                print('Secretaria')
                menu = 9
    else:
        #MENU SIN USUARIO
        print('Sin Usuario')
        menu = 10
    
    
    context = {
        'Title':'Hospitapp - Hospital MY-ANGELS',
        'paciente':query,
        'menu' : menu,
    }
    return render(request,'index.html',context)

#Login
def loginuser(request):
    loginform = LoginForm(request.POST)
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect('home')
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('loginuser')
    else:
        loginform = LoginForm()
    return render(request,'loginuser.html',{'loginuserform':loginform})


#Paginas del sitio generales
def faqs(request):
    context = {
        'Title':'Hospitapp - Preguntas Frecuentes',
    }
    return render(request,'faqs.html',context)


def services(request):
    context = {
        'Title':'Hospitapp - Servicios',
    }
    return render(request,'services.html',context)


def specialties(request):
    context = {
        'Title':'Hospitapp - Especialidades',
    }
    return render(request,'specialties.html',context)


def doctors(request):
    context = {
        'Title':'Hospitapp - Doctores',
    }
    return render(request,'doctors.html',context)

def testimonials(request):
    context = {
        'Title':'Hospitapp - Testimonios - Conocenos',
    }
    return render(request,'testimonials.html',context)

#Registrar a un paciente desde la pagina

def register_patient(request):
    paciente = PacienteRegisterForm(request.POST)
    if request.method == 'POST':
        if paciente.is_valid():
            paciente.es_paciente = True
            paciente = paciente.save()
            return redirect('login', {'username': paciente.username, 'password': paciente.password})

        else:
            print(paciente.non_field_errors)
            print(paciente.errors)
    else:
        paciente = PacienteRegisterForm()
    return render(request, 'register_paciente.html',{'paciente':paciente})

#Registrar un cita 

def register_appointment(request):
    cita = RegistroCitasForm(request.POST)
    if request.method == 'POST':
        if cita.is_valid():
            cita.es_paciente = True
            cita = cita.save()
            messages.success(request, 'La cita fue registrada correctamente.')
            return redirect('home')

        else:
            messages.error(request, 'La cita NO fue registrada, intente de nuevo.')
            print(cita.non_field_errors)
            print(cita.errors)
    else:
        cita = RegistroCitasForm()
    return render(request, 'registrar_cita.html',{'cita':cita})