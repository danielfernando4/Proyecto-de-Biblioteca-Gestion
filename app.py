from flask import Flask, render_template, request, redirect, url_for, jsonify
from conectorPostgres import DatabaseConnector

app = Flask(__name__, template_folder="templates")


dsn = "dbname=BibliotecaEPN user=postgres password=RockoDB44 host=localhost port=5432"
db_conn = DatabaseConnector(dsn)
db_conn.initialize_connection_pool(minconn=1, maxconn=100)

@app.route("/")
def main():
    return "main"


@app.route("/base")
def base():
    return render_template("base.html")



@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        categoria = request.form['categoria']
        codigo = request.form['codigo']
        paginas = int(request.form['paginas'])
        fecha = request.form['fecha']
        autor = request.form['autor']
        facultad = request.form['facultad']
        cantidad = int(request.form['cantidad'])
        disponibles = int(request.form['disponibles'])

        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("CALL sp_registrar_libro(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (autor, titulo, categoria, codigo, paginas, fecha, facultad, cantidad, disponibles))

        conn.commit()
        cursor.close()
        conn.close()
    return render_template("registrar.html")




@app.route("/actualizar", methods=["GET", "POST", "PUT"])
def actualizar():
    rows = ["", "", "", "", "", "", "", ""]
    if request.method == "POST":
        data = request.get_json()  
        query = data.get('query')  # Este debe ser el nombre del autor, por ejemplo: "Jose Fernandez"
        
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        try:
            sql_query = """
            SELECT libro.codigo_libro, libro.titulo_libro, libro.categoria, libro.numero_pag, 
                   publicacion.fecha_pub, inventario.cantidad, inventario.disponibles, autor.nombre_autor
            FROM autor
            INNER JOIN publicacion ON autor.codigo_autor = publicacion.codigo_autor
            INNER JOIN libro ON libro.codigo_libro = publicacion.codigo_libro
            INNER JOIN inventario ON inventario.codigo_libro = libro.codigo_libro
            INNER JOIN facultad ON facultad.codigo_facultad = inventario.codigo_facultad
            WHERE libro.codigo_libro = %s
            """

            params = (query,)
            cursor.execute(sql_query, params)
            rows = list(cursor.fetchall())
            rows_conversion = [elemento for tupla in rows for elemento in tupla]
            return jsonify({'rows': rows_conversion})

        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
        finally:
            cursor.close()
            conn.close()

    elif request.method == "PUT":
        data = request.get_json()
        updated_data = data.get('updatedData', [])
        print("Datos actualizados recibidos:", updated_data)

        return jsonify({"message": "Datos actualizados correctamente."})

    return render_template("actualizar.html", row=rows)

        

@app.route("/eliminar")
def eliminar():
    conn = db_conn.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT lib.codigo_libro, lib.titulo_libro, lib.categoria, fac.nombre_facultad, inv.cantidad FROM libro AS lib INNER JOIN inventario AS inv ON lib.codigo_libro = inv.codigo_libro INNER JOIN facultad AS fac ON inv.codigo_facultad = fac.codigo_facultad ORDER BY lib.codigo_libro ASC")    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print(rows)
    return render_template("eliminar.html", rows=rows)



@app.route('/eliminar_libro/<string:id>', methods=['DELETE'])
def eliminar_libro(id):
    conn = db_conn.get_connection()
    cursor = conn.cursor()
    
    try:
        # Eliminar el libro de la base de datos usando el id (ahora como cadena)
        cursor.execute('DELETE FROM inventario WHERE codigo_libro = %s', (id,))
        cursor.execute('DELETE FROM libro WHERE codigo_libro = %s', (id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route("/consultar")
def consultar():
    conn = db_conn.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT lib.codigo_libro, lib.titulo_libro, fac.nombre_facultad, inv.cantidad, inv.disponibles FROM libro AS lib INNER JOIN  inventario AS inv ON  lib.codigo_libro = inv.codigo_libro INNER JOIN  facultad AS fac ON  inv.codigo_facultad = fac.codigo_facultad ORDER BY lib.codigo_libro ASC")    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print(rows)
    return render_template("consultar.html", rows=rows)






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
    pass
