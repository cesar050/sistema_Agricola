import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from routes.cultivo_routes import cultivo_bp
from routes.sensor_routes import sensor_bp
from routes.lectura_routes import lectura_bp
from routes.tarea_routes import tarea_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(cultivo_bp, url_prefix="/api/cultivos")
app.register_blueprint(sensor_bp, url_prefix="/api/sensores")
app.register_blueprint(lectura_bp, url_prefix="/api/lecturas")
app.register_blueprint(tarea_bp, url_prefix="/api/tareas")

@app.route("/")
def index():
    return {"message": "SIGA - API REST"}

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')