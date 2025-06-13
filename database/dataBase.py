import pymysql
import json
from sqlalchemy import create_engine, Column, Integer,BigInteger,String,ForeignKey,DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import re
import app
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func
from collections import Counter



# Datos for conexion a base de datos
username = "cc5002"
host = "localhost"
puerto = 3306
NombreBaseDeDatos = "tarea2"
password = "programacionweb"
db_charset = "utf8"

# conection
# si quiero postgres cambio a mysql a postgres..+ motor que es pymysql
# charset para emojis tildes 
DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{puerto}/{NombreBaseDeDatos}""?charset=utf8mb4"

# crea la conexión a la base de datos usando la librería PyMySQL
engine = create_engine(DATABASE_URL,echo=False, future=True)
#crear una sesion, se usa para abrir y cerrar conexiones con la base de datos
SessionLocal = sessionmaker(bind=engine)
# es la clase base de la cual heredan todos los modelos para crear tablas (se vio en auxiliar)
Base = declarative_base()

# --- models --- 
# cada clase debe abstraerse, tienen el mismo comportamiento de la Base
# cada clase hereda de declarative_Base, es la clase base

# cuando no tiene que ser null, nullable = false, sino true
# relationships es parte de SQLalchemy


# (me falta revisar)
class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = "comuna"
    id = Column(Integer, primary_key=True, autoincrement=False)  # ¡Importante: no usar autoincrement!
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)

    region = relationship("Region", back_populates="comunas")
    actividades = relationship("Actividad", back_populates="comuna")

class Actividad(Base):
    __tablename__ = "actividad"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime)
    descripcion = Column(String(500))

    comuna = relationship("Comuna", back_populates="actividades")
    fotos = relationship("Foto", back_populates="actividad", cascade="all, delete-orphan")
    contactos = relationship("ContactarPor", back_populates="actividad", cascade="all, delete-orphan")
    temas = relationship("ActividadTema", back_populates="actividad", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="actividad", cascade="all, delete-orphan")


class Foto(Base):
    __tablename__ = "foto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship("Actividad", back_populates="fotos")

class ContactarPor(Base):
    __tablename__ = "contactar_por"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship("Actividad", back_populates="contactos")

class ActividadTema(Base):
    __tablename__ = "actividad_tema"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15))
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship("Actividad", back_populates="temas")

# tabla-comentario.sql
class Comentario(Base):
    __tablename__  = "comentario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship("Actividad", back_populates="comentarios")



# crea todas las tablas que aun no existen en la db segun las clases que heredan de base (las que tienen Base)
Base.metadata.create_all(engine)

# obligatorio, debe cumplir con
# formato de dirección de
# email. Largo máximo 100.
def validate_email(email): 
    regexEmail = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    email = email.strip()
    if email == "" or len(email)>100:
         return False
    return bool(regexEmail.match(email))


# obligatorio, largo máximo 200.
def validate_name(name):
     if name =="" or len(name)>200:
          return False
     return True

#opcional, largo máximo 100.
def validate_sector(sector):
     sector = sector.strip()
     if len(sector)>100:
          return False
     return True
# opcional, debe cumplir con
# formato de número de
# teléfono móvil
# +NNN.NNNNNNNN, por
# ejemplo: +569.12345678
def validate_number(number):
     if number =="":
          return True
     # es .trim() }de JS en python
     number = number.strip()
     ExprRegularNumber = re.compile(r'^\+\d{3}\.\d{8}$')
     return  bool(ExprRegularNumber.match(number))

# opcional. Máximo 5. El input
# de información de ID o URL
# debe permitir mínimo 4
# caracteres y máximo 50.
def validate_contactar(formulario):
    medios = ['whatsapp', 'instagram', 'telegram', 'X', 'tiktok', 'otra']
    seleccionados = 0
    for medio in medios:
        # Si el checkbox fue marcado, estará presente
        if medio in formulario:
            campo_id = f"id_{medio}"
            valor = formulario.get(campo_id, "").strip()

            if not (4 <= len(valor) <= 50):
                return False  #inválido
            seleccionados += 1

    # 0 a 5 selecciones válidas, true
    return 0 <= seleccionados <= 5
     



            

