from distutils import errors
from django.contrib.auth import get_user_model
from re import TEMPLATE
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.conf import settings

from hospitapp.models import cita_paciente, cita_turno, medical_staff
from . import forms
from .forms import LoginForm, PacienteRegisterForm, RegistroCitasForm, ProfileForm
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
################################
# El home de la pagina donde se cambian los menus por usuario.
################################

def home(request):
    username_get = request.user.username
    user_id = request.user.id
    print(username_get)
    print(user_id)
    if User.is_authenticated:
        print("autenticado")
        querybd = User.objects.get(pk = user_id)
        print(querybd.first_name)
    else:
        querybd = None
        User.is_authenticated = False
    
    if User.is_authenticated:
        if querybd.is_superuser == True:
            # MENU SUPERUSER
            print('Super')
            menu = 0
        else:
            if querybd.es_admin == True:
                # MENU ADMIN-SISTEMA
                print('Admin')
                menu = 1
                if querybd.es_doctor:
                    # MENU ADMIN-DOCTOR
                    print('Admin Doc')
                    menu = 2
                elif querybd.es_enfermera == True:
                    # MENU ADMIN-ENFERMERA
                    print('Admin Enfer')
                    menu = 3
                elif querybd.es_farmacia == True:
                    # MENU ADMIN-FARMACIA
                    print('Admin Farm')
                    menu = 4
            elif querybd.es_paciente == True:
                # MENU PACIENTE
                print('Paciente')
                menu  = 5
            elif querybd.es_doctor == True:
                print('Doc')
                # MENU DOCTOR
                menu = 6
            elif querybd.es_enfermera == True:
                #MENU ENFERMERA
                print('Enfermera')
                menu = 7
            elif querybd.es_farmacia == True:
                # MENU FARMACIA
                print('Farmacia')
                menu = 8
            elif querybd.es_secretaria == True:
                # MENU SECRETARIA
                print('Secretaria')
                menu = 9
    else:
        #MENU SIN USUARIO
        print('Sin Usuario')
        menu = 10
    
    
    context = {
        'Title':'Hospitapp - Hospital MY-ANGELS',
        'paciente':querybd,
        'menu' : menu,
    }
    return render(request,'index.html',context)

################################
#Login
################################

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

################################
#Paginas del sitio generales
################################

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

################################
#Registrar a un paciente desde la pagina
################################

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

################################
# Modificar el perfil de usuario
################################

def user_profile(request,id):
    user_id = id
    if request.method == 'POST':
        print("Post")
        datos = User.objects.get(pk = user_id)
        profile = ProfileForm(request.POST)
        datos.id = user_id
        print(datos.id)
        datos.username = profile['username'].value()
        print(datos.username)
        datos.first_name = profile['first_name'].value()
        print(datos.first_name)
        datos.last_name = profile['last_name'].value()
        print(datos.last_name)
        datos.email = profile['email'].value()
        print(datos.email)
        datos.rfc = profile['rfc'].value()
        print(datos.rfc)
        try:
            usuario = datos.save()
            paciente = datos
            profile = ProfileForm(request.POST or None, instance = datos)    
            print('valido y save')
            return redirect('home')
        except Exception as e:
            print(e)
            profile = ProfileForm(request.POST or None, instance = datos)
            paciente = datos
    else:
        datos = User.objects.get(pk = user_id)
        profile = ProfileForm(request.POST or None, instance = datos)        
        print('solo cargamos datos')
    paciente = datos
    return render(request,'user_profile.html', {'paciente':paciente, 'profile' : profile})

################################
#Registrar un cita 
################################

def register_appointment(request,id):
    
    if request.method == 'POST':
        cita = RegistroCitasForm(request.POST or None)
        paciente = User.objects.get(pk = id)
        hora = cita_turno.objects.get(pk = request.POST['id_hora'])
        doctor = User.objects.get(pk = request.POST['id_doctor'])
        fechacita = request.POST['fecha_cita']
        citas_medico = cita_paciente(id_paciente = paciente ,fecha_cita = fechacita, id_hora = hora, id_doctor = doctor)
        try:
            citas_medico.save()
            messages.success(request, 'La cita fue registrada correctamente.')
            return redirect('home')
        except:
            print("errors")
            #messages.error(request, 'La cita NO fue registrada, intente de nuevo.')
    else:
        cita = RegistroCitasForm(request.POST or None)
        paciente = User.objects.get(pk = id)
    cita = RegistroCitasForm()
    paciente = User.objects.get(pk = id)
    return render(request, 'register_appointment.html',{'cita':cita , 'paciente':paciente,})