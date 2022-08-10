from re import TEMPLATE
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if User.is_authenticated:
        if User.is_superuser:
            print("SuperUsuario")
        elif User.es_admin:
            print("Administrador")
        elif User.es_paciente:
            print("Paciente")
        elif User.es_doctor:
            print("Doctor")
        elif User.es_enfermera:
            print("Enfermera")
        elif User.es_farmacia:
            print("Farmacia")
        elif User.es_secretaria:
            print("Secretaria")
    else:
        print("NO autenticado")
    context = {
        'Title':'Hospitapp - Hospital MY-ANGELS',
    }
    return render(request,'index.html',context)


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

