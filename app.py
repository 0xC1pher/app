# app.py
import os
import logging
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, NumberRange, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# Database Setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Models
class CursoMateria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    id_materia = db.Column(db.Integer, db.ForeignKey('materia.id'))

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo_email = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150))
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    id_acudiente = db.Column(db.Integer, db.ForeignKey('acudiente.id'))
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso = db.relationship('Curso', backref=db.backref('estudiantes', lazy=True))
    acudiente = db.relationship('Acudiente', backref=db.backref('estudiantes', lazy=True))

    __table_args__ = (db.Index('ix_estudiante_id_curso', id_curso),)

class Clase(db.Model):
    id_clase = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso = db.relationship('Curso', backref=db.backref('clases', lazy=True))

class Inscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    id_materia = db.Column(db.Integer, db.ForeignKey('materia.id'))
    estudiante = db.relationship('Estudiante', backref=db.backref('inscripciones', lazy=True))
    materia = db.relationship('Materia', backref=db.backref('inscripciones', lazy=True))

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    id_profesor = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    profesor = db.relationship('Usuario', backref=db.backref('cursos', lazy=True))
    materias = db.relationship('Materia', secondary='curso_materia', backref=db.backref('cursos', lazy=True))

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True)
    creditos = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    id_profesor = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    profesor = db.relationship('Usuario', foreign_keys=[id_profesor], backref='materias_dictadas')

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50))
    justificacion = db.Column(db.Text)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    id_clase = db.Column(db.Integer, db.ForeignKey('clase.id_clase'))
    id_profesor = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    estudiante = db.relationship('Estudiante', backref=db.backref('asistencias', lazy=True))
    clase = db.relationship('Clase', backref=db.backref('asistencias', lazy=True))
    profesor = db.relationship('Usuario', foreign_keys=[id_profesor], backref='asistencias_registradas')

class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    contenido = db.Column(db.Text)

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

class Acudiente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150))
    telefono = db.Column(db.String(20))

# Custom Validators
class UniqueEmail(object):
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

# Forms
class RegistrationForm(FlaskForm):
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
    tipo_usuario = SelectField('Tipo de Usuario', choices=[('Profesor', 'Profesor'), ('Administrador', 'Administrador')], validators=[DataRequired()])

class ClaseForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    codigo = StringField('Código', validators=[DataRequired(), Length(max=20)])
    creditos = IntegerField('Créditos', validators=[DataRequired(), NumberRange(min=1, max=10)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    id_profesor = SelectField('Profesor', coerce=int, validators=[DataRequired()])

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    correo = StringField('Correo', validators=[
        DataRequired(),
        Email(),
        Length(max=150),
        UniqueEmail(model=Usuario, field=Usuario.correo_email)
    ])
    contrasena = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8)])
    tipo_usuario = SelectField('Tipo de Usuario', choices=[('Profesor', 'Profesor'), ('Administrador', 'Administrador')], validators=[DataRequired()])

class CursoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    id_profesor = SelectField('Profesor', coerce=int, validators=[DataRequired()])
    materias = SelectMultipleField('Materias', coerce=int)

class EstudianteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    correo = StringField('Correo', validators=[Optional(), Email(), Length(max=150)])
    fecha_nacimiento = StringField('Fecha de Nacimiento (YYYY-MM-DD)', validators=[Optional()])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=200)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    id_acudiente = IntegerField('ID Acudiente', validators=[Optional()])
    id_curso = SelectField('Curso', coerce=int, validators=[DataRequired()])

