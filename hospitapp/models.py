from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import TimeField
from django.test import override_settings


"""
###################################################################################
###################################################################################
                        CATALOGOS DE LA BASE DE DATOS
###################################################################################
###################################################################################
"""

# CATALOGO DE ESPECIALIDADES MEDICAS
class cat_especialidades(models.Model):
    especialidad = models.CharField(max_length=100, verbose_name='Especialidad')
    class Meta:
        verbose_name = 'Catalogo de Especialidades'
    
    def __str__(self):
        return self.especialidad

# CATALOGO DE ESCUELAS
class cat_escuelas(models.Model):
    escuela = models.CharField(max_length=100, verbose_name='Universidad')
    class Meta:
        verbose_name = 'Catalogo de Universidades'
    
    def __str__(self):
        return self.escuela
class cat_genero(models.Model):
    genero = models.CharField(max_length=50, verbose_name='Genero')
    class Meta:
        verbose_name = 'Catalogo de Generos'

# CATALOGO DE PARENTESCOS
class cat_parentesco(models.Model):
    parentesco = models.CharField(max_length=100, verbose_name='Parentesco')
    class Meta:
        verbose_name = 'Catalogo de Parentesco'

# CATALOGO DE MEDICAMENTOS
class cat_medicamentos(models.Model):
    grupo_terapeutico = models.ForeignKey('cat_grupos_terapeuticos', on_delete=models.CASCADE, verbose_name='Usada en ' )
    clave_univ= models.CharField(max_length=15, verbose_name='Clave (SAICA)')
    compuesto = models.CharField(max_length=400, verbose_name='Descripcion')
    unidad_medida = models.CharField(max_length=100, verbose_name='Unidad de Medida')

    class Meta:
        verbose_name = 'Catalogo de Medicamentos'

#CATALOGO DE GRUPOS TERAPEUTICOS PARA MEDICAMENTOS
class cat_grupos_terapeuticos (models.Model):
    nombre_grupo  = models.CharField(max_length=100, verbose_name='Grupos Terapeuticos')
    class Meta:
        verbose_name = 'Catalogo de Grupos Terapeuticos para Medicamentos'

#CATALOGO DE OPERACIONES
class cat_operaciones(models.Model):
    operacion = models.CharField(max_length=100, verbose_name='Operacion')
    cveCIE9 = models.CharField(max_length=100, verbose_name='Clave CIE9')
    nivel = models.IntegerField(verbose_name='Nivel')
    class Meta:
        verbose_name = 'Catalogo de Operaciones'


#CATALOGO DE ANALISIS CLINICOS
class cat_analisis(models.Model):
    analisis = models.CharField(max_length=100, verbose_name='Analisis Clinicos')
    class Meta:
        verbose_name = 'Catalogo de Analisis Clinicos'

