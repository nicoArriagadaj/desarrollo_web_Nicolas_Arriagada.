from flask import Flask, render_template


host = "localhost"
puerto = 3306
NombreBaseDeDatos = "tarea2"
username = "cc5002"
password = "programacionweb"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
