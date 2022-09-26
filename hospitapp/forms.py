from select import select
from ssl import Options
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model
import datetime
from hospitapp.models import cita_paciente, cita_turno, medical_staff,antecedentes_medicos, antecedentes_ginecologicos, cat_ets
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

class PatientProfile(forms.ModelForm):
    user= forms.CharField(widget=forms.HiddenInput())
    telefono = models.CharField(max_length=20, verbose_name='Telefono')
    direccion = models.CharField(max_length=200, verbose_name='Direccion')
    fecha_nac = models.DateField(verbose_name='Fecha de Nacimiento')
    id_genero = models.ForeignKey('cat_genero', on_delete=models.CASCADE) #LGBTQ
    id_sexo = models.CharField(verbose_name = "Sexo", max_length= 10, choices=sexo)
    tipo_sangre = models.CharField(max_length=5, verbose_name='Tipo de Sangre')
    derechohabiente = models.BooleanField(default = False, verbose_name='Derechohabiente')
    afiliado = models.BooleanField(default = False, verbose_name='Afiliado' )
    parentesco = models.ForeignKey('cat_parentesco', on_delete=models.CASCADE)
    activo = models.BooleanField(default = True, verbose_name='Activo')

    class Meta:
        model = patients
        fields = ('telefono','direccion', 'fecha_nac', 'id_genero', 'id_sexo', 'tipo_sangre', 'derechohabiente', 'afiliado', 'parentesco', 'activo')


class LoginForm(forms.ModelForm):
    username = forms.CharField( 
                                label='Usuario',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
                                label='Contraseña',
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})))

    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password'].help_text = None


sql = 'SELECT hms.id, au.first_name, au.last_name FROM  hospitapp_medical_staff hms, auth_user au WHERE hms.user_id = au.id AND  au.es_doctor  = TRUE'
qs = medical_staff.objects.raw (sql)

class RegistroCitasForm(forms.ModelForm):
    
    fecha_cita = input_formats=['%d/%m/%Y %H:%M']

    id_hora = forms.ModelChoiceField(
                            label='Hora', 
                            queryset=cita_turno.objects.all()
                            )
    id_doctor = forms.ModelChoiceField(
                            label='Doctor', 
                            #queryset = User.__str__(User.objects.fiilter(es_doctor =True))
                            queryset = User.objects.filter(es_doctor =True)
                            )
    id_paciente = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = cita_paciente
        fields = ('fecha_cita', 'id_hora', 'id_doctor','id_paciente',)
    