#CATALOGO DE ENFERMEDADES
class cat_enfermedades(models.Model):
    SIS=(("ENFERMEDADES TRANSMISIBLES", "ENFERMEDADES TRANSMISIBLES"), ("CRÓNICAS DEGENERATIVAS", "CRÓNICAS DEGENERATIVAS"),
        ("OTRAS ENFERMEDADES","OTRAS ENFERMEDADES"), ("NO APLICA","NO APLICA"))
    clave = models.CharField(max_length=10, verbose_name='Clave de la enfermedad')
    nombre = models.CharField(max_length=150, verbose_name='Nombre de la enfermedad')
    clave_SIS = models.CharField(verbose_name = "Clave SIS", max_length= 100, choices=SIS, default = "")
    capitulo = models.ForeignKey('cat_capitulos_enfermedades', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Catalogo de Enfermedades'

#CATALOGO DE CAPITULOS PARA ENFERMEDADES
class cat_capitulos_enfermedades(models.Model):
    capitulo = models.CharField(max_length=100, verbose_name='Capitulo de Enfermedad')
    class Meta:
        verbose_name = 'Catalogo de Capitulos de Enfermedades'

#CATALOGO DE HOSPITALIZACIONES
class cat_hospitalizaciones(models.Model):
    motivo = models.CharField(max_length=100, verbose_name='Motivo de Entrada')

    class Meta:
        verbose_name = 'Catalogo de Motivos de Hospitalizacion'

#CATALOGO DE MATERIAL DE CURACION
class cat_matetrial_curacion(models.Model):
    clave = models.CharField(max_length=15, verbose_name='Clave')
    material = models.CharField(max_length=250, verbose_name='Descripcion')
    presentacion  = models.CharField(max_length=100, verbose_name='Presentacion')
    usado_en = models.ForeignKey('cat_servicios', on_delete=models.CASCADE, verbose_name='Usado en')

    class Meta:
        verbose_name = 'Catalogo de Material de Curacion'

#CATALOGO DE SERVICIOS O ESPECIALIAD PARA USO DE MATERIAL DE CURACION
class cat_servicios(models.Model):
    servicio = models.CharField(max_length=100, verbose_name='Uso de Material')

    class Meta:
        verbose_name = 'Catalogo de usos de Material de Curacion'

#CATALOGO DE ETS (ENFERMEDADES DE TRANSMISION SEXUAL)
class cat_ets (models.Model):
    Nombre = models.CharField(max_length=1000, verbose_name='Nombre de la ETS')
    def __str__(self):
        return self.Nombre
    class Meta:
        verbose_name = 'Enfermedades de Transmision Sexual (ETS)'

"""
###################################################################################
###################################################################################
                TABLAS PRIMARIAS Y SECUNDARIAS DE LA BASE DE DATOS
###################################################################################
###################################################################################
"""

# ABSTRACCION DE USUARIO
class User(AbstractUser):
    rfc = models.CharField(max_length=13)
    es_paciente = models.BooleanField(default=False)
    es_enfermera = models.BooleanField(default=False)
    es_doctor = models.BooleanField(default=False)
    es_farmacia = models.BooleanField(default=False)
    es_admin = models.BooleanField(default=False)
    es_secretaria = models.BooleanField(default=False)

    def __str__(self):
        cadena=self.first_name+" "+self.last_name
        return cadena
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
# PERFIL DEL PERSONAL MEDICO 
class medical_staff(models.Model):
    user= models.ForeignKey('User', on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, verbose_name='Telefono')
    cedula_prof = models.CharField(max_length=15, verbose_name='Cedula Profesional')
    fecha_nac = models.DateField(verbose_name='Fecha de Nacimiento')
    id_especialidad = models.ForeignKey('cat_especialidades', on_delete=models.CASCADE, verbose_name='Especialidad')
    id_escuela = models.ForeignKey('cat_escuelas', on_delete=models.CASCADE, verbose_name='Universidad')
    modulo = models.IntegerField(verbose_name='Modulo donde da consulta')
    activo = models.BooleanField(default = True, verbose_name='Activo')
    class Meta:
        verbose_name = 'Perfil Personal Medico'
        verbose_name_plural = 'Perfiles de Personal Medico'

# PERFIL DE LOS PACIENTES Y AFILIADOS
class patients(models.Model):
    sexo=(("MASCULINO", "MASCULINO"), ("FEMENINO", "FEMENINO"))
    user= models.ForeignKey('User', on_delete=models.CASCADE)
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
    #rfc_vinculado = user= models.ForeignKey('User', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Perfil Paciente'
        verbose_name_plural = 'Perfiles de Pacientes'


"""
###################################################################################
                                EXPEDIENTE CLINICO
###################################################################################
"""
# ALERGIAS DE LOS PACIENTES A MEDICAMENTOS
class alergies(models.Model):
    user= models.ForeignKey('User', on_delete=models.CASCADE)
    alergia_a = models.ForeignKey('cat_medicamentos', on_delete=models.CASCADE,verbose_name='Alergia a')
    class Meta:
        verbose_name = 'Alergias del Paciente'
        verbose_name_plural = 'Alergias de los Pacientes'

# OPERACIONES A LOS PACIENTES
class operations(models.Model):
    user= models.ForeignKey('User', on_delete=models.CASCADE)
    operacion_recibida = models.ForeignKey('cat_operaciones', on_delete=models.CASCADE,verbose_name='operacion recibida')
    medico_responsable = models.ForeignKey('medical_staff', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Operaciones del Paciente'
        verbose_name_plural = 'Operaciones de los Pacientes'

class analysis(models.Model):
    user= models.ForeignKey('User', on_delete=models.CASCADE)
    analisis_hecho = models.ForeignKey('cat_analisis', on_delete=models.CASCADE,verbose_name='analisis hechos')
    medico_responsable = models.ForeignKey('medical_staff', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Analisis Clinicos hechos al Paciente'
        verbose_name_plural = 'Analisis Clinicos hechos a los Pacientes'

"""
###################################################################################
                                ANTECEDENTES
###################################################################################
"""
# ANTECEDENTES QUE SE LE TOMAN AL PACIENTE POR PRIMERA VEZ
class antecedentes_medicos(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    cardiovasculares = models.BooleanField(verbose_name ='Problemas Cardiacos')
    pulmonares = models.BooleanField(verbose_name ='Problemas Pulmonares')
    digestivos = models.BooleanField(verbose_name ='Problemas Digestivos')
    renales = models.BooleanField(verbose_name ='Problemas Renales')
    quirurgicos = models.BooleanField(verbose_name ='Ha tenido Operaciones')
    transfusiones = models.BooleanField(verbose_name ='Ha tenido transfusiones')
    alcoholismo = models.BooleanField(verbose_name ='Ha padecido alcoholismo')
    tabaquismo = models.BooleanField(verbose_name ='Ha padecido tabaquismo')
    drogas = models.BooleanField(verbose_name ='Problemas de Drogradiccion')
    inmunizaciones = models.BooleanField(verbose_name ='Se ha vacunado')
    padre_vivo = models.BooleanField(verbose_name ='Su padre vive')
    madre_vivo = models.BooleanField(verbose_name ='Su madre vive')
    hnos_Tiene = models.BooleanField(verbose_name ='Tiene hermanos')
    hnos_cuantos = models.IntegerField(verbose_name ='Numero de hermanos')
    enfermeades_padre = models.CharField(max_length=500, verbose_name = 'Enfermedades del Padre')
    enfermeades_madre = models.CharField(max_length=500, verbose_name = 'Enfermedades de la Madre')
    enfermeades_hnos = models.CharField(max_length=500, verbose_name = 'Enfermedades de los Hermanos')
    otras_anotaciones = models.CharField(max_length=1000, verbose_name = 'Otras Anotaciones')
    class Meta:
        verbose_name = 'Antecedentes del paciente'
        verbose_name_plural = 'Antecedentes de los pacientes'

# ANTECEDENTES GINECOLOGICOS QUE SE LE TOMAN AL PACIENTE POR PRIMERA VEZ
class antecedentes_ginecologicos(models.Model):
    sangrado = (('Eumenorrea - regla escasa','Eumenorrea - regla escasa'),
                ('Hipermenorrea - reglas abundantes.','Hipermenorrea - reglas abundantes.'),
                ('Amenorrea - ausencia de menstruación','Amenorrea - ausencia de menstruación'),
                ('Polihipermenorrea - regla frecuente y abundante','Polihipermenorrea - regla frecuente y abundante'),
                ('Oligohipomenorrea - regla a largos intervalos y escasa','Oligohipomenorrea - regla a largos intervalos y escasa'),
                ('Oligohipermenorrea - reglas poco frecuentes y abundantes','Oligohipermenorrea - reglas poco frecuentes y abundantes'),
                ('Polihipomenorrea - reglas frecuentes y escasas','Polihipomenorrea - reglas frecuentes y escasas'),
                ('Hipermenorrea dolorosa - regla abundante y dolorosa', 'Hipermenorrea dolorosa - regla abundante y dolorosa'),
                ('Metrorragias. Hemorragias endometriales irregulares y acíclicas', 'Metrorragias. Hemorragias endometriales irregulares y acíclicas')
                )
    frec = (('Regular','Regular'),('Irregular','Irregular'))
    anticonceptivos = ( (('El preservativo'),('El preservativo')),
                        (('El espermicida'),('El espermicida')),
                        (('El preservativo femenino'),('El preservativo femenino')),
                        (('El diafragma'),('El diafragma')),
                        (('La esponja vaginal'),('La esponja vaginal')),
                        (('La píldora'),('La esponja vaginal')),
                        (('La minipíldora Progestágeno'),('La minipíldora Progestágeno')),
                        (('La píldora del día después (PDS)'),('La píldora del día después (PDS)')),
                        (('El adhesivo anticonceptivo'),('El adhesivo anticonceptivo')),
                        (('El anillo vaginal'),('El anillo vaginal')),
                        (('El anticonceptivo inyectable'),('El anticonceptivo inyectable')),
                        (('El implante anticonceptivo'),('El implante anticonceptivo')),
                        (('Dispositivo intrauterino (DIU)'),('Dispositivo intrauterino (DIU)')),
                        (('Vasectomía'),('Vasectomía')),
                        (('Ligadura de trompas'),('Ligadura de trompas')),
                        (('Método del calendario menstrual'),('Método del calendario menstrual')),
                        (('Coito interrumpido'),('Coito interrumpido')),
                        (('Moco cervical'),('Moco cervical')),
                        (('Lactancia materna'),('Lactancia materna'))
                            )
    user = models.IntegerField(verbose_name='Usuario')
    menarquia = models.IntegerField(verbose_name='Edad Primera Mestruacion')
    ritmo= models.IntegerField(verbose_name='Dias aproximados entre cada Mestruacion')
    FUM = models.DateField(auto_now=False, auto_now_add=False, verbose_name = 'Fecha de Ultima Mestruacion', null = True, blank = True)
    Duracion = models.IntegerField(verbose_name='Dias aproximados que tarda la Mestruacion')
    Cant_Sangre = models.CharField(verbose_name = "Cantidad de Sangre", max_length= 100, choices=sangrado, default = "")
    frecuencia = models.CharField(verbose_name = "Frecuencia de Mestruacion", max_length= 50, choices=frec, default = "")
    dolor = models.BooleanField(verbose_name ='Presencia de Dolor en la Mestruacion')
    gestaciones = models.IntegerField(verbose_name='Numero de Gestaciones')
    partos = models.IntegerField(verbose_name='Numero de Partos')
    fup = models.DateField( auto_now=False, verbose_name = 'Fecha de Ultimo Parto', null = True, blank = True)
    abortos = models.IntegerField(verbose_name='Numero de Abortos')
    fua = models.DateField( auto_now=False, auto_now_add=False, verbose_name = 'Fecha de Ultimo Aborto',  null = True, blank = True)
    cesareas = models.IntegerField(verbose_name='Numero de Cesareas')
    fuc = models.DateField( auto_now=False, auto_now_add=False, verbose_name = 'Fecha de Ultima Cesarea', null = True, blank = True)
    fupapa = models.DateField( auto_now=False, auto_now_add=False, verbose_name = 'Fecha de Ultimo Papanicolau',  null = True, blank = True)
    ets = models.ManyToManyField(cat_ets)
    inicio_sexo = models.IntegerField(verbose_name='Edad de Inicio Sexual')
    frecuencia_sexo = models.IntegerField(verbose_name='Frecuencia de relaciones por semana')
    num_parejas = models.IntegerField(verbose_name='Numero de Parejas sexuales')
    metodo_anticonceptivo = models.CharField(verbose_name = "Metodos Anticonceptivos", max_length= 100, choices=anticonceptivos, default = "")
    problemas_sexo = models.CharField(max_length=500, verbose_name='Problemas Sexuales', null = True, blank = True)
    menopausia = models.BooleanField(verbose_name ='Ya presentó la menopausia')
    edad_menopausia = models.IntegerField(verbose_name='Edad que tuvo la menopausia',null = True, blank = True)

    class Meta:
        verbose_name = 'Antecedentes Ginecologicos de la paciente'
        verbose_name_plural = 'Antecedentes Ginecologicos de las pacientes'


#FALTA LA TABLA OPERACION A REALIZAR:
# orden, id_medico, tipo_operacion, sala_operacion, 
# material_a_usar (TABLA)
# personal a usar (TABLA)
"""
###################################################################################
                                    CONSULTA
###################################################################################
"""

# INDICADORES QUE SE TOMAN EN ENFERMERIA ANTES DE LA CONSULTA
class indicadores_pre(models.Model):
    estados_nutri = (   ('No tiene desnutrición','No tiene desnutrición'),
                        ('Riesgo de denutrición','Riesgo de denutrición'),
                        ('Desnutrición moderada','Desnutrición moderada'),
                        ('Desnutrición Grave','Desnutrición Grave'),
                        ('Sobrepeso','Sobrepeso'),
                        ('Obesidad','Obesidad')
                        )
    paciente = models.ForeignKey('User',on_delete=models.CASCADE,verbose_name='Paciente', related_name='Paciente')
    Fecha =  models.DateField(auto_now=True, auto_now_add=False, verbose_name='Fecha')
    Hora  = models.TimeField(auto_now=True, auto_now_add=False, verbose_name ='Hora')
    enfermera = models.ForeignKey('User',on_delete=models.CASCADE,verbose_name='Enfermera',related_name='Enfermera')
    peso = models.FloatField(verbose_name ='Peso en kgs')
    talla = models.FloatField(verbose_name ='Talla en mts')
    imc = models.FloatField(verbose_name ='Indice de Masa Corporal (IMC)')
    circ_abdominal = models.FloatField(verbose_name ='Circunferencia Abdominal')
    presion = models.FloatField(verbose_name ='Presion Sanguinea')
    frec_cardiaca = models.IntegerField(verbose_name ='Frecuencia Cardiaca')
    frec_respiratoria  = models.IntegerField(verbose_name ='Frecuencia Respiratoria')
    temperatura = models.FloatField(verbose_name ='Temperatura en Grados °C')
    saturacion_o2  = models.FloatField(verbose_name ='Saturación de Oxigeno en %')
    glucemia_capilar = models.FloatField(verbose_name ='Glucemia Capilar')
    nutricion = models.CharField(verbose_name = 'Estado Nutricional', max_length= 40, choices=estados_nutri, default = "")
    seguimiento_hospitalario = models.BooleanField(verbose_name='Segumiento Hospitalizado', default=False)
    class Meta:
        verbose_name = 'Indicadores del paciente'
        verbose_name_plural = 'Indicadores de los pacientes'

# DATOS QUE SE TOMAN AL PASAR EL PACIENTE A CONSULTA CON SU MEDICO
class consulta(models.Model):
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    id_medico = models.ForeignKey('medical_staff', verbose_name=("Medico"), on_delete=models.CASCADE)
    urgencia = models.BooleanField(verbose_name='Es consulta de Urgencias', default=False)
    fecha = models.DateField( auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    id_indicadores = models.ForeignKey('indicadores_pre', verbose_name=("Indicadores"), on_delete=models.CASCADE) 
    presentacion = models.CharField(max_length=1000, verbose_name='Presentacion del Paciente', help_text='Corroborar que es el paciente')
    #SOAP
    subjetivo = models.CharField(max_length=1000, verbose_name='Subjetivo del Paciente', help_text='Lo que dice el paciente')
    objetivo = models.CharField(max_length=1000, verbose_name='Objetivo del Paciente', help_text='Lo que se ve en el paciente') 
    evaluacion = models.CharField(max_length=1000, verbose_name='Evaluacion del Paciente', help_text='Lo que el medico cree tiene el paciente')
    plan = models.CharField(max_length=1000, verbose_name='Plan para el Paciente', help_text='Lo que se hara con el paciente')
    #SOAP
    pronostico = models.CharField(max_length=1000, verbose_name='Pronostico del Paciente', help_text='Se espera o no el regreso del paciente')
    tratamiento_no_farm = models.CharField(max_length=2000, verbose_name='Indicaciones', help_text='Tratamiento no farmacologico')
    id_enfermedad  = models.ForeignKey('cat_enfermedades', verbose_name=("Enfermedad"), on_delete=models.CASCADE)
    hospitalizacion = models.BooleanField(verbose_name='Hospitalizar', default=False)
    programado = models.BooleanField(verbose_name='Hospitalzacion programada', default=False)
    nota_medica_hospitalizado = models.BooleanField(verbose_name='Nota Medica', default=False)
    #si se hospitaliza usa receta a fuerzas
    receta = models.BooleanField(verbose_name='Receta', default=False)
    #PRESENTACION (PLANTILLA)
    #Se presenta paciente Masculino/Femenino 
    # de XX años de edad 
    # de X.XX de estatura y 
    # XXX de peso, 
    # de nombre FULANITO DE MENGANITO DE TAL, 
    # con domicilio en XXXXXXXX y 
    # numero de telefono XXXXXXXX,  

    class Meta:
        verbose_name = 'Consulta realizada al paciente'
        verbose_name_plural = 'Consultas realizadas a los pacientes'

# RECETA MEDICA SI SE AMERITA EN LA CONSULTA
class receta(models.Model):
    id_consulta = models.ForeignKey("consulta", on_delete=models.CASCADE, related_name='id_consulta')
    id_medicamento  = models.ForeignKey("cat_medicamentos", verbose_name=("Medicamento"), on_delete=models.CASCADE)
    indicaciones = models.CharField(max_length=500, blank=False, verbose_name='Indicaciones')

    class Meta:
        verbose_name = 'Recetas al paciente'
        verbose_name_plural = 'Recetas a los pacientes'


"""
###################################################################################
                                HOSPITALIZACION
###################################################################################
"""
# HOSPITALIZACION EN CASO DE SER NECESARIO
class hospitalizacion(models.Model):
    paciente = models.ForeignKey("patients", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha Ingreso')
    hora = models.TimeField(auto_now=True, verbose_name='Hora Ingreso')
    motivo = models.ForeignKey("cat_hospitalizaciones", on_delete=models.CASCADE,verbose_name='Motivo') 
    consulta_referencia = models.ForeignKey("consulta", on_delete=models.CASCADE, related_name='consulta_referencia')
    urgencia = models.BooleanField(verbose_name='Urgencia', default=False)
    cirugia = models.BooleanField(verbose_name='Cirugia', default=False)
    cama = models.CharField(max_length=10, verbose_name = "Cama")
    dieta = models.CharField(max_length=200, verbose_name = "Dieta")
    medico_responsable = models.ForeignKey("medical_staff", on_delete=models.CASCADE, verbose_name='Medico Responsable') 
    familiar_responsable = models.CharField(max_length=200, verbose_name = "Familiar")
    parentesco = models.ForeignKey("cat_parentesco", on_delete=models.CASCADE, verbose_name='Parentesco') 
    numero_telefono  = models.CharField(max_length=50, verbose_name = "Telefono")
    #receta medicamentos
    class Meta:
        verbose_name = 'Hospitalizacion del paciente'
        verbose_name_plural = 'Hospitalizacion de los pacientes'

class seguimiento (models.Model):
    Turnos = (("Matutino","Matutino"),("Vespertino","Vespertino"),("Nocturno","Nocturno"))
    Estado = (('Bueno','Bueno'),('Regular','Regular'),('Malo','Malo'))
    tipo_venoclisis = ( ('Sello de herparina','Sello de herparina'),
                        ('vena permeable para 8 horas','vena permeable para 8 horas'),
                        ('vena permeable para 12 horas','vena permeable para 12 horas'),
                        ('vena permeable para 24 horas','vena permeable para 24 horas'),
                        )
    tipo_sonda = (  ('Sonda Vesical Foley','Sonda Vesical Foley'),
                    ('Sonda Nasograstrica','Sonda Nasograstrica'),
                    ('Sonda Nelaton','Sonda Nelaton'),
                    ('Sonda Intestinal','Sonda Intestinal'),
                    ('Sonda Rectal','Sonda Rectal')
                    )
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    Turno = models.CharField(verbose_name = 'Turno', max_length= 10, choices=Turnos, default = "")
    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    requiere_limpieza_ropa = models.BooleanField(verbose_name='Cambio de Ropa de Cama y Demas', default =False)
    administrar_medicamentos = models.BooleanField(verbose_name='Administracion de Medicamentos', default =False)
    edo_salud = models.CharField(verbose_name = 'Estado de Salud', max_length= 10, choices=Estado, default = "")
    aloja_conjunto =models.BooleanField(verbose_name='Alojamiento Conjunto', default =False)
    venoclisis = models.BooleanField(verbose_name='Venoclisis', default =False)
    tipo_venoclisis =  models.CharField(verbose_name = 'Tipo Venoclisis', max_length= 30, choices=tipo_venoclisis, default = "")
    control_fluidos = models.BooleanField(verbose_name='Control de Fluidos', default =False)
    cant_fluidos = models.IntegerField(verbose_name='Cantidad de fluidos')
    control_termico = models.BooleanField(verbose_name='Control Termico', default =False)
    signos_vitales = models.ForeignKey("indicadores_pre", on_delete=models.CASCADE)
    vigilancia_extrema = models.BooleanField(verbose_name='Vigilancia Extrema', default =False)
    vigilar_sangrado = models.BooleanField(verbose_name='Vigilar Sangrado', default =False)
    sondas = models.BooleanField(verbose_name='Sonda', default =False)
    sonda_tipo = models.CharField(verbose_name = 'Tipo de Sonda', max_length= 50, choices=tipo_sonda, default = "")
    transfusion = models.BooleanField(verbose_name='Transfusion', default =False)
    paquetes_globulares = models.IntegerField(verbose_name='Paquetes globulares')
    destrostix =models.IntegerField(verbose_name='Destrostis')
    cuidado_especial = models.BooleanField(verbose_name='Cuidado Especial', default =False)
    ce_indicaciones = models.CharField(max_length=300, verbose_name='Indicaciones de cuidado especial')
    oxigeno = models.BooleanField(verbose_name='Oxigeno', default =False)
    oxigeno_lt_min = models.IntegerField(verbose_name='Litros por minuto')
    preoperatorio = models.BooleanField(verbose_name='Preoperatorio', default =False)
    #SI ES SI DEBEN LIGARSE LOS ANALISIS PREOPERATORIOS
    examenes_laboratorio = models.BooleanField(verbose_name='Examenes de Laboratorio', default =False)
    #SI ES SI, LISTAR LOS DEL DIA ORDENADOS POR LA  HORA
    estudios = models.BooleanField(verbose_name='Estudios', default =False)
    #SI ES SI, LISTAR LOS DEL DIA ORDENADOS POR LA  HORA
    otros = models.CharField(max_length=500, verbose_name='Otras Indicaciones')
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')

#NOTA MEDICA (HECHA POR EL MEDICO)
class nota_medica(models.Model):
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    id_consulta = models.ForeignKey("consulta", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')

#SU RESPECTIVA ALTA
class alta_hospitalizacion(models.Model):
    opcion_alta =(  ('Alta prematura','Alta prematura'),
                    ('Alta médica por mejoría','Alta médica por mejoría'),
                    ('Alta médica definitiva','Alta médica definitiva'),
                    ('Alta por traslado','Alta por traslado'),
                    ('Alta médica transitoria','Alta médica transitoria'),
                    ('Alta médica voluntaria','Alta médica voluntaria'),
                    ('Alta por abandono del tratamiento','Alta por abandono del tratamiento'),
                    ('Alta forzosa','Alta forzosa'),
                    ('Alta por defunción o fallecimiento','Alta por defunción o fallecimiento'),
                    ('Alta por fuga','Alta por fuga'),
                    ('Alta médica deportiva','Alta médica deportiva'))

    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    # Lista de los analisis realizados durante la hospitalizacion
    # Lista de los estudios realizados durante la hospitalizacion
    motivo_alta = models.CharField(verbose_name = 'Motivo de Alta', max_length= 100, choices = opcion_alta, default = "")
    diagnostico = models.CharField(max_length=500, verbose_name='Diagnostico al Alta')
    curado = models.BooleanField(verbose_name='Curado', default =False)
    dieta = models.CharField(max_length=1000, verbose_name='Dieta Especial')
    restricciones = models.CharField(max_length=1000, verbose_name='Restricciones')
    dispositivos_ayuda = models.CharField(max_length=500, verbose_name='Dispositivos de Ayuda')
    cuidados_heridas = models.CharField(max_length=1000, verbose_name='Cuidado de Heridas')
    indicaciones_indicadores = models.CharField(max_length=1000, verbose_name='Instrucciones para tomar los inicadores')
    sintomas_peligro = models.CharField(max_length=1000, verbose_name='Sintomas de Riesgo')
    cita_seguimiento = models.CharField(max_length=100, verbose_name='Cita para Seguimiento')
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    #receta medicamentos

# ANALISIS EN CASO DE SER NECESARIO
class solicitud_laboratorio (models.Model):
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    medico_solicita = models.ForeignKey('medical_staff', verbose_name=("Medico solicitante"), on_delete=models.CASCADE)
    tipo_analisis = models.ForeignKey('cat_analisis', verbose_name=("Analisis"), on_delete=models.CASCADE) 
    urgencia = models.BooleanField(verbose_name='Urgencia', default =False)
    hospitalizado =  models.BooleanField(verbose_name='Hospitalizado', default =False)
    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    atendido = models.BooleanField(verbose_name='atendido', default =False)

#RESULTADOS DE ANALISIS
class resultados_laboratorio (models.Model):
    paciente  = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    referencia = models.ForeignKey('solicitud_laboratorio', verbose_name=("Paciente"), on_delete=models.CASCADE)
    texto_descriptivo = models.CharField( max_length=2000, verbose_name=("Descripcion"))
    mediciones = models.CharField( max_length=5000, verbose_name=("Resultados"))
    medical_staff_lab  = models.ForeignKey('medical_staff', verbose_name=("Medico Elaboró"), on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')

    # ESPECIALISTA EN CASO DE SER NECESARIO
class solicitud_especialista (models.Model):
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    medico_solicita = models.ForeignKey('medical_staff', verbose_name=("Medico solicitante"), on_delete=models.CASCADE)
    tipo_especialidad = models.ForeignKey('cat_especialidades', verbose_name=("Especialista solicitado"), on_delete=models.CASCADE) 
    urgencia = models.BooleanField(verbose_name='Urgencia', default =False)
    hospitalizado =  models.BooleanField(verbose_name='Hospitalizado', default =False)
    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    atendido = models.BooleanField(verbose_name='atendido', default =False)

# SOLICITUD DE ESTUDIOS CLINICOS
class solicitud_estudios (models.Model):
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    medico_solicita = models.ForeignKey('medical_staff', verbose_name=("Medico solicitante"), on_delete=models.CASCADE)
    tipo_estudio = models.ForeignKey('cat_operaciones', verbose_name=("Estudio solicitado"), on_delete=models.CASCADE, limit_choices_to={'nivel':1,'nivel':2} )  
    urgencia = models.BooleanField(verbose_name='Urgencia', default =False)
    hospitalizado =  models.BooleanField(verbose_name='Hospitalizado', default =False)
    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    atendido = models.BooleanField(verbose_name='atendido', default =False)

#RESULTADOS DE ESTUDIOS CLINICOS
class resultados_estudios (models.Model):
    paciente  = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    referencia = models.ForeignKey('solicitud_estudios', verbose_name=("Paciente"), on_delete=models.CASCADE)
    texto_descriptivo = models.CharField( max_length=2000, verbose_name=("Descripcion"))
    mediciones = models.CharField( max_length=5000, verbose_name=("Resultados"))
    medical_staff_lab  = models.ForeignKey('medical_staff', verbose_name=("Medico Elaboró"), on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')

# SOLICITUD DE OPERACION
class solicitud_operacion (models.Model):
    id_paciente = models.ForeignKey('patients', verbose_name=("Paciente"), on_delete=models.CASCADE)
    medico_solicita = models.ForeignKey('medical_staff', verbose_name=("Medico solicitante"), on_delete=models.CASCADE)
    tipo_estudio = models.ForeignKey('cat_operaciones', verbose_name=("Estudio solicitado"), on_delete=models.CASCADE, limit_choices_to={'nivel':3} )  
    urgencia = models.BooleanField(verbose_name='Urgencia', default =False)
    fecha_programada = models.DateField(auto_now=True, verbose_name='Fecha Programada')
    hospitalizado =  models.BooleanField(verbose_name='Hospitalizado', default =False)
    id_hospitalizacion = models.ForeignKey("hospitalizacion", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    atendido = models.BooleanField(verbose_name='atendido', default =False)


# MATERIAL A USAR EN OPERACION
class material_operacion(models.Model):
    id_solicitud_operacion = models.ForeignKey('solicitud_operacion', verbose_name=("Operaciones"), on_delete=models.CASCADE)
    id_material_operacion =  models.ForeignKey('material_operacion', verbose_name=("Material de Operacion"), on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name='Cantidad')

# PERSONAL A USAR EN OPERACION
class personal_operacion(models.Model):
    id_solicitud_operacion = models.ForeignKey('solicitud_operacion', verbose_name=("Operaciones"), on_delete=models.CASCADE)
    id_personal_operacion =  models.ForeignKey('material_operacion', verbose_name=("Material de Operacion"), on_delete=models.CASCADE)

    
#STOCK DE MATERIAL POR AREA
class material_areas (models.Model):
    opciones_areas = (  ('Enfermería','Enfermería'),
                        ('Carro Rojo','Carro Rojo'),
                        ('Urgencias','Urgencias'),
                        ('Hospitalizacion','Hospitalizacion'))
    opcion_farmacia = (('Medicamento','Medicamento'),('Material de Curación','Material de Curación'))
    area  = models.CharField(verbose_name = 'Area', max_length= 50, choices = opciones_areas, default = "")
    cantidad  = models.IntegerField(verbose_name='Cantidad')
    tipo_material = models.CharField(verbose_name = 'Tipo Material', max_length= 50, choices = opcion_farmacia, default = "")
    id_farmacia = models.ForeignKey('farmacia', verbose_name=("Medicamento / Material de Curación"), on_delete=models.CASCADE)
    
#ATENCION ENFERMERIA
class atencion_enfermeria(models.Model):
    fecha = models.DateField( auto_now=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now=True, verbose_name='Hora')
    id_paciente = models.ForeignKey('patients', on_delete=models.CASCADE, verbose_name = "Paciente")
    enfermera = models.ForeignKey('medical_staff', on_delete=models.CASCADE, verbose_name="Enfermera")
    procedimiento = models.ForeignKey('cat_operaciones', verbose_name=("Procedimiento de Enfermería"), on_delete=models.CASCADE, limit_choices_to={'nivel':1} )  
    class Meta:
        verbose_name = 'Atención de enfermería'

#MATERIAL USADO EN ENFERMERIA
class material_usado_enfermeria(models.Model):
    id_atencion = models.ForeignKey('atencion_enfermeria', on_delete=models.CASCADE, verbose_name="Atencion")
    material_usado = models.ForeignKey('material_areas', on_delete=models.CASCADE, verbose_name="Material_usado", limit_choices_to='Enfermería')
    cantidad = models.IntegerField(verbose_name="Cantidad")

#SOLICITUDES DE MATERIAL Y MEDICAMENTOS
class pedir_material(models.Model):
    opciones_areas = (  ('Enfermería','Enfermería'),
                        ('Carro Rojo','Carro Rojo'),
                        ('Urgencias','Urgencias'),
                        ('Hospitalizacion','Hospitalizacion'))
    opcion_farmacia = (('Medicamento','Medicamento'),('Material de Curación','Material de Curación'))
    area  = models.CharField(verbose_name = 'Area', max_length= 50, choices = opciones_areas, default = "")
    cantidad  = models.IntegerField(verbose_name='Cantidad')
    tipo_material = models.CharField(verbose_name = 'Tipo Material', max_length= 50, choices = opcion_farmacia, default = "")    
    medico_solicita = models.ForeignKey('medical_staff', on_delete=models.CASCADE, verbose_name="Solicitado por")


# FARMACIA 
class farmacia(models.Model):
    opcion = (('Medicamento','Medicamento'),('Material de Curación','Material de Curación'))
    tipo_med = models.CharField(verbose_name = 'Tipo de Stock', max_length= 50, choices = opcion, default = "")
    id_material= models.ForeignKey('cat_matetrial_curacion', verbose_name=("Material de Curación"), on_delete=models.CASCADE)
    id_medicamento = models.ForeignKey('cat_medicamentos', verbose_name=("Medicamento"), on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    Lote = models.CharField(verbose_name = 'Lote', max_length= 15)
    Fecha_caducidad = models.DateField(auto_now=False, auto_now_add=False, verbose_name = "Fecha de caducidad")

# SURTIR RECETAS
class surtir_recetas(models.Model):
    receta = receta
    farmacia = farmacia
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha_surtido = models.DateField(auto_now=True, auto_now_add=False, verbose_name = "Fecha")
    hora_surtido = models.TimeField(auto_now=True, auto_now_add=False, verbose_name = 'Hora')
    
#AGENDAR CITAS
class cita_paciente (models.Model):
    id_paciente = models.ForeignKey('User', verbose_name=("Paciente"), related_name="Paciente_Cita", on_delete=models.CASCADE)
    fecha_cita = models.DateField(auto_now=False, auto_now_add=False, verbose_name = "Fecha de la cita")
    id_hora = models.ForeignKey('cita_turno', on_delete = models.CASCADE, verbose_name = "Hora de la Cita")
    id_doctor = models.ForeignKey('User', verbose_name=("Doctor/Especialista"), related_name ="Doctor_Cita", on_delete=models.CASCADE)

#CITAS (HORAS) POR TURNOS
class cita_turno (models.Model):
    Turnos = (("Matutino","Matutino"),("Vespertino","Vespertino"),("Nocturno","Nocturno"))
    hora = models.CharField(max_length=30, verbose_name = "Hora de la Cita")
    turno = models.CharField(verbose_name = 'Turno', max_length= 10, choices=Turnos, default = "")
    def __str__(self):
        cadena=self.hora
        return cadena
"""
###################################################################################
###################################################################################
                    MENSAJERO DE LA BASE DE DATOS (Opcional)
###################################################################################
###################################################################################
"""
# MENSAJERO INTERNO DEL SISTEMA
class mensajero(models.Model):
    remitente = models.ForeignKey('User',on_delete=models.CASCADE,verbose_name='ENVIA', related_name='Remitente')
    destinatario = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='DESTINO',related_name='Destinatario')
    titulo = models.CharField(max_length=100, verbose_name='ASUNTO')
    mensaje = models.CharField(max_length=1000, verbose_name='MENSAJE')
    enviado = models.DateTimeField(auto_now = True)
    leido = models.BooleanField(verbose_name='Leido',default = False)

    #se agrega esto para filtrar los datos de operaciones y otros estudios   limit_choices_to = { 'nivel': 1 }
    
    # def __str__(self):
    #     return f'Perfil de {self.user}'
    
    # class Meta:
    #     verbose_name = 'Perfil'
    #     verbose_name_plural = 'Perfiles'

    # Colors=(("NEGRO", "Negro"), ("BLANCO", "Blanco"), ("GRIS","Gris"))
    # txtColor = models.CharField(verbose_name = "Color de Texto", max_length= 15, choices=Colors, default = "Negro")