from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa la extensión CORS
import os
from extractorSICSA  import extraer_oficio_y_asunto_primera_pagina

app = Flask(__name__)
CORS(app)  # Configura CORS para la aplicación Flask
@app.route('/ETL/extraer-informacion', methods=['POST', 'OPTIONS'])
def extraer_informacion():
    if request.method == 'OPTIONS':
        # Manejar solicitudes OPTIONS
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response


    try:
        if 'file' not in request.files:
            return jsonify({"error": "No se proporcionó ningún archivo PDF"}), 400

        archivo_pdf = request.files['file']
        ruta_temporal = "temp.pdf"

        archivo_pdf.save(ruta_temporal)

        resultado = extraer_oficio_y_asunto_primera_pagina(ruta_temporal)

        os.remove(ruta_temporal)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=99)
