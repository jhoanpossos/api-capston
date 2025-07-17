from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

def conectar_sql_server():
    try:
        connection_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=tcp:servidor-alpr-test-final.database.windows.net,1433;"
            "Database=Registro_Placas;"
            "Uid=jhoan;"
            "Pwd=Capston_2025!;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"❌ Error al conectar con Azure SQL Database: {e}")
        return None

@app.route("/placa", methods=["POST"])
def guardar_placa():
    data = request.get_json()
    placa = data.get("placa")
    if not placa:
        return jsonify({"error": "Placa no proporcionada"}), 400

    conn = conectar_sql_server()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PlacasDetectadas (Placa) VALUES (?)", placa)
        conn.commit()
        return jsonify({"message": "Placa guardada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/placa/<string:placa>", methods=["GET"])
def verificar_placa(placa):
    conn = conectar_sql_server()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VehiculosRegistrados WHERE Placa = ?", placa)
        row = cursor.fetchone()
        if row:
            return jsonify({"registrada": True}), 200
        else:
            return jsonify({"registrada": False}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