# Authentication
@app.before_request
def require_login():
    if request.endpoint not in ['login', 'register', 'static'] and 'usuario_id' not in session:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if request.method == 'POST':
        correo_email_form = request.form.get('correo')
        contrasena_form = request.form.get('contrasena')
        tipo_usuario_form = request.form.get('tipo_usuario')

        usuario = Usuario.query.filter_by(correo_email=correo_email_form).first()

        if usuario:
            if bcrypt.check_password_hash(usuario.contraseña, contrasena_form):
                if usuario.rol == tipo_usuario_form:
                    session['usuario_id'] = usuario.id_usuario
                    session['rol'] = usuario.rol  # Store the role in the session
                    logger.info(f"Usuario {usuario.correo_email} logged in as {usuario.rol}")
                    if tipo_usuario_form == 'Profesor':
                        return redirect(url_for('dashboard_profesor'))
                    elif tipo_usuario_form == 'Administrador':
                        return redirect(url_for('dashboard_administrador'))
                    else:
                        flash("Rol no reconocido", "error")
                else:
                    flash("Tipo de usuario incorrecto", "error")
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Usuario no encontrado", "error")

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.contrasena.data).decode('utf-8')
            nuevo_usuario = Usuario(
                nombre=form.nombre.data,
                correo_email=form.correo.data,
                contraseña=hashed_password,
                rol=form.tipo_usuario.data
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado con éxito', 'success')
            logger.info(f"New user registered: {nuevo_usuario.correo_email}")
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed: usuario.correo_email" in str(e):
                flash("Este correo electrónico ya está registrado.", "error")
            else:
                flash(f"Error al registrar el usuario: {str(e)}", "error")
            logger.error(f"Registration error: {e}")
        except Exception as e:
            db.session.rollback()
            flash(f"Error inesperado: {str(e)}", "error")
            logger.exception("Unexpected registration error")  # Log the full traceback
    return render_template('register.html', form=form)

# Dashboards
@app.route('/dashboard_administrador')
def dashboard_administrador():
    if session.get('usuario_id') and session.get('rol') == 'Administrador':
        return render_template('dashboard_administrador.html')
    else:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('login'))

@app.route('/dashboard_profesor')
def dashboard_profesor():
    if session.get('usuario_id') and session.get('rol') == 'Profesor':
        return render_template('dashboard_profesor.html')
    else:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('login'))

# Student Management
@app.route('/register_estudiante', methods=['GET', 'POST'])
def register_estudiante():
    if session.get('usuario_id') and session.get('rol') == 'Administrador':
        form = EstudianteForm(request.form)
        form.id_curso.choices = [(curso.id, curso.nombre) for curso in Curso.query.all()]

        if form.validate_on_submit():
            try:
                fecha_nacimiento = datetime.strptime(form.fecha_nacimiento.data, '%Y-%m-%d').date() if form.fecha_nacimiento.data else None
                nuevo_estudiante = Estudiante(
                    nombre=form.nombre.data,
                    apellido=form.apellido.data,
                    correo=form.correo.data,
                    fecha_nacimiento=fecha_nacimiento,
                    direccion=form.direccion.data,
                    telefono=form.telefono.data,
                    id_acudiente=form.id_acudiente.data if form.id_acudiente.data else None,
                    id_curso=form.id_curso.data
                )
                db.session.add(nuevo_estudiante)
                db.session.commit()
                flash('Estudiante registrado con éxito', 'success')
                logger.info(f"New student registered: {nuevo_estudiante.nombre} {nuevo_estudiante.apellido}")
                return redirect(url_for('list_estudiantes'))
            except ValueError:
                flash('Formato de fecha inválido', 'danger')
                logger.warning("Invalid date format provided.")
            except Exception as e:
                db.session.rollback()
                flash(f'Error al registrar el estudiante: {str(e)}', 'danger')
                logger.exception(f"Error registering student: {e}")
        return render_template('register_estudiante.html', form=form)
    else:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('login'))

@app.route('/estudiantes/list')
def list_estudiantes():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    estudiantes = Estudiante.query.paginate(page=page, per_page=per_page)
    return render_template('list_estudiantes.html', estudiantes=estudiantes)

