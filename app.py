from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




# Datos for conexion a base de datos
host = "localhost"
puerto = 3306
NombreBaseDeDatos = "tarea2"
username = "cc5002"
password = "programacionweb"

app = Flask(__name__)

# del aux  
app.secret_key = "s3cr3t_k3y"








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


@app.route('/agregar_actividad', methods=['POST'])
def agregar_actividad():
    # procesar datos del formulario
    email = request.form['email']
    region = request.form['regiones']
    comuna = request.form['comunas']
    sector = request.form['sector']
    name = request.form['name']
    number = request.form['number']
    contactar = request.form['contactar']
    DiaHoraInicio = request.form['DiaHoraInicio']
    DiaHoraTermino = request.form['DiaHoraTermino']
    descripción = request.form['descripción']
    tema = request.form['tema']
    foto = request.files['Foto']

    # validar datos del formulario
    emailValidation(email)
    nameValidation(name)
    regionValidation(region)
    comunaValidation(comuna)
    sectorValidation(sector)
    numberValidation(number)
    contactarValidation(contactar)
    DiaHoraInicioValidation(DiaHoraInicio)
    DiaHoraTerminoValidation(DiaHoraTermino)
    descripciónValidation(descripción)
    temaValidation(tema)
    fotoValidation(foto)











    # Otros datos

    
    return "Actividad agregada correctamente"  # o redirigir (aun tengo que ver esto)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://cc5002:programacionweb@localhost/tarea2'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)