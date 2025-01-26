from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/actualizar")
def actualizar():
    return render_template("actualizar.html")


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