# obligatorios
# quitarle espacios y mayusculas
def normalize(text):
    return text.strip().lower()

def validate_region_comuna(comuna_id, region_nombre):
    session = SessionLocal()
    try:
        comuna_obj = session.query(Comuna).filter_by(id=int(comuna_id)).first()
        if not comuna_obj:
            print("No se encontró la comuna con id:", comuna_id)
            return False

        nombre_db = normalize(comuna_obj.region.nombre)
        nombre_form = normalize(region_nombre)

        print("REGIÓN en BD:", repr(nombre_db))
        print("REGIÓN en formulario:", repr(nombre_form))

        return nombre_db == nombre_form
    finally:
        session.close()


# HoraInicio 
# obligatorio. Debe cumplir con
# el formato año-mes-dia
# hora:minuto

# HoraTermino
# opcional. Debe cumplir con el
# formato año-mes-dia
# hora:minuto. Si se informa,
# debe ser mayor a día y hora
# de inicio.
def validate_dates(inicio, final):
    # obligatorio
    if not inicio:
        return False
    # try para que no se caiga el programa si no se convierte el formato 
    try:
        fmt = "%Y-%m-%dT%H:%M"  # format del input de agregaActividad.html, datetime-local
        dt_inicio = datetime.strptime(inicio, fmt)

        if not final:
            return True

        dt_final = datetime.strptime(final, fmt)

        if dt_final <= dt_inicio:
            return False

        return True
    # si es una excepcion, lanza un error y retorna False
    except ValueError:
            # Si no se puede convertir a datetime, retorna False
        return False



# obligatorio, mínimo 1 foto y
# máximo 5 fotos.
def validate_foto(fotos): 
    maximo_fotos = 5
    max_tamano = 2 * 1024 * 1024  # 2 MB
    if not fotos or len(fotos) == 0:
        return False
    if len(fotos) > maximo_fotos:
        return False
    for archivo in fotos:
        if not archivo.mimetype.startswith("image/"):
            return False
        # Validar tamaño
        archivo.seek(0, 2)
        tamanio = archivo.tell()
        archivo.seek(0)
        if tamanio > max_tamano:
            return False
    return True
     

# opcional.
def validate_descripcion(descripcion):
     if len(descripcion) >800:
          return False
     return True

# obligatorio. Al menos 1
# opción. Si selecciona otro, el
# input debe permitir como
# mínimo 3 caracteres y
# máximo 15
# input.name = 'otroTema'  JS
def validaTema(formulario):
    arreglo = [
        'musica',
        'deporte',
        'ciencias',
        'religion',
        'politica',
        'tecnologia',
        'juegos',
        'baile',
        'comida',
        'otro',
    ]

    if not any(tema in formulario for tema in arreglo):
        return False

    if 'otro' in formulario:
        otro_tema = formulario.get('otroTema', '').strip() 
        if len(otro_tema) < 3 or len(otro_tema) > 15:
            return False

    return True


    



# para crear una actividad
def create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    try:
        nueva_actividad = Actividad(
            comuna_id=comuna_id,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            dia_hora_inicio=dia_hora_inicio,
            dia_hora_termino=dia_hora_termino,
            descripcion=descripcion
        )
        session.add(nueva_actividad)
        session.commit()
        return nueva_actividad.id  # retorna el id 
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# para agregar los temas a la actividad
def agregar_fotos_a_actividad(actividad_id, lista_nombres_archivos):
    session = SessionLocal()
    try:
        for nombre_archivo in lista_nombres_archivos:
            nueva_foto = Foto(
                ruta_archivo=f"static/fotos/{nombre_archivo}",
                nombre_archivo=nombre_archivo,
                actividad_id=actividad_id
            )
            session.add(nueva_foto)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    
