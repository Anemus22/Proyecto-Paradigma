-- Base de datos: gestion_profesoral

CREATE TABLE IF NOT EXISTS area_conocimiento (
    id SERIAL PRIMARY KEY,
    gran_area VARCHAR(60) NOT NULL,
    area VARCHAR(60) NOT NULL,
    disciplina VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS termino_clave (
    termino VARCHAR(30) PRIMARY KEY,
    termino_ingles VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS linea_investigacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS facultades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE,
    tipo VARCHAR(60),
    fecha_fun DATE
);

CREATE TABLE IF NOT EXISTS programa (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(60),
    nivel VARCHAR(60),
    fecha_creacion DATE,
    fecha_cierre DATE,
    numero_cohortes INTEGER,
    cant_graduados INTEGER,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ciudad VARCHAR(60),
    facultad_id INTEGER,
    CONSTRAINT fk_programa_facultad
        FOREIGN KEY (facultad_id) REFERENCES facultades(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS red (
    idr SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    url VARCHAR(255),
    pais VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS docente (
    cedula INTEGER PRIMARY KEY,
    nombres VARCHAR(80) NOT NULL,
    apellidos VARCHAR(80) NOT NULL,
    genero VARCHAR(20),
    cargo VARCHAR(80),
    fecha_nacimiento DATE,
    correo VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    url_cvlac VARCHAR(255),
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    escalafon VARCHAR(80),
    perfil TEXT,
    cat_minciencia VARCHAR(80),
    conv_minciencia VARCHAR(80),
    nacionalidaad VARCHAR(80),
    linea_investigacion_principal INTEGER,
    CONSTRAINT fk_docente_linea
        FOREIGN KEY (linea_investigacion_principal) REFERENCES linea_investigacion(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS estudios_realizados (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(180) NOT NULL,
    universidad VARCHAR(180),
    fecha DATE,
    tipo VARCHAR(60),
    ciudad VARCHAR(80),
    docente INTEGER NOT NULL,
    ins_acreditada VARCHAR(120),
    metodologia VARCHAR(80),
    perfil_egresado TEXT,
    pais VARCHAR(80),
    linea_investigacion INTEGER,
    CONSTRAINT fk_estudio_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_estudio_linea
        FOREIGN KEY (linea_investigacion) REFERENCES linea_investigacion(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS docente_departamento (
    docente INTEGER NOT NULL,
    departamento INTEGER NOT NULL,
    dedicacion VARCHAR(30) NOT NULL,
    modalidad VARCHAR(45) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE,
    PRIMARY KEY (docente, departamento),
    CONSTRAINT fk_dd_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_dd_programa
        FOREIGN KEY (departamento) REFERENCES programa(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS intereses_futuros (
    docente INTEGER NOT NULL,
    termino_clave VARCHAR(30) NOT NULL,
    PRIMARY KEY (docente, termino_clave),
    CONSTRAINT fk_if_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_if_termino
        FOREIGN KEY (termino_clave) REFERENCES termino_clave(termino)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS evaluacion_docente (
    id SERIAL PRIMARY KEY,
    calificacion DOUBLE PRECISION NOT NULL,
    semestre VARCHAR(30) NOT NULL,
    docente INTEGER NOT NULL,
    CONSTRAINT fk_eval_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reconocimiento (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(80) NOT NULL,
    fecha DATE NOT NULL,
    institucion VARCHAR(180) NOT NULL,
    nombre VARCHAR(180) NOT NULL,
    ambito VARCHAR(80) NOT NULL,
    docente INTEGER NOT NULL,
    CONSTRAINT fk_rec_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experiencia (
    id SERIAL PRIMARY KEY,
    nombre_cargo VARCHAR(180) NOT NULL,
    institucion VARCHAR(180) NOT NULL,
    tipo VARCHAR(80) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    docente INTEGER NOT NULL,
    CONSTRAINT fk_exp_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS red_docente (
    red INTEGER NOT NULL,
    docente INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    act_destacadas TEXT,
    PRIMARY KEY (red, docente),
    CONSTRAINT fk_red_docente_red
        FOREIGN KEY (red) REFERENCES red(idr)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_red_docente_docente
        FOREIGN KEY (docente) REFERENCES docente(cedula)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS estudio_ac (
    estudio INTEGER NOT NULL,
    area_conocimiento INTEGER NOT NULL,
    PRIMARY KEY (estudio, area_conocimiento),
    CONSTRAINT fk_estudio_ac_estudio
        FOREIGN KEY (estudio) REFERENCES estudios_realizados(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_estudio_ac_area
        FOREIGN KEY (area_conocimiento) REFERENCES area_conocimiento(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS apoyo_profesoral (
    estudio INTEGER PRIMARY KEY,
    con_apoyo BOOLEAN NOT NULL DEFAULT TRUE,
    institucion VARCHAR(180) NOT NULL,
    tipo VARCHAR(80) NOT NULL,
    CONSTRAINT fk_apoyo_estudio
        FOREIGN KEY (estudio) REFERENCES estudios_realizados(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS beca (
    estudio INTEGER PRIMARY KEY,
    tipo VARCHAR(80) NOT NULL,
    institucion VARCHAR(180) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    CONSTRAINT fk_beca_estudio
        FOREIGN KEY (estudio) REFERENCES estudios_realizados(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Tablas de gestión de usuarios
CREATE TABLE IF NOT EXISTS rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    nombre_completo VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rol_usuario (
    usuario_id INT NOT NULL,
    rol_id INT NOT NULL,
    PRIMARY KEY (usuario_id, rol_id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE
);
