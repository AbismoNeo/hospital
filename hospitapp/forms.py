from select import select
from ssl import Options
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model
import datetime
from hospitapp.models import cita_paciente, cita_turno
from tempus_dominus.widgets import DatePicker
#TimePicker, DateTimePicker

User = get_user_model()
username_validator = UnicodeUsernameValidator()

class PacienteRegisterForm(UserCreationForm):
    username = forms.CharField( 
                                label='Usuario',
                                max_length=15, 
                                help_text=('Requerido. 15 caracteres o menos, letras, digitos y @/./+/-/_ solamente.'), 
                                validators=[username_validator], 
                                error_messages={'unique': ("Ya existe un usuario con ese nombre de Usuario.")}, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
                                label='Nombre(s)',
                                max_length=32, 
                                min_length=4, 
                                required=True, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
                                label = 'Apellidos',
                                max_length=32, 
                                min_length=4, 
                                required=True, 
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    rfc = forms.CharField(
                                label = 'RFC',
                                max_length=15, 
                                min_length=13, 
                                required=True, 
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(label = 'Email',
                                max_length=50, 
                                min_length=10, 
                                required=True, 
                                widget=(forms.EmailInput(attrs={'class': 'form-control'}))
                                )                                
    password1 = forms.CharField(
                                label='Contraseña',
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})), 
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(
                                label = 'Confirmación de Contraseña', 
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
                                help_text=('Vuelva a ingresar la contraseña para confirmar'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','rfc','email', 'password1', 'password2',)


class LoginForm(forms.ModelForm):
    username = forms.CharField( 
                                label='Usuario',
                                widget=forms.TextInput(attrs={'class': 'fa fa-user form-control'}))
    password = forms.CharField(
                                label='Contraseña',
                                widget=(forms.PasswordInput(attrs={'class': 'fa fa-lock form-control'})))

    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password'].help_text = None

class RegistroCitasForm(forms.ModelForm):

    fecha_cita = input_formats=['%d/%m/%Y %H:%M']
    # fecha_cita = forms.DateField(widget = DatePicker(
    #                                 options={
    #                                     'maxDate': (datetime.date.today()+datetime.timedelta(days=15)).strftime('%d-%m-%Y'),
    #                                     'minDate':datetime.date.today().strftime('%d-%m-%Y'),
    #                                     'useCurrent': True,
    #                                     'collapse': False
    #                                         },
    #                                 attrs={
    #                                     'append': 'fas fa-calendar',
    #                                     'icon_toggle': True,
    #                                     'input_toggle': True,
    #                                     'class': 'form-control datetimepicker-input',
    #                                         }))
    id_hora = forms.ModelChoiceField(
                            label='Hora', 
                            queryset=cita_turno.objects.values_list('hora',flat=True)
                            )
    id_doctor = forms.ModelChoiceField(
                            label='Doctor', 
                            #queryset = User.__str__(User.objects.fiilter(es_doctor =True))
                            queryset = User.objects.filter(es_doctor =True)
                            )
    id_paciente = forms.CharField(widget=forms.HiddenInput())
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = cita_paciente
        fields = ('fecha_cita', 'id_hora', 'id_doctor','id_paciente',)
    #     fields = ('fecha_cita',)
    #     #fields = ('fecha_cita', 'id_hora', 'id_doctor','id_paciente',)
    #     widgets = {
    #         'fecha_cita': DatePicker(
    #                                 options={
    #                                     'maxDate': (datetime.datetime.now()+datetime.timedelta(days=15)).strftime('%d-%m-%Y'),
    #                                     'minDate':datetime.datetime.now().strftime('%d-%m-%Y'),
    #                                     'useCurrent': True,
    #                                     'collapse': False
    #                                         },
    #                                 attrs={
    #                                     'append': 'fas fa-calendar',
    #                                     'icon_toggle': True,
    #                                         }),
    #                                     }