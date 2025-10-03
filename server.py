# server.py
from app import app # Importa la instancia de la aplicación Flask desde tu paquete

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    