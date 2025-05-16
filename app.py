from flask import Flask, render_template, request, redirect, url_for, session
from database import dataBase 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import filetype
import os

app = Flask(__name__)

UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_PATH, exist_ok=True) 
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

# del aux  
app.secret_key = "s3cr3t_k3y"


@app.route('/')
def index():
    mensaje = session.pop('mensaje_exito', None)# el que se recibe con session['mensaje_exito']
    actividades = dataBase.obtener_actividades_con_foto(limit=5) # Obtener las primeras 5 actividades para mostrar en el índice
    return render_template('index.html', mensaje=mensaje, actividades=actividades)





@app.route('/agregar_actividad')
def agregar():
    return render_template('AgregarActividad.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('Estadisticas.html')

@app.route('/info')
def info():
    actividad_id = request.args.get('id', type=int)
    if not actividad_id:
        return "ID de actividad no proporcionado", 400

    actividad = dataBase.obtener_detalle_actividad(actividad_id)
    if not actividad:
        return "Actividad no encontrada", 404

    return render_template('infoOrdenada.html', actividad=actividad)

@app.route('/listado_de_actividades')
def listado():
    page = int(request.args.get('page', 1))  # Página actual, por defecto 1
    actividades_por_pagina = 5
    offset = (page - 1) * actividades_por_pagina

    actividades, total = dataBase.obtener_actividades_paginadas(offset, actividades_por_pagina)

    total_paginas = (total + actividades_por_pagina - 1) // actividades_por_pagina  # Redondeo hacia arriba

    return render_template(
        'ListadoDeActividades.html',
        actividades=actividades,
        pagina_actual=page,
        total_paginas=total_paginas
    )


@app.route('/agregar_actividad', methods=['POST'])
def agregar_actividad():
    try:
        print("Contenido del formulario recibido:", request.form)
        email = request.form.get('email', '')
        region = request.form.get('regiones', '')
        comuna = request.form.get('comunas', '')
        sector = request.form.get('sector', '')
        name = request.form.get('name', '')
        number = request.form.get('number', '')
        DiaHoraInicio = request.form.get('DiaHoraInicio', '')
        DiaHoraTermino = request.form.get('DiaHoraTermino', '')
        description = request.form.get('descripción', '')
        fotos = request.files.getlist('Foto')
        errors = []
        if not dataBase.validate_email(email):
            errors.append('Email inválido')
        if not dataBase.validate_name(name):
            errors.append('Nombre inválido')
        if not dataBase.validate_number(number):
            errors.append('Número inválido')
        if not dataBase.validate_dates(DiaHoraInicio, DiaHoraTermino):
            errors.append('Fechas inválidas')
        if not dataBase.validate_foto(fotos):
            errors.append('Fotos inválidas')
        if not dataBase.validate_sector(sector):
            errors.append('Sector inválido')
        if not dataBase.validate_descripcion(description):
            errors.append('Descripción inválida')
        if not dataBase.validaTema(request.form):
           errors.append("Debe seleccionar al menos un tema válido.")
       
        # Validar comuna numérica antes de cualquier otra validación que la use
        if not comuna.isdigit():
           errors.append("Debe seleccionar una comuna válida.")
        else:
           if not dataBase.validate_region_comuna(comuna, region):
              errors.append('Región o comuna inválida')
        if not dataBase.validate_contactar(request.form):
            errors.append("Los datos de contacto no son válidos.")

        if errors:
            return render_template('AgregarActividad.html', errors=errors)

        fmt = "%Y-%m-%dT%H:%M"
        dia_hora_inicio = datetime.strptime(DiaHoraInicio, fmt)
        dia_hora_termino = datetime.strptime(DiaHoraTermino, fmt) if DiaHoraTermino else None

        from werkzeug.utils import secure_filename
        filenames = []
        for foto in fotos:
            if foto.filename:
                filename = secure_filename(foto.filename)
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(ruta)
                filenames.append(filename)

        actividad_id = dataBase.create_actividad(
            comuna_id=int(comuna),
            sector=sector,
            nombre=name,
            email=email,
            celular=number,
            dia_hora_inicio=dia_hora_inicio,
            dia_hora_termino=dia_hora_termino,
            descripcion=description,
        )

        dataBase.agregar_fotos_a_actividad(actividad_id, filenames)
        dataBase.agregar_contactos_a_actividad(actividad_id, request.form)
        dataBase.agregar_temas_a_actividad(actividad_id, request.form)


        session['mensaje_exito'] = "Actividad agregada exitosamente"
        return redirect(url_for('index'))

    except Exception as e:
        return f"Ocurrió un error inesperado: {e}", 400


if __name__ == '__main__':
    app.run(debug=True)
    