from __future__ import annotations

import os
from typing import Any

import requests
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "gestor-profesoral")

API = os.getenv("API_URL", "http://127.0.0.1:8000")
API_V1 = f"{API}/api/v1"


def _get(endpoint: str, default: Any):
    try:
        r = requests.get(f"{API_V1}{endpoint}", timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return default


def _post(endpoint: str, payload: dict):
    try:
        r = requests.post(f"{API_V1}{endpoint}", json=payload, timeout=10)
        if r.status_code >= 400:
            try:
                return False, r.json().get("detail", "Operación no permitida")
            except Exception:
                return False, "Operación no permitida"
        return True, "Guardado correctamente"
    except requests.RequestException:
        return False, "No se pudo conectar con la API"


@app.route("/")
def index():
    contexto = {
        "resumen": _get("/resumen", {}),
        "docentes": _get("/docentes", []),
        "programas": _get("/programas", []),
        "evaluaciones": _get("/evaluaciones", []),
        "facultades": _get("/facultades", []),
        "lineas": _get("/lineas", []),
        "api_base": API,
    }
    return render_template("index.html", **contexto)


@app.route("/crear_docente", methods=["POST"])
def crear_docente():
    payload = {
        "cedula": int(request.form["cedula"]),
        "nombres": request.form["nombres"].strip(),
        "apellidos": request.form["apellidos"].strip(),
        "correo": request.form["correo"].strip(),
        "genero": request.form.get("genero", "").strip() or None,
        "cargo": request.form.get("cargo", "").strip() or None,
        "telefono": request.form.get("telefono", "").strip() or None,
        "linea_investigacion_principal": int(request.form["linea_investigacion_principal"])
        if request.form.get("linea_investigacion_principal")
        else None,
    }
    ok, msg = _post("/docentes/", payload)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/crear_programa", methods=["POST"])
def crear_programa():
    payload = {
        "nombre": request.form["nombre"].strip(),
        "tipo": request.form.get("tipo", "").strip() or None,
        "nivel": request.form.get("nivel", "").strip() or None,
        "ciudad": request.form.get("ciudad", "").strip() or None,
        "facultad_id": int(request.form["facultad_id"]) if request.form.get("facultad_id") else None,
    }
    ok, msg = _post("/programas/", payload)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/crear_evaluacion", methods=["POST"])
def crear_evaluacion():
    payload = {
        "calificacion": float(request.form["calificacion"]),
        "semestre": request.form["semestre"].strip(),
        "docente": int(request.form["docente"]),
    }
    ok, msg = _post("/evaluaciones/", payload)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/crear_facultad", methods=["POST"])
def crear_facultad():
    payload = {
        "nombre": request.form["nombre"].strip(),
        "tipo": request.form.get("tipo", "").strip() or None,
    }
    ok, msg = _post("/facultades/", payload)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/crear_linea", methods=["POST"])
def crear_linea():
    payload = {
        "nombre": request.form["nombre"].strip(),
        "descripcion": request.form.get("descripcion", "").strip() or None,
    }
    ok, msg = _post("/lineas/", payload)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))

def _delete(endpoint: str):
    try:
        # Usamos la variable API_V1 que ya definiste
        r = requests.delete(f"{API_V1}{endpoint}", timeout=10)
        r.raise_for_status()
        return True, "Eliminado correctamente"
    except requests.RequestException:
        return False, "No se pudo conectar con la API para eliminar"

# Nueva ruta en tu app.py para manejar la petición desde el HTML
@app.route("/eliminar_docente/<int:id>", methods=["POST"])
def eliminar_docente(id):
    ok, msg = _delete(f"/docentes/{id}") # Ajusta el endpoint según tu API
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


# Rutas de eliminación para los demás recursos
@app.route("/eliminar_programa/<int:id>", methods=["POST"])
def eliminar_programa(id):
    ok, msg = _delete(f"/programas/{id}")
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/eliminar_evaluacion/<int:id>", methods=["POST"])
def eliminar_evaluacion(id):
    ok, msg = _delete(f"/evaluaciones/{id}")
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/eliminar_facultad/<int:id>", methods=["POST"])
def eliminar_facultad(id):
    ok, msg = _delete(f"/facultades/{id}")
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/eliminar_linea/<int:id>", methods=["POST"])
def eliminar_linea(id):
    ok, msg = _delete(f"/lineas/{id}")
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
