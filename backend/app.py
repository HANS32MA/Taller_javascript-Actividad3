from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
import pymysql

app = Flask(__name__)
# Nos permite acceder desde una api externa
CORS(app)

# Funcion para conectarnos a la base de datos de mysql
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn
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
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)
            
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Ruta para consulta individual de un registro en el baúl
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul where id_baul='{0}' """.format(codigo))
        datos = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if datos != None:
           dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
           return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
           return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

@app.route('/registro/', methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute(""" insert into baul (plataforma, usuario, clave) values \
        ('{0}', '{1}', '{2}')""".format(request.json['plataforma'], \
                                      request.json['usuario'], request.json['clave']))
        conn.commit()  # Para confirmar la inserción de la información
        cur.close()
        conn.close()
        print(x)
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route('/eliminar/<codigo>', methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute(""" delete from baul where id_baul='{0}'""".format(codigo))
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
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        
        x = cur.execute(""" update baul set plataforma='{0}', usuario='{1}', clave='{2}' where 
        id_baul='{3}'""".format(request.json['plataforma'], request.json['usuario'], 
                               request.json['clave'], codigo))
        
        conn.commit()
        cur.close()
        conn.close()
        
         # Retornar un mensaje de éxito
        return jsonify({'mensaje': 'Registro Actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    app.run(debug=True)