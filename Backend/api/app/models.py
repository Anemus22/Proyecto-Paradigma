from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from api.app.database import Base


class AreaConocimiento(Base):
    __tablename__ = "area_conocimiento"

    id = Column(Integer, primary_key=True, index=True)
    gran_area = Column(String(60), nullable=False)
    area = Column(String(60), nullable=False)
    disciplina = Column(String(60), nullable=False)


class TerminoClave(Base):
    __tablename__ = "termino_clave"

    termino = Column(String(30), primary_key=True, index=True)
    termino_ingles = Column(String(30), nullable=True)


class LineaInvestigacion(Base):
    __tablename__ = "linea_investigacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    docentes = relationship("Docente", back_populates="linea_principal_rel")
    estudios = relationship("EstudioRealizado", back_populates="linea_rel")


class Facultad(Base):
    __tablename__ = "facultades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False, unique=True)
    tipo = Column(String(60), nullable=True)
    fecha_fun = Column(Date, nullable=True)

    programas = relationship("Programa", back_populates="facultad_rel")


class Programa(Base):
    __tablename__ = "programa"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    tipo = Column(String(60), nullable=True)
    nivel = Column(String(60), nullable=True)
    fecha_creacion = Column(Date, nullable=True)
    fecha_cierre = Column(Date, nullable=True)
    numero_cohortes = Column(Integer, nullable=True)
    cant_graduados = Column(Integer, nullable=True)
    fecha_actualizacion = Column(DateTime, server_default=func.now(), nullable=True)
    ciudad = Column(String(60), nullable=True)
    facultad_id = Column(
        Integer,
        ForeignKey("facultades.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    facultad_rel = relationship("Facultad", back_populates="programas")
    docentes_departamento = relationship("DocenteDepartamento", back_populates="programa_rel")


class Red(Base):
    __tablename__ = "red"

    idr = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    url = Column(String(255), nullable=True)
    pais = Column(String(80), nullable=True)

    docentes = relationship("RedDocente", back_populates="red_rel")


class Docente(Base):
    __tablename__ = "docente"

    cedula = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(80), nullable=False)
    apellidos = Column(String(80), nullable=False)
    genero = Column(String(20), nullable=True)
    cargo = Column(String(80), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    correo = Column(String(120), nullable=False, unique=True, index=True)
    telefono = Column(String(30), nullable=True)
    url_cvlac = Column(String(255), nullable=True)
    fecha_actualizacion = Column(DateTime, server_default=func.now(), nullable=True)
    escalafon = Column(String(80), nullable=True)
    perfil = Column(Text, nullable=True)
    cat_minciencia = Column(String(80), nullable=True)
    conv_minciencia = Column(String(80), nullable=True)
    nacionalidaad = Column(String(80), nullable=True)
    linea_investigacion_principal = Column(
        Integer,
        ForeignKey("linea_investigacion.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    linea_principal_rel = relationship("LineaInvestigacion", back_populates="docentes")
    estudios = relationship("EstudioRealizado", back_populates="docente_rel", cascade="all, delete-orphan")
    evaluaciones = relationship("EvaluacionDocente", back_populates="docente_rel", cascade="all, delete-orphan")
    reconocimientos = relationship("Reconocimiento", back_populates="docente_rel", cascade="all, delete-orphan")
    experiencias = relationship("Experiencia", back_populates="docente_rel", cascade="all, delete-orphan")
    departamentos = relationship("DocenteDepartamento", back_populates="docente_rel", cascade="all, delete-orphan")
    redes = relationship("RedDocente", back_populates="docente_rel", cascade="all, delete-orphan")
    intereses_futuros = relationship("TerminoClave", secondary="intereses_futuros", back_populates="docentes_interesados")


class EstudioRealizado(Base):
    __tablename__ = "estudios_realizados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(180), nullable=False)
    universidad = Column(String(180), nullable=True)
    fecha = Column(Date, nullable=True)
    tipo = Column(String(60), nullable=True)
    ciudad = Column(String(80), nullable=True)
    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ins_acreditada = Column(String(120), nullable=True)
    metodologia = Column(String(80), nullable=True)
    perfil_egresado = Column(Text, nullable=True)
    pais = Column(String(80), nullable=True)
    linea_investigacion = Column(
        Integer,
        ForeignKey("linea_investigacion.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    docente_rel = relationship("Docente", back_populates="estudios")
    linea_rel = relationship("LineaInvestigacion", back_populates="estudios")
    apoyo_profesoral = relationship("ApoyoProfesoral", back_populates="estudio_rel", uselist=False, cascade="all, delete-orphan")
    beca = relationship("Beca", back_populates="estudio_rel", uselist=False, cascade="all, delete-orphan")
    areas = relationship("AreaConocimiento", secondary="estudio_ac", back_populates="estudios_asociados")


class DocenteDepartamento(Base):
    __tablename__ = "docente_departamento"

    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    departamento = Column(
        Integer,
        ForeignKey("programa.id", onupdate="CASCADE", ondelete="RESTRICT"),
        primary_key=True,
    )
    dedicacion = Column(String(30), nullable=False)
    modalidad = Column(String(45), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    fecha_salida = Column(Date, nullable=True)

    docente_rel = relationship("Docente", back_populates="departamentos")
    programa_rel = relationship("Programa", back_populates="docentes_departamento")


class InteresesFuturos(Base):
    __tablename__ = "intereses_futuros"

    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    termino_clave = Column(
        String(30),
        ForeignKey("termino_clave.termino", onupdate="CASCADE", ondelete="RESTRICT"),
        primary_key=True,
    )


class EvaluacionDocente(Base):
    __tablename__ = "evaluacion_docente"

    id = Column(Integer, primary_key=True, index=True)
    calificacion = Column(Float, nullable=False)
    semestre = Column(String(30), nullable=False)
    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    docente_rel = relationship("Docente", back_populates="evaluaciones")


class Reconocimiento(Base):
    __tablename__ = "reconocimiento"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(80), nullable=False)
    fecha = Column(Date, nullable=False)
    institucion = Column(String(180), nullable=False)
    nombre = Column(String(180), nullable=False)
    ambito = Column(String(80), nullable=False)
    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    docente_rel = relationship("Docente", back_populates="reconocimientos")


class Experiencia(Base):
    __tablename__ = "experiencia"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cargo = Column(String(180), nullable=False)
    institucion = Column(String(180), nullable=False)
    tipo = Column(String(80), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    docente_rel = relationship("Docente", back_populates="experiencias")


class RedDocente(Base):
    __tablename__ = "red_docente"

    red = Column(
        Integer,
        ForeignKey("red.idr", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    docente = Column(
        Integer,
        ForeignKey("docente.cedula", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    act_destacadas = Column(Text, nullable=True)

    red_rel = relationship("Red", back_populates="docentes")
    docente_rel = relationship("Docente", back_populates="redes")


class EstudioAC(Base):
    __tablename__ = "estudio_ac"

    estudio = Column(
        Integer,
        ForeignKey("estudios_realizados.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    area_conocimiento = Column(
        Integer,
        ForeignKey("area_conocimiento.id", onupdate="CASCADE", ondelete="RESTRICT"),
        primary_key=True,
    )


class ApoyoProfesoral(Base):
    __tablename__ = "apoyo_profesoral"

    estudio = Column(
        Integer,
        ForeignKey("estudios_realizados.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    con_apoyo = Column(Boolean, default=True, nullable=False)
    institucion = Column(String(180), nullable=False)
    tipo = Column(String(80), nullable=False)

    estudio_rel = relationship("EstudioRealizado", back_populates="apoyo_profesoral")


class Beca(Base):
    __tablename__ = "beca"

    estudio = Column(
        Integer,
        ForeignKey("estudios_realizados.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    tipo = Column(String(80), nullable=False)
    institucion = Column(String(180), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    estudio_rel = relationship("EstudioRealizado", back_populates="beca")


# back-populates for collection relationships declared after dependent classes
AreaConocimiento.estudios_asociados = relationship(  # type: ignore[attr-defined]
    "EstudioRealizado",
    secondary="estudio_ac",
    back_populates="areas",
)

TerminoClave.docentes_interesados = relationship(  # type: ignore[attr-defined]
    "Docente",
    secondary="intereses_futuros",
    back_populates="intereses_futuros",
)
