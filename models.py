from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from enum import Enum, unique
from sqlalchemy import Enum as SQLAlchemyEnum, UniqueConstraint, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, Time, Text, ForeignKey
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

@unique
class Rol(Enum):
    PADRE = 'Padre'
    PROFESOR = 'Profesor'
    ADMINISTRADOR = 'Administrador'

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario: Mapped[int] = mapped_column(primary_key=True)  # AUTO-GENERATED
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    contraseña: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(50), nullable=False)
    correo_email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def set_password(self, password):
        """Hashea la contraseña antes de guardarla en la base de datos."""
        self.contraseña = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return bcrypt.check_password_hash(self.contraseña, password)

    # Relaciones uno-a-uno
    acudiente: Mapped["Acudiente"] = relationship(back_populates='usuario', uselist=False, cascade='all, delete-orphan')
    profesor: Mapped["Profesor"] = relationship(back_populates='usuario', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuario {self.nombre}>'  # CAMBIO AQUÍ

class Acudiente(db.Model):
    __tablename__ = 'acudiente'
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id_usuario', ondelete='CASCADE'), unique=True, nullable=False) #cascade on delete

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(back_populates='acudiente')
    estudiantes: Mapped[list["Estudiante"]] = relationship(back_populates='acudiente', cascade='all, delete-orphan') #Ensure cascade delete

    def __repr__(self):
        return f'<Acudiente {self.nombre} {self.apellido}>'

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)
    id_acudiente: Mapped[int] = mapped_column(Integer, ForeignKey('acudiente.id', ondelete='SET NULL'), nullable=True) #Set null on delete
    id_curso: Mapped[int] = mapped_column(Integer, ForeignKey('curso.id', ondelete='SET NULL'), nullable=True) #set null on delete
    correo: Mapped[str] = mapped_column(String(255), nullable=False, unique=True) # Length from SQL and unique
    codigo_estudiante: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # Added

    # Relaciones
    acudiente: Mapped[Acudiente] = relationship(back_populates='estudiantes')
    curso: Mapped["Curso"] = relationship(back_populates='estudiantes_en_curso')
    inscripciones: Mapped[list["Inscripcion"]] = relationship(back_populates='estudiante', cascade="all, delete-orphan") #Relationship
    asistencias_registradas: Mapped[list["Asistencia"]] = relationship(back_populates='estudiante') #Relationship

    def __repr__(self):
        return f'<Estudiante {self.nombre} {self.apellido}>'

class Clase(db.Model):
    __tablename__ = 'clase'
    id_clase: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED and IDENTITY
    fecha: Mapped[Date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[Time] = mapped_column(Time, nullable=True)
    hora_fin: Mapped[Time] = mapped_column(Time, nullable=True)
    id_curso: Mapped[int] = mapped_column(Integer, ForeignKey('curso.id'), nullable=False)

    # Relaciones
    curso: Mapped["Curso"] = relationship(back_populates='clases')
    asistencias: Mapped[list["Asistencia"]] = relationship(back_populates='clase', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Clase {self.id_clase} - Curso {self.id_curso}>'

class Curso(db.Model):
    __tablename__ = 'curso'
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    id_profesor: Mapped[int] = mapped_column(Integer, ForeignKey('profesor.id'), nullable=False)  # Changed to profesor.id

    # Relaciones
    profesor: Mapped["Profesor"] = relationship(back_populates='cursos_dictados')
    estudiantes_en_curso: Mapped[list["Estudiante"]] = relationship(back_populates='curso')
    clases: Mapped[list["Clase"]] = relationship(back_populates='curso')
    materias: Mapped[list["Materia"]] = relationship(secondary='curso_materia', back_populates='cursos')
    inscripciones: Mapped[list["Inscripcion"]] = relationship(back_populates='curso')  # Relationship

    def __repr__(self):
        return f'<Curso {self.nombre}>'

class Materia(db.Model):
    __tablename__ = 'materia'
    id_materia: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relaciones
    cursos: Mapped[list["Curso"]] = relationship(secondary='curso_materia', back_populates='materias')

    def __repr__(self):
        return f'<Materia {self.nombre}>'

class CursoMateria(db.Model):
    __tablename__ = 'curso_materia'
    curso_id: Mapped[int] = mapped_column(ForeignKey('curso.id'), primary_key=True)
    materia_id: Mapped[int] = mapped_column(ForeignKey('materia.id_materia'), primary_key=True)

    __table_args__ = (UniqueConstraint('curso_id', 'materia_id', name='_curso_materia_uc'),)

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id_asistencia: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    fecha_asistencia: Mapped[Date] = mapped_column(Date)  # Date
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    justificacion: Mapped[str] = mapped_column(Text, nullable=True)  # Text
    id_estudiante: Mapped[int] = mapped_column(Integer, ForeignKey('estudiante.id'), nullable=False)
    id_clase: Mapped[int] = mapped_column(Integer, ForeignKey('clase.id_clase'), nullable=False)
    id_profesor: Mapped[int] = mapped_column(Integer, ForeignKey('profesor.id'), nullable=False)  # ForeignKey to Profesor

    # Relaciones
    estudiante: Mapped["Estudiante"] = relationship(back_populates='asistencias_registradas')
    clase: Mapped["Clase"] = relationship(back_populates='asistencias')
    profesor: Mapped["Profesor"] = relationship(back_populates='asistencias_registradas') #Back populates

    def __repr__(self):
        return f'<Asistencia Estudiante {self.id_estudiante} Clase {self.id_clase}>'

class Reporte(db.Model):
    __tablename__ = 'reporte'
    id_reporte: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)  # Mandatory field
    fecha_inicio: Mapped[Date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Date] = mapped_column(Date, nullable=False)
    id_profesor: Mapped[int] = mapped_column(Integer, ForeignKey('profesor.id'), nullable=False)

    # Relaciones
    profesor: Mapped["Profesor"] = relationship(back_populates='reportes_generados')

    def __repr__(self):
        return f'<Reporte {self.tipo}>'

class Profesor(db.Model):
    __tablename__ = 'profesor'
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)  # Length from SQL
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id_usuario', ondelete='CASCADE'), unique=True, nullable=False) #Cascade on delete

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(back_populates='profesor', single_parent=True)
    cursos_dictados: Mapped[list["Curso"]] = relationship(back_populates='profesor', cascade='all, delete-orphan')
    reportes_generados: Mapped[list["Reporte"]] = relationship(back_populates='profesor', cascade='all, delete-orphan') #correct back populates relationship
    asistencias_registradas: Mapped[list["Asistencia"]] = relationship(back_populates='profesor')
    clases_dictadas: Mapped[list["Clase"]] = relationship(secondary="curso", viewonly=True)

    def __repr__(self):
        return f'<Profesor {self.nombre} {self.apellido}>'

class Inscripcion(db.Model):
    __tablename__ = 'inscripcion'
    id_inscripcion: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)  # AUTO-GENERATED
    fecha_inscripcion: Mapped[Date] = mapped_column(Date) #Remove Server default
    id_estudiante: Mapped[int] = mapped_column(ForeignKey('estudiante.id'), nullable=False)
    id_curso: Mapped[int] = mapped_column(ForeignKey('curso.id'), nullable=False)

    # Relaciones
    estudiante: Mapped["Estudiante"] = relationship(back_populates='inscripciones')
    curso: Mapped["Curso"] = relationship(back_populates='inscripciones')

    __table_args__ = (UniqueConstraint('id_estudiante', 'id_curso', name='unique_student_curso'),)

    def __repr__(self):
        return f'<Inscripcion Estudiante {self.id_estudiante} Curso {self.id_curso}>'
