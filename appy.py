from flask import Flask, render_template, request, redirect

# Datos for conexion a base de datos
host = "localhost"
puerto = 3306
NombreBaseDeDatos = "tarea2"
username = "cc5002"
password = "programacionweb"

app = Flask(__name__)

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
    nombre = request.form['name']
    email = request.form['email']
    # Otros datos

    
    return "Actividad agregada correctamente"  # o redirigir (aun tengo que ver esto)


if __name__ == '__main__':
    app.run(debug=True)