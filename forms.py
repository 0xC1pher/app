from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import ValidationError
from models import Usuario, Rol, Materia  # Importa los modelos Usuario, Rol y Materia

class UniqueEmail(object):
    """Custom validator to ensure email uniqueness."""

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'Este correo ya está en uso.'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class UsuarioForm(FlaskForm):
    """Form for creating and editing user accounts."""
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=4, max=100)])
    correo = StringField('Correo', validators=[
        DataRequired(),
        Email(),
        Length(min=6, max=200),
        UniqueEmail(model=Usuario, field=Usuario.correo_email)
    ])
    contrasena = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('confirmar_contrasena', message='Las contraseñas deben coincidir')
    ])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    tipo_usuario = SelectField('Tipo de Usuario', choices=[(rol.name, rol.value) for rol in Rol], validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    """Form for user registration (similar to UsuarioForm but potentially simpler)."""
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    correo = StringField('Correo', validators=[
        DataRequired(),
        Email(),
        Length(max=150),
        UniqueEmail(model=Usuario, field=Usuario.correo_email)
    ])
    contrasena = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('confirmar_contrasena', message='Las contraseñas deben coincidir')
    ])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    tipo_usuario = SelectField('Tipo de Usuario', choices=[(rol.name, rol.value) for rol in Rol], validators=[DataRequired()])  # Using the Enum

class ClaseForm(FlaskForm):
    """Form for creating classes."""
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=4, max=100)])
    codigo = StringField('Código', validators=[DataRequired(), Length(min=2, max=20)])
    creditos = IntegerField('Créditos', validators=[DataRequired(), NumberRange(min=1, max=10)])
    descripcion = TextAreaField('Descripción')
    id_profesor = SelectField('Profesor', coerce=int, choices=[])  # Populate dynamically

class CursoForm(FlaskForm):
    """Form for creating courses."""
    nombre = StringField('Nombre del Curso', validators=[DataRequired(), Length(min=4, max=100)])
    descripcion = TextAreaField('Descripción del Curso (Opcional)')
    materias = SelectMultipleField('Materias del Curso', coerce=int, choices=[])  # Populate dynamically
