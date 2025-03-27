-- Crear Base de Datos Principal
CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;

-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    Codigo VARCHAR(20) PRIMARY KEY,
    RazonSocial VARCHAR(255) NOT NULL,
    CUIT VARCHAR(15)
);

-- Tabla de Opciones de Tareas
CREATE TABLE IF NOT EXISTS tareas (
    ID VARCHAR(10) PRIMARY KEY,
    Tarea VARCHAR(255) UNIQUE NOT NULL,
    Seccion VARCHAR(255)
);

-- Tabla de Piezas
CREATE TABLE IF NOT EXISTS piezas (
    Codigo VARCHAR(10) PRIMARY KEY,
    Pieza VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla de Maquinarias
CREATE TABLE IF NOT EXISTS maquinarias (
    Codigo VARCHAR(15) PRIMARY KEY,
    Producto_codigo VARCHAR(20) NOT NULL,
    Nombre VARCHAR(255) UNIQUE NOT NULL,
    SECTOR VARCHAR(50)
);

-- Tabla de Insumos
CREATE TABLE IF NOT EXISTS insumos (
    Codigo VARCHAR(15) PRIMARY KEY,
    materiales_insumos VARCHAR(255) NOT NULL,
    insumos VARCHAR(255) NOT NULL
);
-- Crear Base de Datos para Respuestas
CREATE DATABASE IF NOT EXISTS rt_respuestas_db;
USE rt_respuestas_db;

-- Tabla General para los Formularios
CREATE TABLE IF NOT EXISTS general (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE DEFAULT CURDATE(),
    cliente_id INT NOT NULL,
    evaluacion BOOLEAN DEFAULT FALSE,
    mecanica BOOLEAN DEFAULT FALSE,
    mecanizado BOOLEAN DEFAULT FALSE,
    ingenieria BOOLEAN DEFAULT FALSE,
    lavado BOOLEAN DEFAULT FALSE,
    arenado BOOLEAN DEFAULT FALSE,
    pintura BOOLEAN DEFAULT FALSE,
    soldadura BOOLEAN DEFAULT FALSE,
    tratamiento_termico BOOLEAN DEFAULT FALSE,
    corte BOOLEAN DEFAULT FALSE,
    transporte BOOLEAN DEFAULT FALSE,
    plegado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (cliente_id) REFERENCES test_db.clientes(id) ON DELETE CASCADE
);

-- Tabla de Tareas Relacionadas con el Formulario
CREATE TABLE IF NOT EXISTS tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    general_id INT NOT NULL,
    tarea VARCHAR(255) NOT NULL,
    pieza VARCHAR(255) NOT NULL,
    maquinaria VARCHAR(255) NOT NULL,
    horas_trabajo FLOAT NOT NULL,
    FOREIGN KEY (general_id) REFERENCES general(id) ON DELETE CASCADE
);

-- Tabla de Insumos Relacionados con el Formulario
CREATE TABLE IF NOT EXISTS insumos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    general_id INT NOT NULL,
    insumo VARCHAR(255) NOT NULL,
    material VARCHAR(255) NOT NULL,
    od FLOAT,
    od_unidad VARCHAR(50),
    id_medida FLOAT,
    id_unidad VARCHAR(50),
    largo FLOAT,
    largo_unidad VARCHAR(50),
    ancho FLOAT,
    ancho_unidad VARCHAR(50),
    alto FLOAT,
    alto_unidad VARCHAR(50),
    cantidad INT NOT NULL,
    FOREIGN KEY (general_id) REFERENCES general(id) ON DELETE CASCADE
);