# Materia Management
@app.route('/materias/add', methods=['GET', 'POST'])
def add_materia():
    usuario_id = session.get('usuario_id')
    if usuario_id and session.get('rol') == 'Administrador':
        profesores = Usuario.query.filter_by(rol='Profesor').all()
        profesor_choices = [(profesor.id_usuario, f"{profesor.nombre} {profesor.apellido}") for profesor in profesores]

        form = ClaseForm()
        form.id_profesor.choices = profesor_choices

        if request.method == 'POST' and form.validate():
            try:
                nueva_materia = Materia(
                    nombre=form.nombre.data,
                    codigo=form.codigo.data,
                    creditos=form.creditos.data,
                    descripcion=form.descripcion.data,
                    id_profesor=form.id_profesor.data
                )
                db.session.add(nueva_materia)
                db.session.commit()
                flash('Materia agregada con éxito', 'success')
                logger.info(f"New materia added: {nueva_materia.nombre}")
                return redirect(url_for('list_materias'))
            except IntegrityError as e:
                db.session.rollback()
                flash(f'Error al agregar materia: {str(e)}', 'danger')
                logger.error(f"Error adding materia: {e}")
            except Exception as e:
                db.session.rollback()
                flash(f'Error inesperado: {str(e)}', 'danger')
                logger.exception("Unexpected error adding materia")
        return render_template('add_materia.html', form=form, profesores=profesores)
    else:
        flash('No tienes permisos para agregar materias', 'error')
        return redirect(url_for('login'))

@app.route('/materias/list')
def list_materias():
    materias = Materia.query.all()
    return render_template('list_materias.html', materias=materias, tipo_entidad="Materias")

