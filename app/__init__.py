# Proyecto para usuario
# importemos el modulos flask
from flask import Flask
from flask_bcrypt import Bcrypt

# Inicializa Bcrypt ( sin pasar la app todavia  )
bcrypt = Bcrypt()

def create_app():
    #crea la instancia de la app
    app = Flask(__name__)

    # Configurar la clave secreta para el desarrollo
    app.secret_key = "TP4$medioB"

    # Vincular Bcrypt  a la aplicacion
    bcrypt.init_app(app)  


    #----- Registro de BLUEPRINTS -----

    # Importar tus blueprints (asegurate que esten bien 
    # definidos en sus respectivos archivos)
    from .controllers import user_controller
    # el punto indica importacion relativa dentro del paquete

    # Registrar los blueprints
    app.register_blueprint(user_controller.users_bp)

    # Ruta principal que redirige a la paguina de inicio o registro/login

    @app.route('/')
    def index():
        from flask import redirect, session, render_template
        # Importaciones locales para evitar circularidad temprana
        if 'user_id' in session:
            return redirect('/dashboard') 
        return render_template('bienvenida.html')

    return app

# Crear la instancia de la app cuando se importa el modulo

app = create_app()
