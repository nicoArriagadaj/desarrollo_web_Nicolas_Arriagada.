from flask import Flask, render_template, request, redirect, url_for, session
from database import dataBase 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import filetype
import os

app = Flask(__name__)

# del aux  
app.secret_key = "s3cr3t_k3y"
UPLOAD_FOLDER = 'static/fotos'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/AgregarActividad')
def agregar():
    return render_template('AgregarActividad.html')

@app.route('/Estadisticas')
def estadisticas():
    return render_template('Estadisticas.html')

@app.route('/info')
def info():
    return render_template('infoOrdenada.html')

@app.route('/ListadoDeActividades')
def listado():
    return render_template('ListadoDeActividades.html')


@app.route('/AgregarActividad', methods=['POST'])
def agregar_actividad():
    # procesar datos del formulario
    email = request.form['email']
    region = request.form['regiones']
    comuna = request.form['comunas']
    sector = request.form['sector']
    name = request.form['name']
    number = request.form['number']
    # como en contactar hay multiples opciones, debo cambiarlo 
    contactar = request.form['contactar']
    DiaHoraInicio = request.form['DiaHoraInicio']
    DiaHoraTermino = request.form.get['DiaHoraTermino',None] # get para que no falle si no se ingresa
    description = request.form['descripción']
    tema = request.form['tema']
    fotos = request.files.getlist('Foto') 

    errors = []
    # aqui debo validar datos (me faltan algunos validadores)
    # Validaciones (usar funciones ya hechas)
    if not dataBase.validate_email(email):
        errors.append('Email inválido')
    if not dataBase.validate_name(name):
        errors.append('Nombre inválido')
    if not dataBase.validate_number(number):
        errors.append('Número inválido')
    if not dataBase.validate_dates(dia_hora_inicio, dia_hora_termino):
        errors.append('Fechas inválidas')
    if not dataBase.validate_foto(fotos):
        errors.append('Fotos inválidas')
    if not dataBase.validate_sector(sector):
        errors.append('Sector inválido')
    if not dataBase.validate_descripcion(description):
        errors.append('Descripción inválida')
    if not dataBase.validate_region_comuna(comuna, region):
        errors.append('Región o comuna inválida')
        # en temas, debo ver cuales se agregan
    if not dataBase.validate_tema(temas[0], otro_tema):
        errors.append('Tema inválido')
    # esta parte debo arreglarla, pues mi AgregarActividad.html en contactar tiene un select unico, no multiple.
    """ 
    for contacto in medios_contacto:
        if not dataBase.validate_contactar(contacto_otro if contacto == "otra" else contacto):
            errors.append('Contacto inválido') """

    if errors:
            # usamos render_template si hacemos get, y redirect cuando es post
            return render_template('AgregarActividad.html', errors=errors)

    # Conversión fechas a datetime
    fmt = "%Y-%m-%dT%H:%M"
    dia_hora_inicio = datetime.strptime(dia_hora_inicio, fmt)
    dia_hora_termino = datetime.strptime(dia_hora_termino, fmt) if dia_hora_termino else None

    # Guardar fotos
    from werkzeug.utils import secure_filename # para seguridad
    filenames = []
    for foto in fotos:
        filename = secure_filename(foto.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(ruta)
        filenames.append(filename)


        # Guardar actividad en base de datos
    dataBase.create_actividad(
        comuna_id=int(comuna),
        sector=sector,
        nombre=name,
        email=email,
        celular=number,
        dia_hora_inicio=dia_hora_inicio,
        dia_hora_termino=dia_hora_termino,
        descripcion=description,
    )
    # REDIRECT PARA CUANDO SE HAGA EL POST =  redirigir
    return redirect(url_for('index'))



    # validadores individuales
    for err in (
        dataBase.validate_email(email),
        dataBase.validate_name(name),
        dataBase.validate_sector(sector),
        dataBase.validate_number(number),
        dataBase.validate_contactar(contactar),
        dataBase.validate_region_comuna(region, comuna),
        dataBase.validate_descripcion(descripción),
        ):
        if err:
            errors.append(err)

    
    tema = request.form.get("tema")
    otro_tema = request.form.get("otroTema") # Nombre del Otro, que definimos en JS

    if not dataBase.validate_tema(tema, otro_tema):
      return render_template("AgregarActividad.html", error="Tema inválido")

    from werkzeug.utils import secure_filename   # para seguridad 
    for archivo in fotos:
        archivo.save(f"uploads/{secure_filename(archivo.filename)}")  # guardar en uploads

    # validadores de fechas
    dt_ini, dt_fin, err = dataBase.validate_date(DiaHoraInicio, DiaHoraTermino)
    if err:
        errors.append(err)

    if errors:
      return render_template(("AgregarActividad.html"))




    # Otros datos
    db = SessionLocal()
    return "Actividad agregada correctamente"  # o redirigir (aun tengo que ver esto)



if __name__ == '__main__':
    app.run(debug=True)