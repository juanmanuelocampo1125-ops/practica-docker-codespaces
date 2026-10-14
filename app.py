from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "productos.db"

def conectar():
    return sqlite3.connect(DB)

@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]

        with conectar() as db:
            db.execute(
                "INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)",
                (nombre, categoria, precio)
            )

        return redirect("/")

    with conectar() as db:
        productos = db.execute(
            "SELECT id, nombre, categoria, precio FROM productos"
        ).fetchall()

    return render_template("index.html", productos=productos)

def crear_tabla():
    with conectar() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL
            )
        """)

crear_tabla()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)