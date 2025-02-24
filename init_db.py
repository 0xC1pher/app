from app import app, db
from models import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def init_db():
    with app.app_context():
        db.create_all()

        # Crear usuarios iniciales
        usuarios = [
            {"nombre": "padre1", "contraseña": "padre123", "rol": "padre", "correo_email": "padre2@gmail.com"},
            {"nombre": "profesor1", "contraseña": "profesor123", "rol": "profesor", "correo_email": "profesor@empresa.com"},
            {"nombre": "admin1", "contraseña": "admin123", "rol": "administrador", "correo_email": "admin@gmail.com"},
        ]

        for usuario_data in usuarios:
            usuario = Usuario(
                nombre=usuario_data["nombre"],
                rol=usuario_data["rol"],
                correo_email=usuario_data["correo_email"]
            )
            usuario.set_password(usuario_data["contraseña"])
            db.session.add(usuario)

        db.session.commit()
        print("Base de datos inicializada con datos predeterminados.")

if __name__ == "__main__":
    init_db()
