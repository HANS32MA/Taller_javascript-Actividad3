from flask import Flask #Se utiliza para importar la libreria de Flask
from flask_cors import CORS #Permite configurar políticas de CORS en aplicaciones Flask
from flask import jsonify, request #El método JSONIFY simplifica la creación de respuestas JSON
                                #El REQUEST permite el acceso a toda la información que pasa desde el navegador del cliente al servidor

import pymysql # permite la interacción con bases de datos MySQL escrito completamente en Python

app = Flask(__name__) # Sirve para que Flask sepa dónde buscar recursos como plantillas y archivos estáticos

CORS(app) # es un mecanismo de seguridad que permite a las aplicaciones web interactuar con recursos de otros dominios

# Funcion para conectarnos a la base de datos de mysql
# Función para conectarse a la base de datos MySQL
def conectar():
    return pymysql.connect(
        host='localhost', 
        user='root', 
        passwd='',  
        db='gestor_contrasena', 
        charset='utf8mb4'
    )

# -----------------------------------
# Funciones de autenticación y registro de usuarios
# -----------------------------------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(data)
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = "SELECT * FROM baul WHERE clave = %s and email = %s"
        cursor.execute(query, (password, email))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify({"success": True, "message": "Inicio de sesión exitoso"})
        else:
            return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401
    except Exception as ex:
        print(ex)
        return jsonify({"success": False, "message": "Error al conectar con la base de datos"}), 500

from flask import request, jsonify
# Assuming 'conectar' is your database connection function
# and you have necessary imports like psycopg2 if using PostgreSQL

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_username = data.get('new-username')
    new_password = data.get('new-password')
    new_email = data.get('new-email') # Added email field

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute("SELECT * FROM baul WHERE usuario = %s", (new_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"success": False, "message": "El usuario ya existe"}), 400

        # Check if email exists
        cursor.execute("SELECT * FROM baul WHERE email = %s", (new_email,))
        existing_email = cursor.fetchone()
        if existing_email:
            return jsonify({"success": False, "message": "El email ya existe"}), 400

        query = "INSERT INTO baul (usuario, clave, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (new_username, new_password, new_email))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Registro exitoso"})
    except Exception as ex:
        print(ex)
        return jsonify({"success": False, "message": "Error al registrar el usuario"}), 500
    
    
# Ruta para consulta general del baul de contraseñas
@app.route("/")
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul """)
        datos = cur.fetchall()
        data = []
        
        for row in datos:
            dato = {
                'id_baul': row[0],
                'usuario': row[2],
                'clave': row[3],
                'email': row[4]
            }
            data.append(dato)
            
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Ruta para consulta individual de un registro en el baúl
@app.route("/consulta_individual/<usuario>/", methods=['GET'])
def consulta_individual(usuario):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul WHERE usuario = %s """, (usuario,)) # Buscar por nombre de usuario
        datos = cur.fetchone()

        cur.close()
        conn.close()

        if datos:
            dato = {
                'id_baul': datos[0],
                'usuario': datos[1],
                'clave': datos[2],
                'email': datos[3]
            }
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para agragar nuevos datos a la base de datos
@app.route('/registro/', methods=['POST'])
def registro():
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(""" INSERT INTO baul (usuario, clave, email) VALUES (%s, %s, %s, %s) """, 
                    (request.json['usuario'], request.json['clave'], request.json['email']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para eliminar datos de la base de datos
@app.route('/eliminar/<codigo>', methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(""" DELETE FROM baul WHERE id_baul = %s """, (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route('/actualizar/<codigo>', methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(""" UPDATE baul SET documento = %s, usuario = %s, clave = %s, email = %s WHERE id_baul = %s """,
                    (request.json['usuario'], request.json['clave'], request.json['email'], codigo))
        conn.commit() # Guarda de forma permanente los cambios realizados en una transacción de base de datos o tabla
        cur.close() # Cierra un cursor, es decir, finaliza el uso de un cursor en una aplicación
        conn.close() # Cierra la conexión con la base de datos
        
         # Retornar un mensaje de éxito
        return jsonify({'mensaje': 'Registro Actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# el COMMIT es el proceso de convertir un conjunto de cambios provisionales en permanentes
if __name__ == '__main__':
    app.run(debug=True)