class ProfileForm(forms.ModelForm):
    username = forms.CharField( 
                                label='Usuario',
                                max_length=15, 
                                help_text=('Requerido. 15 caracteres o menos, letras, digitos y @/./+/-/_ solamente.'), 
                                validators=[username_validator], 
                                error_messages={'unique': ("Ya existe un usuario con ese nombre de Usuario.")}, 
                                #readonly = True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly', }))
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
                                #readonly = True,
                                widget=(forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly',})))
    email = forms.EmailField(label = 'Email',
                                max_length=50, 
                                min_length=10, 
                                required=True, 
                                widget=(forms.EmailInput(attrs={'class': 'form-control'}))
                                )                                
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','rfc','email',)
        #exclude = ['password1','password2']

class AntecedentesForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    cardiovasculares = forms.BooleanField(
                                            label='¿Tiene Problemas Cardiacos?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    pulmonares = forms.BooleanField(
                                            label='¿Tiene Problemas Pulmonares?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    digestivos = forms.BooleanField(
                                            label='¿Tiene Problemas Digestivos?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    renales =forms.BooleanField(
                                            label='¿Tiene Problemas Renales?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    quirurgicos = forms.BooleanField(
                                            label='¿Ha tenido Operaciones?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    transfusiones = forms.BooleanField(
                                            label='¿Ha tenido Transfusiones?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    alcoholismo = forms.BooleanField(
                                            label='¿Ha padecido Alcoholismo?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    tabaquismo = forms.BooleanField(
                                            label='¿Ha padecido Tabaquismo?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    drogas = forms.BooleanField(
                                            label='¿Ha padecido Problemas de Drogas?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    
    inmunizaciones = forms.BooleanField(
                                            label='¿Se Ha Vacunado?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    padre_vivo = forms.BooleanField(
                                            label='¿Padre Vivo?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    madre_vivo = forms.BooleanField(
                                            label='¿Madre Viva?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    hnos_Tiene = forms.BooleanField(
                                            label='¿Tiene Hermanos?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    hnos_cuantos = forms.IntegerField(
                                            label ='Numero de Hermanos',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))
    enfermeades_padre = forms.CharField(
                                label = 'Enfermedades del Padre',
                                max_length=500, 
                                min_length=0, 
                                widget=(forms.Textarea(attrs={'class': 'form-control'})))
    enfermeades_madre =forms.CharField(
                                label = 'Enfermedades de la Madre',
                                max_length=500, 
                                min_length=0, 
                                widget=(forms.Textarea(attrs={'class': 'form-control'})))

    enfermeades_hnos = forms.CharField(
                                label = 'Enfermedades de Hermano(s)',
                                max_length=500, 
                                min_length=0, 
                                widget=(forms.Textarea(attrs={'class': 'form-control'})))
    otras_anotaciones = forms.CharField(
                                label = 'Otras Anotaciones',
                                max_length=1000, 
                                min_length=0, 
                                widget=(forms.Textarea(attrs={'class': 'form-control'})))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        #self.fields['nombre_del_campo'].required = False
        self.fields['cardiovasculares'].required = False
        self.fields['pulmonares'].required = False
        self.fields['digestivos'].required = False
        self.fields['renales'].required = False
        self.fields['quirurgicos'].required = False
        self.fields['transfusiones'].required = False
        self.fields['alcoholismo'].required = False
        self.fields['tabaquismo'].required = False
        self.fields['drogas'].required = False
        self.fields['inmunizaciones'].required = False
        self.fields['padre_vivo'].required = False
        self.fields['madre_vivo'].required = False
        self.fields['hnos_Tiene'].required = False
        self.fields['hnos_cuantos'].required = False
        self.fields['enfermeades_padre'].required = False
        self.fields['enfermeades_madre'].required = False
        self.fields['enfermeades_hnos'].required = False
        self.fields['otras_anotaciones'].required = False
    class Meta:
        model = antecedentes_medicos
        fields = (  'cardiovasculares', 'pulmonares', 'digestivos', 'renales', 'quirurgicos',
                    'transfusiones', 'alcoholismo', 'tabaquismo', 'drogas', 'inmunizaciones',
                    'padre_vivo', 'madre_vivo', 'hnos_Tiene', 'hnos_cuantos', 'enfermeades_padre',
                    'enfermeades_madre', 'enfermeades_hnos', 'otras_anotaciones',)

class GinecologiaAntecedentesForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    
    menarquia = forms.IntegerField(
                                            label ='Edad Primera Mestruacion',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    ritmo= forms.IntegerField(
                                            label ='Dias aproximados entre cada Mestruacion',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))
    #Fecha Ultima Mestruacion
    FUM = input_formats=['%d/%m/%Y %H:%M'] 
        
    Duracion = forms.IntegerField(
                                            label ='Dias aproximados que tarda la Mestruacion',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    Cant_Sangre = forms.ChoiceField(choices=antecedentes_ginecologicos.sangrado, label = 'Cantidad de Sangrado')

    frecuencia = forms.ChoiceField(choices=antecedentes_ginecologicos.frec, label = 'Frecuencia de Mestruacion')
        
    dolor = forms.BooleanField(
                                            label='Presencia de Dolor en la Mestruacion',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    
    gestaciones = forms.IntegerField(
                                            label ='Numero de Gestaciones',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    partos = forms.IntegerField(
                                            label ='Numero de Partos',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))
    #Fecha Ultimo Parto
    fup = input_formats=['%d/%m/%Y %H:%M']
    abortos = forms.IntegerField(
                                            label ='Numero de Abortos',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))
    #Fecha Ultimo Aborto
    fua = input_formats=['%d/%m/%Y %H:%M']
    
    cesareas = forms.IntegerField(
                                            label ='Numero de Cesareas',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))
    #Fecha Ultima Cesarea
    fuc = input_formats=['%d/%m/%Y %H:%M']
    #Fecha ultimo Papanicolau
    fupapa = input_formats=['%d/%m/%Y %H:%M']
        
    ets = forms.ModelMultipleChoiceField(
                                widget = forms.CheckboxSelectMultiple,
                                label='Enfermedades de Transimisión Sexual',
                                queryset = cat_ets.objects.all()
                                )
    inicio_sexo = forms.IntegerField(
                                            label ='Edad de Inicio Sexual',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    frecuencia_sexo = forms.IntegerField(
                                            label ='Frecuencia de relaciones por semana',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    num_parejas = forms.IntegerField(
                                            label ='Numero de Parejas Sexuales',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    metodo_anticonceptivo = forms.ChoiceField(choices=antecedentes_ginecologicos.anticonceptivos, label = 'Metodos Anticonceptivos')
    
    problemas_sexo = forms.CharField(
                                label = 'Problemas Sexuales',
                                max_length=500, 
                                min_length=0, 
                                widget=(forms.Textarea(attrs={'class': 'form-control'})))
                            
    menopausia = forms.BooleanField(
                                            label='¿Ya presentó la menopausia?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))

    edad_menopausia = forms.IntegerField(
                                            label ='Edad que tuvo la menopausia',
                                            widget=(forms.NumberInput(attrs={'class': 'form-control'})))


    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['menarquia'].required = False
        self.fields['ritmo'].required = False
        self.fields['FUM'].required = False
        self.fields['Duracion'].required = False
        self.fields['Cant_Sangre'].required = False
        self.fields['frecuencia'].required = False
        self.fields['dolor'].required = False
        self.fields['gestaciones'].required = False
        self.fields['partos'].required = False
        self.fields['fup'].required = False
        self.fields['abortos'].required = False
        self.fields['fua'].required = False
        self.fields['cesareas'].required = False
        self.fields['fuc'].required = False
        self.fields['fupapa'].required = False
        self.fields['ets'].required = False
        self.fields['inicio_sexo'].required = False
        self.fields['frecuencia_sexo'].required = False
        self.fields['num_parejas'].required = False
        self.fields['metodo_anticonceptivo'].required = False
        self.fields['problemas_sexo'].required = False
        self.fields['menopausia'].required = False
        self.fields['edad_menopausia'].required = False
    
    class Meta:
        model = antecedentes_ginecologicos
        fields = (  
                    'user',             'menarquia',    'ritmo' ,               'FUM',              'Duracion',     'Cant_Sangre',
                    'frecuencia',       'dolor',        'gestaciones',          'partos',           'fup',          'abortos',
                    'fua',              'cesareas',     'fuc',                  'fupapa',           'ets',          
                    'inicio_sexo',      'frecuencia_sexo',  'num_parejas',  'metodo_anticonceptivo','problemas_sexo',   'menopausia',   'edad_menopausia', 
                    
                )

    