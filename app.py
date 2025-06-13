from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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




# get
@app.route('/agregar_actividad')
def agregar():
    return render_template('AgregarActividad.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('Estadisticas.html')



@app.route('/api/estadisticas/dias_semana')
def datos_estadisticas_diasGrafico1():
    datos = dataBase.EstadisticasGrafico1()
    return jsonify(datos)


@app.route('/api/estadisticas/temas')
def datos_estadisticasGrafico2():
    datos = dataBase.EstadisticasGrafico2()
    return jsonify(datos)

@app.route('/api/estadisticas/Meses')
def datos_estadisticasGrafico3():
    datos = dataBase.EstadisticasGrafico3()
    return jsonify(datos)


#agregarComentario a la db
@app.route('/api/comentario', methods=['POST'])
def api_agregar_comentario():
    data = request.get_json()
    nombre = data.get("nombre", "").strip()
    comentario = data.get("comentario", "").strip()
    actividad_id = data.get("actividad_id", "").strip()
    errors = []
    # Validaciones igual que antes
    if not dataBase.validarComentarioNombre(nombre):
        errors.append("Nombre inválido (3-80 caracteres).")
    if not dataBase.validarComentario(comentario):
        errors.append("Comentario inválido (mín. 5 y max. 200 caracteres).")
    if not actividad_id.isdigit():
        errors.append("ID de actividad inválido.")
    if errors:
        return jsonify(success=False, errors=errors)
    try:
        dataBase.agregar_comentario(nombre, comentario, actividad_id)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, errors=[str(e)]), 500

@app.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
def api_listar_comentarios(actividad_id):
    comentarios = dataBase.obtener_comentarios_por_actividad(actividad_id)
    return jsonify(comentarios=comentarios)

@app.route('/info')
def info():
    actividad_id = request.args.get('id', type=int)
    if not actividad_id:
        actividad_id = request.args.get('actividad_id', type=int)
    if not actividad_id:
        return "ID de actividad no proporcionado", 400

    actividad = dataBase.obtener_detalle_actividad(actividad_id)
    if not actividad:
        return "Actividad no encontrada", 404

    return render_template('infoOrdenada.html', actividad=actividad)

# arreglar el problemad de que, dar una pagina invalida, redirecciona a 1, o a la ultima.
@app.route('/listado_de_actividades')
def listado():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1 

    if page < 1:
        page = 1

    actividades_por_pagina = 5
    offset = (page - 1) * actividades_por_pagina

    actividades, total = dataBase.obtener_actividades_paginadas(offset, actividades_por_pagina)
    total_paginas = (total + actividades_por_pagina - 1) // actividades_por_pagina

    # Si la página solicitada es mayor que el total de páginas, redirigir a la última
    if total_paginas > 0 and page > total_paginas:
        page = total_paginas
        offset = (page - 1) * actividades_por_pagina
        actividades, total = dataBase.obtener_actividades_paginadas(offset, actividades_por_pagina)

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
    