# agregar contactos a la actividad
def agregar_contactos_a_actividad(actividad_id, formulario):
    session = SessionLocal()
    try:
        medios = ['whatsapp', 'instagram', 'telegram', 'X', 'tiktok', 'otra']
        for medio in medios:
            identificador = formulario.get(f"id_{medio}", "").strip()
            if identificador:
                nuevo_contacto = ContactarPor(
                    nombre=medio,
                    identificador=identificador,
                    actividad_id=actividad_id
                )
                session.add(nuevo_contacto)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def agregar_temas_a_actividad(actividad_id, formulario):
    session = SessionLocal()
    try:
        temas_form = [
            'musica', 'deporte', 'ciencias', 'religion', 'politica',
            'tecnologia', 'juegos', 'baile', 'comida', 'otro'
        ]
        # pues hay tildes dentro de la base de datos de sql
        mapeo_enum = {
            'musica': 'música',
            'deporte': 'deporte',
            'ciencias': 'ciencias',
            'religion': 'religión',
            'politica': 'política',
            'tecnologia': 'tecnología',
            'juegos': 'juegos',
            'baile': 'baile',
            'comida': 'comida',
            'otro': 'otro'
        }

        for tema in temas_form:
            if tema in formulario:
                tema_enum = mapeo_enum[tema]
                glosa = formulario.get("otroTema", "").strip() if tema == 'otro' else None

                nuevo_tema = ActividadTema(
                    tema=tema_enum,
                    glosa_otro=glosa if glosa else None,
                    actividad_id=actividad_id
                )
                session.add(nuevo_tema)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def obtener_actividades_paginadas(offset, limit):
    session = SessionLocal()
    try:
        total = session.query(Actividad).count()
        actividades = session.query(Actividad).offset(offset).limit(limit).all()

        resultado = []
        for a in actividades:
            fecha_termino = (
                (a.dia_hora_inicio + timedelta(hours=3)) if a.dia_hora_termino is None else a.dia_hora_termino
            )
            total_fotos = len(a.fotos)

            resultado.append({
                'id': a.id,
                'nombre': a.nombre,
                'email': a.email,
                'celular': a.celular,
                'comuna': a.comuna.nombre,
                'region': a.comuna.region.nombre,
                'sector': a.sector,
                'fecha_inicio': a.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
                'fecha_termino': fecha_termino.strftime('%Y-%m-%d %H:%M') if fecha_termino else '---',
                'total_fotos': total_fotos
            })
        return resultado, total
    finally:
        session.close()


def obtener_detalle_actividad(actividad_id):
    session = SessionLocal()
    try:
        a = session.query(Actividad).filter_by(id=actividad_id).first()
        if not a:
            return None

        return {
            'id': a.id,
            'nombre': a.nombre,
            'email': a.email,
            'sector': a.sector,
            'comuna': a.comuna.nombre,
            'celular': a.celular,
            'region': a.comuna.region.nombre,
            'fecha_inicio': a.dia_hora_inicio,
            'fecha_termino': a.dia_hora_termino,
            'descripcion': a.descripcion,
            'temas': [{'tema': t.tema, 'glosa_otro': t.glosa_otro} for t in a.temas],
            'contactos': [{'medio': c.nombre, 'dato': c.identificador} for c in a.contactos],
            'fotos': [f"/static/uploads/" + f.nombre_archivo for f in a.fotos],
            'total_fotos': len(a.fotos)  
        }
    finally:
        session.close()


def obtener_actividades_con_foto(limit=5):
    session = SessionLocal()
    try:
        actividades = session.query(Actividad).order_by(Actividad.dia_hora_inicio.desc()).limit(limit).all()
        resultado = []
        for a in actividades:
            fecha_termino = (
                (a.dia_hora_inicio + timedelta(hours=3)) if a.dia_hora_termino is None else a.dia_hora_termino
            )
            primera_foto = a.fotos[0].nombre_archivo if a.fotos else None
            resultado.append({
                'id': a.id,
                'nombre': a.nombre,
                'comuna': a.comuna.nombre,
                'sector': a.sector,
                'fecha_inicio': a.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
                'fecha_termino': fecha_termino.strftime('%Y-%m-%d %H:%M') if fecha_termino else '---',
                'foto_url': f"/static/uploads/{primera_foto}" if primera_foto else None
            })
        return resultado
    finally:
        session.close()




