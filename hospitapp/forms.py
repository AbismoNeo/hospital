from select import select
from ssl import Options
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model
import datetime
from hospitapp.models import cita_paciente, cita_turno, medical_staff,antecedentes_medicos, antecedentes_ginecologicos, cat_ets, patients, cat_parentesco, cat_genero, cat_especialidades, cat_escuelas, cat_medicamentos,alergies, operations_history, cat_operaciones, indicadores_pre, cat_enfermedades, consulta
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

class PatientProfileForm(forms.ModelForm):
    user= forms.CharField(widget=forms.HiddenInput())
    telefono = forms.CharField(
                                label = 'Telefono',
                                max_length=15, 
                                min_length=10, 
                                required=True, 
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    direccion = forms.CharField(
                                label = 'Dirección',
                                max_length=200, 
                                required=False,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':3, 'cols':5 })))
    fecha_nac = input_formats=['%d/%m/%Y %H:%M'] 
    
    id_genero = forms.ModelChoiceField(
                            label='Genero', 
                            queryset=cat_genero.objects.all()
                            )

    id_sexo = forms.ChoiceField(choices=patients.sexo, label = 'Sexo')
    tipo_sangre = forms.CharField(
                                label = 'Tipo de Sangre',
                                max_length=5, 
                                required=True,
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    derechohabiente = forms.BooleanField(
                                            label='¿Es Derechohabiente?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    afiliado = forms.BooleanField(
                                            label='¿Es Afiliado?',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    parentesco = forms.ModelChoiceField(
                            label='Parentesco', 
                            queryset=cat_parentesco.objects.all()
                            )
    activo = forms.BooleanField(
                                            label='Activo',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    class Meta:
        model = patients
        fields = ('telefono','direccion', 'fecha_nac', 'id_genero', 'id_sexo', 'tipo_sangre', 'derechohabiente', 'afiliado', 'parentesco', 'activo')

class MedicalProfileForm(forms.ModelForm):
    user= forms.CharField(widget=forms.HiddenInput())
    telefono = forms.CharField(
                                label = 'Telefono',
                                max_length=15, 
                                min_length=10,
                                required=True,
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))

    cedula_prof = forms.CharField(
                                label = 'Cedula Profesional',
                                max_length=15, 
                                min_length=10,
                                required=True,
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))

    fecha_nac = input_formats=['%d/%m/%Y %H:%M'] 

    id_especialidad = forms.ModelChoiceField(
                            label='Especialidad', 
                            queryset=cat_especialidades.objects.all()
                            )

    id_escuela = forms.ModelChoiceField(
                            label='Universidad', 
                            queryset=cat_escuelas.objects.all()
                            )

    modulo = forms.IntegerField(
                                label ='Modulo de Consulta',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    activo = forms.BooleanField(
                                label='Activo',
                                widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    class Meta:
        model = medical_staff
        fields = ('user', 'telefono', 'cedula_prof', 'fecha_nac', 'id_especialidad', 'id_escuela', 'modulo', 'activo')

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

class alergiesForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    alergia_a = forms.ModelMultipleChoiceField(
                                widget = forms.CheckboxSelectMultiple,
                                label='Alergía a',
                                queryset = cat_medicamentos.objects.all()
                                )
    class Meta:
        model = alergies
        fields = ( 'user', 'alergia_a')

class operations_historyForm(forms.ModelForm):
    user= forms.CharField(widget=forms.HiddenInput())
    operacion_recibida = forms.ModelMultipleChoiceField(
                                widget = forms.CheckboxSelectMultiple,
                                queryset = cat_operaciones.objects.all()
                                )
    class Meta:
        model = operations_history
        fields = ( 'user', 'operacion_recibida')

class indicators_preForm(forms.ModelForm):

    paciente = forms.CharField(widget=forms.HiddenInput())
    Fecha =  forms.DateField(widget=forms.HiddenInput())
    Hora  = forms.TimeField(widget=forms.HiddenInput())

    enfermera = forms.ModelChoiceField(
                            label='Atendido por', 
                            queryset=User.objects.filter(es_doctor = True) | User.objects.filter(es_enfermera = True))

    peso = forms.FloatField(    label ='Peso en Kgs',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    talla = forms.FloatField(   label ='Talla en mts',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))
    
    imc = forms.FloatField(   label ='Indice de Masa Corporal (IMC)',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    circ_abdominal = forms.FloatField(   label ='Circunferencia Abdominal',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    presion = forms.FloatField(   label ='Presion Sanguinea',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    frec_cardiaca = forms.IntegerField(   label ='Frecuencia Cardiaca',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    frec_respiratoria  = forms.IntegerField(   label ='Frecuencia Respiratoria',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    temperatura = forms.FloatField(   label ='Temperatura en Grados °C',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    saturacion_o2  = forms.FloatField(   label ='Saturación de Oxigeno en %',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    glucemia_capilar = forms.FloatField(   label ='Glucemia Capilar',
                                widget=(forms.NumberInput(attrs={'class': 'form-control'})))

    nutricion = forms.ChoiceField(choices=indicadores_pre.estados_nutri, label = 'Estado Nutricional')

    seguimiento_hospitalario = forms.BooleanField(
                                            label='Segumiento Hospitalizado',
                                            widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))

    class Meta:
        model = indicadores_pre
        fields = ('__all__')  

class search_patientsForm(forms.Form):
    busqueda = forms.CharField(
                                max_length=200, 
                                required=False,
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    class Meta:
        fields = ['busqueda', ]
        labels = { "busqueda" : "" }
datenow = datetime.datetime.now()
class appointment_doctorForm(forms.ModelForm):
    id_paciente = forms.CharField(widget=forms.HiddenInput())
    id_medico = forms.CharField(widget=forms.HiddenInput())
    urgencia = forms.BooleanField(
                                    label='Consulta Urgencia',
                                    widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True'})))
    fecha =  forms.DateField(widget=forms.HiddenInput())
    hora  = forms.TimeField(widget=forms.HiddenInput())
    
    id_indicadores = forms.ModelChoiceField(
                            label='Indicadores del  día:', 
                            queryset=indicadores_pre.objects.filter(Fecha = datenow).filter(paciente = 2)
                            )
#    id_indicadores = models.ForeignKey('indicadores_pre', verbose_name=("Indicadores"), on_delete=models.CASCADE) 

    presentacion = forms.CharField(
                                label = 'Presentacion del Paciente',
                                max_length=1000, 
                                required=False,
                                #help_text ='Corroborar que es el paciente' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5,})))
    #SOAP
    subjetivo = forms.CharField(
                                label = 'Subjetivo del Paciente',
                                max_length=1000, 
                                required=False,
                                #help_text ='Lo que dice el paciente' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5, })))
    
    objetivo = forms.CharField(
                                label = 'Objetivo del Paciente',
                                max_length=1000, 
                                required=False,
                                #help_text ='Lo que se ve en el paciente' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5,})))
    
    evaluacion = objetivo = forms.CharField(
                                label = 'Evaluacion del Paciente',
                                max_length=1000, 
                                required=False,
                                #help_text ='Lo que el medico cree tiene el paciente' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5,})))
    
    plan = objetivo = forms.CharField(
                                label = 'Plan para el Paciente',
                                max_length=1000, 
                                required=False,
                                #help_text ='Lo que se hara con el paciente' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5,})))
    
    #SOAP
    
    pronostico = objetivo = forms.CharField(
                                label = 'Pronostico del Paciente',
                                max_length=1000, 
                                required=False,
                                #help_text ='Se espera el regreso o no del paciente' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5,'data-toggle':"tooltip", 'title':"Se espera o no el regreso pronto del paciente."})))
    
    tratamiento_no_farm = forms.CharField(
                                label = 'indicaciones',
                                max_length=2000, 
                                required=False,
                                #help_text ='Tratamiento no farmacologico' ,
                                widget=(forms.Textarea(attrs={'class': 'form-control', 'name':'body', 'rows':5, 'data-toggle':"tooltip", 'title':"Indicaciones no farmacologicas a seguir por el paciente"})))
    
    id_enfermedad  = forms.ModelChoiceField(
                            label='Enfermedad:', 
                            widget=forms.Select(attrs={'data-toggle':"tooltip", 'title':"Enfermedad posiblemente detectada al paciente",'font-size':'28px','wordwrap':'True' }),
                            queryset=cat_enfermedades.objects.all()
                                            )

    hospitalizacion = forms.BooleanField(
                                    label='Hospitalizar',
                                    widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True', 'data-toggle':"tooltip", 'title':"¿Se debe hospitalizar?"})))

    programado = forms.BooleanField(
                                    label='Hospitalización Programada',
                                    widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True', 'data-toggle':"tooltip", 'title':"¿Tenía una hospitaliacion programada?"})))
    
    nota_medica_hospitalizado = forms.BooleanField(
                                    label='Nota Medica',
                                    widget =(forms.CheckboxInput(attrs={'style':'width:20px;height:20px;','null':'True', 'blank':'True', 'data-toggle':"tooltip", 'title':"¿Es una nota medica?"})))
    #si se hospitaliza usa receta a fuerzas
    receta = id_paciente = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = consulta
        fields = '__all__'