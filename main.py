from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
ARCHIVO_JSON = 'registros.json'

# Asegurarnos de que el archivo JSON exista al arrancar
if not os.path.exists(ARCHIVO_JSON):
    with open(ARCHIVO_JSON, 'w') as f:
        json.dump([], f)

# 1. RUTA PRINCIPAL (El menú)
@app.route('/')
def inicio():
    return render_template('index.html')

# 2. RUTA PARA NUEVO REGISTRO (Muestra el formulario HTML)
@app.route('/nuevo')
def nuevo_registro():
    return render_template('nuevo.html')

# 3. RUTA PARA GUARDAR LOS DATOS (Recibe la info del formulario)
@app.route('/guardar', methods=['POST'])
def guardar_registro():
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    
    # Leemos el JSON de forma segura
    try:
        with open(ARCHIVO_JSON, 'r') as f:
            registros = json.load(f)
    except json.JSONDecodeError:
        # Si el archivo está vacío o corrupto, empezamos una lista nueva
        registros = []
    
    nuevo_dato = {"titulo": titulo, "contenido": contenido}
    registros.append(nuevo_dato)
    
    with open(ARCHIVO_JSON, 'w') as f:
        json.dump(registros, f, indent=4)
    
    return redirect(url_for('inicio'))

# 4. RUTA PARA VER REGISTROS (Lee el JSON)
@app.route('/ver')
def ver_registros():
    # Por ahora lo mostraremos simple, luego lo hacemos bonito
    with open(ARCHIVO_JSON, 'r') as f:
        registros = json.load(f)
    
    texto = "<h1>Registros en Base de Datos:</h1>"
    for r in registros:
        texto += f"<p><strong>{r['titulo']}</strong>: {r['contenido']}</p>"
    texto += "<a href='/'>Volver</a>"
    return texto

if __name__ == '__main__':
    app.run(debug=True)