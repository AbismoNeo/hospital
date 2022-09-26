from distutils import errors
from email import iterators
from django.contrib.auth import get_user_model
from re import TEMPLATE
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.conf import settings
from datetime import datetime
from hospitapp.models import antecedentes_ginecologicos, antecedentes_medicos, cita_paciente, cita_turno, medical_staff
from . import forms
from .forms import LoginForm, PacienteRegisterForm, RegistroCitasForm, ProfileForm, AntecedentesForm, GinecologiaAntecedentesForm
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
            messages.error(request, 'La cita NO fue registrada, intente de nuevo.')
    else:
        cita = RegistroCitasForm(request.POST or None)
        paciente = User.objects.get(pk = id)
    cita = RegistroCitasForm()
    paciente = User.objects.get(pk = id)
    return render(request, 'register_appointment.html',{'cita':cita , 'paciente':paciente,})


def list_appointment(request, id):
    if User.is_authenticated:
        user_id = id
        print("##### USER ID ####")
        print(user_id)
        print("##### FIRST NAME ####")
        user_first_name_get = request.user.first_name
        print(user_first_name_get)
        user_last_name_get = request.user.last_name
        print("##### LAST NAME ####")
        print(user_last_name_get)
        #Genera un Diccionario
        appointments = cita_paciente.objects.filter(id_paciente = id).values( 'id_doctor__first_name', 'id_doctor__last_name', 'id_hora__hora', 'fecha_cita','id')
        if not appointments:
            print("VACIO")
            appointments = None
        else:
            print("NO VACIO")
            
        #Genera una Tupla
        #appointments = cita_paciente.objects.filter(id_paciente = id).values_list( 'id_doctor__first_name', 'id_doctor__last_name', 'id_hora__hora', 'fecha_cita')
        print("##### APPOINTMENT ####")
        print(appointments)
        paciente  = User.objects.get(pk = user_id)
    else:
        return redirect('home')
    return render(request,'list_appointments.html',{'cita':appointments, 'paciente': paciente})

def remove_appointment(request, id):
    if User.is_authenticated:
        #Borramos la cita
        record = cita_paciente.objects.get(pk = id )
        record.delete()
        paciente = record.id
        appointments = cita_paciente.objects.filter(id_paciente = paciente).values( 'id_doctor__first_name', 'id_doctor__last_name', 'id_hora__hora', 'fecha_cita','id')
        print(appointments)
        paciente = User.objects.get(pk = id)
    else:
        print("no Borrada")
        return redirect('home')
    return render(request,'list_appointments.html',{'cita':appointments, 'paciente': paciente})

def register_medical_history(request,id):
    if request.method == 'POST':
        print("POST")
        history = AntecedentesForm(request.POST or None)
        usuario = User.objects.get(pk = history['user'].value())
        historial = antecedentes_medicos.objects.create(
        user = usuario,
        cardiovasculares = history['cardiovasculares'].value(),
        pulmonares = history['pulmonares'].value(),
        digestivos = history['digestivos'].value(),
        renales = history['renales'].value(),
        quirurgicos = history['quirurgicos'].value(),
        transfusiones = history['transfusiones'].value(),
        alcoholismo = history['alcoholismo'].value(),
        tabaquismo = history['tabaquismo'].value(),
        drogas = history['drogas'].value(),
        inmunizaciones = history['inmunizaciones'].value(),
        padre_vivo = history['padre_vivo'].value(),
        madre_vivo = history['madre_vivo'].value(),
        hnos_Tiene = history['hnos_Tiene'].value(),
        hnos_cuantos = history['hnos_cuantos'].value(),
        enfermeades_padre = history['enfermeades_padre'].value(),
        enfermeades_madre = history['enfermeades_madre'].value(),
        enfermeades_hnos = history['enfermeades_hnos'].value(),
        otras_anotaciones = history['otras_anotaciones'].value()
                                                        )
        try:
            historial.save()
            messages.success(request, 'La cita fue registrada correctamente.')
            return redirect('home')
        except:
            messages.error(request, 'La cita NO fue registrada, intente de nuevo.')
    else:
        history = AntecedentesForm(request.POST or None)
        paciente = User.objects.get(pk = id)
        history = AntecedentesForm(initial ={'user' : paciente.id})
    paciente = User.objects.get(pk = id)
    return render(request, 'register_medical_history.html',{'history':historial , 'paciente':paciente,})


def register_gynecological_history(request,id):
    if request.method == 'POST':
        history = GinecologiaAntecedentesForm(request.POST or None)
        #historial = antecedentes_ginecologicos(request.POST)
        historial = GinecologiaAntecedentesForm(request.POST or None)
        print(historial)
        try:
            antginec = historial
            antginec.save(commit = False)
            lista_ets = request.POST.getlist('ets')
            # for listets in lista_ets:
            #     print("add antes")
            #     print(listets)
            #     antginec.ets.add(listets)
            #     print("add despues")
            #historial.save()
            antginec.save()
            messages.success(request, 'La cita fue registrada correctamente.')
            return redirect('home')
        except Exception as inst:
            # print(type(inst))    # the exception instance
            # print(inst.args)     # arguments stored in .args
            # print(inst)
            # print(errors)
            messages.error(request, 'La cita NO fue registrada, intente de nuevo.')
    else:
        history = GinecologiaAntecedentesForm()
        paciente = User.objects.get(pk = id)
        history = GinecologiaAntecedentesForm(initial ={'user' : id}) #paciente.id
        print(history)
    paciente = User.objects.get(pk = id)
    return render(request, 'register_gynecological_history.html',{'history':history , 'paciente':paciente,})

"""
hora_cita
cita_dcotor

SELECT   "hospitapp_cita_paciente"."fecha_cita",
         "hospitapp_cita_turno"."hora",
         "auth_user"."first_name",
         "auth_user"."last_name"
FROM     "hospitapp_cita_turno" 
INNER JOIN "hospitapp_cita_paciente"  ON "hospitapp_cita_turno"."id" = "hospitapp_cita_paciente"."id_hora_id" 
INNER JOIN "auth_user"  ON "auth_user"."id" = "hospitapp_cita_paciente"."id_doctor_id" 


Ejemplo de Query
Datos.objects.filter(User_pk__id_paciente = id).values(«campos que quieres»)
Datos.objects.filter(User_pk__id_paciente = id).values_list(«campos que quieres») 
"""