# Enrollment
@app.route('/estudiantes/enroll', methods=['GET', 'POST'])
def enroll_estudiante():
    if session.get('usuario_id') and session.get('rol') == 'Administrador':
        if request.method == 'POST':
            estudiante_id = request.form.get('estudiante_id')
            materia_id = request.form.get('materia_id')

            estudiante = Estudiante.query.get(estudiante_id)
            materia = Materia.query.get(materia_id)

            if not estudiante or not materia:
                flash('Estudiante o materia no encontrados', 'error')
                return redirect(url_for('enroll_estudiante'))

            inscripcion_existente = Inscripcion.query.filter_by(id_estudiante=estudiante_id, id_materia=materia_id).first()
            if inscripcion_existente:
                flash('El estudiante ya está inscrito en esta materia', 'error')
                return redirect(url_for('enroll_estudiante'))

            try:
                nueva_inscripcion = Inscripcion(id_estudiante=estudiante_id, id_materia=materia_id)
                db.session.add(nueva_inscripcion)
                db.session.commit()

                flash('Estudiante inscrito con éxito', 'success')
                logger.info(f"Estudiante {estudiante.nombre} enrolled in materia {materia.nombre}")
                return redirect(url_for('list_estudiantes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al inscribir el estudiante: {str(e)}', 'danger')
                logger.exception(f"Error enrolling student: {e}")

        estudiantes = Estudiante.query.all()
        materias = Materia.query.all()
        return render_template('enroll_estudiante.html', estudiantes=estudiantes, materias=materias)
    else:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('rol', None)  # Remove the role from the session as well
    return redirect(url_for('login'))

# User Management
@app.route('/usuarios/gestion', methods=['GET', 'POST'])
def gestion_usuarios():
    if session.get('usuario_id') and session.get('rol') == 'Administrador':
        form = UsuarioForm(request.form)
        if request.method == 'POST' and form.validate():
            try:
                nombre = form.nombre.data
                correo_email = form.correo.data
                contrasena = form.contrasena.data
                rol = form.tipo_usuario.data

                hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')

                nuevo_usuario = Usuario(
                    nombre=nombre,
                    correo_email=correo_email,
                    contraseña=hashed_password,
                    rol=rol
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                flash('Usuario creado con éxito', 'success')
                logger.info(f"New user created: {nuevo_usuario.correo_email} with role {nuevo_usuario.rol}")
                return redirect(url_for('gestion_usuarios'))
            except IntegrityError as e:
                db.session.rollback()
                flash(f'Error al crear el usuario: {str(e)}', 'danger')
                logger.error(f"Error creating user: {e}")
                return render_template('gestion_usuarios.html', usuarios=Usuario.query.all(), form=form)
            except Exception as e:
                db.session.rollback()
                flash(f'Error inesperado: {str(e)}', 'danger')
                logger.exception("Unexpected error creating user")
                return render_template('gestion_usuarios.html', usuarios=Usuario.query.all(), form=form)

        usuarios = Usuario.query.all()
        return render_template('gestion_usuarios.html', usuarios=usuarios, form=form)
    else:
        flash('No tienes permisos para gestionar usuarios', 'error')
        return redirect(url_for('login'))

# Attendance
@app.route('/asistencia/registrar', methods=['GET', 'POST'])
def registrar_asistencia():
    if not session.get('usuario_id') or session.get('rol') != 'Profesor':
        flash('Debes iniciar sesión como profesor para registrar asistencia.', 'danger')
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    usuario = Usuario.query.get(usuario_id)

    cursos = Curso.query.filter_by(id_profesor=usuario_id).all()
    estudiantes = []
    curso_seleccionado = None

    if request.method == 'POST':
        curso_id = request.form.get('curso_id')
        fecha_clase_str = request.form.get('fecha_clase')

        curso_seleccionado = Curso.query.get(curso_id)
        if not curso_seleccionado:
            flash('Curso no válido.', 'danger')
            return render_template('registrar_asistencia.html', cursos=cursos, estudiantes=estudiantes)

        try:
            fecha_clase = datetime.strptime(fecha_clase_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Fecha de clase no válida.', 'danger')
            return render_template('registrar_asistencia.html', cursos=cursos, estudiantes=estudiantes)

        estudiantes_curso = curso_seleccionado.estudiantes
        if not estudiantes_curso:
            flash('No hay estudiantes inscritos en este curso.', 'warning')
            return render_template('registrar_asistencia.html', cursos=cursos, estudiantes=estudiantes)

        try:
            for estudiante in estudiantes_curso:
                estado_asistencia = request.form.get(f'asistencia_estudiante_{estudiante.id}')
                justificacion = request.form.get(f'justificacion_estudiante_{estudiante.id}')

                # Crear registro de asistencia
                nueva_asistencia = Asistencia(
                    estado=estado_asistencia,
                    justificacion=justificacion,
                    id_estudiante=estudiante.id,
                    id_clase=curso_seleccionado.clases[0].id_clase if curso_seleccionado.clases else None,  # Asumiendo una clase por curso por fecha, ajusta si es diferente
                    id_profesor=usuario_id
                )
                db.session.add(nueva_asistencia)

            db.session.commit()
            flash('Asistencia registrada con éxito.', 'success')
            logger.info(f"Attendance registered for curso {curso_seleccionado.nombre} by profesor {usuario.correo_email}")
            return redirect(url_for('registrar_asistencia'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la asistencia: {str(e)}', 'danger')
            logger.exception(f"Error registering attendance: {e}")
            return render_template('registrar_asistencia.html', cursos=cursos, estudiantes=estudiantes)

    return render_template('registrar_asistencia.html', cursos=cursos, estudiantes=estudiantes, curso_seleccionado=curso_seleccionado)

@app.route('/asistencia/reporte', methods=['GET', 'POST'])
def reporte_asistencia():
    if not session.get('usuario_id') or session.get('rol') != 'Profesor':
        flash('Debes iniciar sesión como profesor para ver el reporte de asistencia.', 'danger')
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    usuario = Usuario.query.get(usuario_id)

    cursos = Curso.query.filter_by(id_profesor=usuario_id).all()
    reporte_data = []
    curso_seleccionado = None
    fecha_inicio = None
    fecha_fin = None

    if request.method == 'POST' or request.method == 'GET':
        curso_id = request.args.get('curso_id')
        fecha_inicio_str = request.args.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin')

        curso_seleccionado = Curso.query.get(curso_id) if curso_id else None
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

        query = Asistencia.query.join(Clase).join(Curso).filter(Curso.id_profesor == usuario_id)

        if curso_id:
            query = query.filter(Clase.id_curso == curso_id)
        if fecha_inicio:
            query = query.filter(Clase.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Clase.fecha <= fecha_fin)

        reporte_data = query.all()

    return render_template('reporte_asistencia.html', cursos=cursos, reporte_data=reporte_data, curso_seleccionado=curso_seleccionado, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

# Course Management
@app.route('/cursos/gestion', methods=['GET', 'POST'])
def gestion_cursos():
    if session.get('usuario_id') and session.get('rol') == 'Administrador':
        form = CursoForm(request.form)
        form.id_profesor.choices = [(profesor.id_usuario, f"{profesor.nombre} {profesor.apellido}") for profesor in Usuario.query.filter_by(rol='Profesor').all()]
        form.materias.choices = [(materia.id, materia.nombre) for materia in Materia.query.all()]

        if request.method == 'POST' and form.validate():
            try:
                nombre = form.nombre.data
                descripcion = form.descripcion.data
                id_profesor = form.id_profesor.data
                materias_seleccionadas_ids = form.materias.data

                nuevo_curso = Curso(
                    nombre=nombre,
                    descripcion=descripcion,
                    id_profesor=id_profesor
                )
                db.session.add(nuevo_curso)
                db.session.commit()

                for materia_id in materias_seleccionadas_ids:
                    curso_materia = CursoMateria(id_curso=nuevo_curso.id, id_materia=materia_id)
                    db.session.add(curso_materia)

                db.session.commit()
                flash('Curso creado con éxito', 'success')
                logger.info(f"New curso created: {nuevo_curso.nombre}")
                return redirect(url_for('gestion_cursos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear el curso: {str(e)}', 'danger')
                logger.exception(f"Error creating curso: {e}")

        return render_template('gestion_cursos.html', form=form)
    else:
        flash('No tienes permisos para gestionar cursos', 'error')
        return redirect(url_for('login'))

@app.route('/cursos/editar/<int:curso_id>', methods=['GET', 'POST'])
def editar_curso(curso_id):
    if not session.get('usuario_id') or session.get('rol') != 'Administrador':
        flash('Debes iniciar sesión como administrador para editar cursos.', 'danger')
        return redirect(url_for('login'))

    curso = Curso.query.get_or_404(curso_id)
    form = CursoForm(request.form, obj=curso)
    form.id_profesor.choices = [(profesor.id_usuario, f"{profesor.nombre} {profesor.apellido}") for profesor in Usuario.query.filter_by(rol='Profesor').all()]
    form.materias.choices = [(materia.id, materia.nombre) for materia in Materia.query.all()]

    if request.method == 'POST' and form.validate():
        try:
            curso.nombre = form.nombre.data
            curso.descripcion = form.descripcion.data
            curso.id_profesor = form.id_profesor.data
            curso.materias = Materia.query.filter(Materia.id.in_(form.materias.data)).all()

            db.session.commit()
            flash('Curso actualizado con éxito.', 'success')
            logger.info(f"Curso updated: {curso.nombre}")
            return redirect(url_for('gestion_cursos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el curso: {str(e)}', 'danger')
            logger.exception(f"Error updating curso: {e}")
            return render_template('editar_curso.html', form=form, curso=curso)

    return render_template('editar_curso.html', form=form, curso=curso)

@app.route('/cursos/eliminar/<int:curso_id>')
def eliminar_curso(curso_id):
    if not session.get('usuario_id') or session.get('rol') != 'Administrador':
        flash('Debes iniciar sesión como administrador para eliminar cursos.', 'danger')
        return redirect(url_for('login'))

    curso = Curso.query.get_or_404(curso_id)

    try:
        db.session.delete(curso)
        db.session.commit()
        flash('Curso eliminado con éxito.', 'success')
        logger.info(f"Curso deleted: {curso.nombre}")
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el curso: {str(e)}', 'danger')
        logger.exception(f"Error deleting curso: {e}")

    return redirect(url_for('gestion_cursos'))

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 error: {request.path}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    logger.error(f"500 error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables within the app context
    app.run(debug=True)
