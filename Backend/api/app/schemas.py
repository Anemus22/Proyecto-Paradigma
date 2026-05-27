from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def _strip_optional(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


class FacultadBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    tipo: str | None = Field(default=None, max_length=60)
    fecha_fun: date | None = None

    @field_validator("nombre", "tipo")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class FacultadCreate(FacultadBase):
    pass


class FacultadUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    tipo: str | None = Field(default=None, max_length=60)
    fecha_fun: date | None = None

    @field_validator("nombre", "tipo")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class FacultadRead(FacultadBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProgramaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    tipo: str | None = Field(default=None, max_length=60)
    nivel: str | None = Field(default=None, max_length=60)
    fecha_creacion: date | None = None
    fecha_cierre: date | None = None
    numero_cohortes: int | None = Field(default=None, ge=0)
    cant_graduados: int | None = Field(default=None, ge=0)
    ciudad: str | None = Field(default=None, max_length=60)
    facultad_id: int | None = Field(default=None, gt=0)

    @field_validator("nombre", "tipo", "nivel", "ciudad")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class ProgramaCreate(ProgramaBase):
    pass


class ProgramaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    tipo: str | None = Field(default=None, max_length=60)
    nivel: str | None = Field(default=None, max_length=60)
    fecha_creacion: date | None = None
    fecha_cierre: date | None = None
    numero_cohortes: int | None = Field(default=None, ge=0)
    cant_graduados: int | None = Field(default=None, ge=0)
    ciudad: str | None = Field(default=None, max_length=60)
    facultad_id: int | None = Field(default=None, gt=0)

    @field_validator("nombre", "tipo", "nivel", "ciudad")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class ProgramaRead(ProgramaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fecha_actualizacion: datetime | None = None


class LineaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120)
    descripcion: str | None = None

    @field_validator("nombre", "descripcion")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class LineaCreate(LineaBase):
    pass


class LineaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    descripcion: str | None = None

    @field_validator("nombre", "descripcion")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class LineaRead(LineaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DocenteBase(BaseModel):
    cedula: int = Field(..., gt=0)
    nombres: str = Field(..., min_length=2, max_length=80)
    apellidos: str = Field(..., min_length=2, max_length=80)
    correo: EmailStr
    genero: str | None = Field(default=None, max_length=20)
    cargo: str | None = Field(default=None, max_length=80)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=30)
    url_cvlac: str | None = Field(default=None, max_length=255)
    escalafon: str | None = Field(default=None, max_length=80)
    perfil: str | None = None
    cat_minciencia: str | None = Field(default=None, max_length=80)
    conv_minciencia: str | None = Field(default=None, max_length=80)
    nacionalidaad: str | None = Field(default=None, max_length=80)
    linea_investigacion_principal: int | None = Field(default=None, gt=0)

    @field_validator("nombres", "apellidos", "genero", "cargo", "telefono", "url_cvlac", "escalafon", "cat_minciencia", "conv_minciencia", "nacionalidaad")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class DocenteCreate(DocenteBase):
    pass


class DocenteUpdate(BaseModel):
    nombres: str | None = Field(default=None, min_length=2, max_length=80)
    apellidos: str | None = Field(default=None, min_length=2, max_length=80)
    correo: EmailStr | None = None
    genero: str | None = Field(default=None, max_length=20)
    cargo: str | None = Field(default=None, max_length=80)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=30)
    url_cvlac: str | None = Field(default=None, max_length=255)
    escalafon: str | None = Field(default=None, max_length=80)
    perfil: str | None = None
    cat_minciencia: str | None = Field(default=None, max_length=80)
    conv_minciencia: str | None = Field(default=None, max_length=80)
    nacionalidaad: str | None = Field(default=None, max_length=80)
    linea_investigacion_principal: int | None = Field(default=None, gt=0)

    @field_validator("nombres", "apellidos", "genero", "cargo", "telefono", "url_cvlac", "escalafon", "cat_minciencia", "conv_minciencia", "nacionalidaad")
    @classmethod
    def trim_fields(cls, value: str | None):
        return _strip_optional(value)


class DocenteRead(DocenteBase):
    model_config = ConfigDict(from_attributes=True)
    fecha_actualizacion: datetime | None = None


class EvaluacionBase(BaseModel):
    calificacion: float = Field(..., ge=0)
    semestre: str = Field(..., min_length=1, max_length=30)
    docente: int = Field(..., gt=0)

    @field_validator("semestre")
    @classmethod
    def trim_semestre(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("El semestre no puede estar vacío")
        return value


class EvaluacionCreate(EvaluacionBase):
    pass


class EvaluacionUpdate(BaseModel):
    calificacion: float | None = Field(default=None, ge=0)
    semestre: str | None = Field(default=None, max_length=30)
    docente: int | None = Field(default=None, gt=0)

    @field_validator("semestre")
    @classmethod
    def trim_semestre(cls, value: str | None):
        return _strip_optional(value)


class EvaluacionRead(EvaluacionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SimpleMessage(BaseModel):
    detail: str


class RootStatus(BaseModel):
    message: str
    version: str
    status: str