# El primero es un gráfico de líneas que informa la cantidad de 
# actividades por día. En el eje X muestra los días y en el eje Y muestra la 
# cantidad de actividades. 
def EstadisticasGrafico1():
    session = SessionLocal()
    try:
        actividades = session.query(Actividad.dia_hora_inicio).all()
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'] 
        #lunes=0, domingo=6
        conteo = Counter([a[0].weekday() for a in actividades if a[0] is not None]) 
        #Mapear índice numérico a nombre de día
        resultado = {dias_semana[i]: conteo.get(i, 0) for i in range(7)}
        return resultado
    finally:
        session.close()

# El segundo gráfico es un gráfico de torta que muestra el total de 
# actividades por tipo. 
def EstadisticasGrafico2():
    session = SessionLocal()
    temas_form = ['música', 'deporte', 'ciencias', 'religión', 'política',
                  'tecnología', 'juegos', 'baile', 'comida', 'otro']
    
    conteos = {}

    try:
        for tema in temas_form:
            cantidad = session.query(func.count(ActividadTema.id)).filter_by(tema=tema).scalar()
            conteos[tema] = cantidad
        return conteos
    finally:
        session.close()

from collections import defaultdict

def EstadisticasGrafico3():
    session = SessionLocal()
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]

    # Diccionario con tramos
    # esto lo hago, pues en vez de hacer un for para inicializar si la clave no existe, la creará y no fallará
    # se puede hacer con for tmb
    conteo = defaultdict(lambda: {'Mañana': 0, 'Mediodía': 0, 'Tarde': 0})
    try:
        actividades = session.query(Actividad.dia_hora_inicio).all()
        for (fecha,) in actividades:
            if fecha is None:
                continue
            mes = meses[fecha.month - 1]
            hora = fecha.hour
            if 6 <= hora < 12:
                tramo = 'Mañana'
            elif 12 <= hora < 18:
                tramo = 'Mediodía'
            else:
                tramo = 'Tarde'

            conteo[mes][tramo] += 1

        return conteo

    finally:
        session.close()


# validar nombre de comentario
# (caja de texto, obligatorio con largo mínimo 3 y máximo 80)
def validarComentarioNombre(nombre):
    nombre = nombre.strip()
    if len(nombre)<3 or len(nombre)>80:
        return False
    else:
        return True
# validar comentario de comentario
#  dato obligatorio con al menos 5 caracteres
# usamos 200 pues 4filas * 50columnas = 200 caracteres como max
def validarComentario(comentario):
    comentario = comentario.strip()
    if len(comentario) < 5:
        return False
    if len(comentario) > 200:
        return False
    return True

# agregar comentarios a la db
def agregar_comentario(nombre, texto, actividad_id):
    session = SessionLocal()
    try:
        nuevo_comentario = Comentario(
            nombre=nombre.strip(),
            texto=texto.strip(),
            fecha=datetime.now(),
            actividad_id=int(actividad_id)
        )
        session.add(nuevo_comentario)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error al guardar el comentario:", e)
        return False
    finally:
        session.close()

        
# obtener comentarios
def obtener_comentarios_por_actividad(actividad_id):
    session = SessionLocal()
    try:
        comentarios = session.query(Comentario).filter_by(actividad_id=actividad_id).order_by(Comentario.fecha.desc()).all()
        return [{
            "nombre": c.nombre,
            "texto": c.texto,
            "fecha": c.fecha.strftime("%Y-%m-%d %H:%M")
        } for c in comentarios]
    finally:
        session.close()