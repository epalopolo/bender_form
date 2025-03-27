from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import pymysql
import os
from dotenv import load_dotenv
from datetime import date

# Cargar variables de entorno
load_dotenv(dotenv_path="keys.env")

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Configuración de bases de datos
DB_DEFAULT = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE_1')}"
DB_RESPUESTAS = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE_2')}"

engine_default = create_engine(DB_DEFAULT, pool_recycle=3600, pool_size=10, max_overflow=5)
engine_respuestas = create_engine(DB_RESPUESTAS, pool_recycle=3600, pool_size=10, max_overflow=5)

SessionDefault = sessionmaker(bind=engine_default)
SessionRespuestas = sessionmaker(bind=engine_respuestas)

BaseDefault = declarative_base()
BaseRespuestas = declarative_base()

@contextmanager
def get_db_session(engine):
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# 🔹 Modelos de la base de datos "default"
class Cliente(BaseDefault):
    __tablename__ = "clientes"
    Codigo = Column(String, primary_key=True, index=True)
    RazonSocial = Column(String, index=True)
    CUIT = Column(String, index=True)

class Tarea(BaseDefault):
    __tablename__ = "tareas"
    ID = Column(String, primary_key=True, index=True)
    Tarea = Column(String, unique=True, index=True)
    Seccion = Column(String, index=True)

class Pieza(BaseDefault):
    __tablename__ = "piezas"
    Codigo = Column(String, primary_key=True, index=True)
    Pieza = Column(String, unique=True, index=True)

class Maquinaria(BaseDefault):
    __tablename__ = "maquinarias"
    Codigo = Column(String, primary_key=True, index=True)
    Producto_codigo = Column(String, index=True)
    Nombre = Column(String, unique=True, index=True)
    SECTOR = Column(String, index=True)

class Insumo(BaseDefault):
    __tablename__ = "insumos"
    Codigo = Column(Integer, primary_key=True, index=True)
    materiales_insumos = Column(String, index=True)
    insumos = Column(String, unique=True, index=True)

# 🔹 Modelos de la base de datos "respuestas_db"
class General(BaseRespuestas):
    __tablename__ = "general"
    id = Column(Integer, primary_key=True)
    fecha = Column(String, default=str(date.today()))
    cliente = Column(String)
    evaluacion = Column(Boolean, default=False)
    mecanica = Column(Boolean, default=False)
    mecanizado = Column(Boolean, default=False)
    ingenieria = Column(Boolean, default=False)
    lavado = Column(Boolean, default=False)
    arenado = Column(Boolean, default=False)
    pintura = Column(Boolean, default=False)
    soldadura = Column(Boolean, default=False)
    tratamiento_termico = Column(Boolean, default=False)
    corte = Column(Boolean, default=False)
    transporte = Column(Boolean, default=False)
    plegado = Column(Boolean, default=False)

class TareaRT(BaseRespuestas):
    __tablename__ = "tareas_rt"
    id = Column(Integer, primary_key=True)
    general_id = Column(Integer, ForeignKey("general.id"))
    tarea = Column(String)
    pieza = Column(String)
    maquinaria = Column(String)
    horas_trabajo = Column(Float)

class InsumoRT(BaseRespuestas):
    __tablename__ = "insumos_rt"
    id = Column(Integer, primary_key=True)
    general_id = Column(Integer, ForeignKey("general.id"))
    insumo = Column(String)
    material = Column(String)
    od = Column(Float)
    od_unidad = Column(String(10))
    id_medida = Column(Float)
    id_unidad = Column(String(10))
    largo = Column(Float)
    largo_unidad = Column(String(10))
    ancho = Column(Float)
    ancho_unidad = Column(String(10))
    alto = Column(Float)
    alto_unidad = Column(String(10))
    cantidad = Column(Float)

# Crear tablas si no existen
BaseDefault.metadata.create_all(bind=engine_default)
BaseRespuestas.metadata.create_all(bind=engine_respuestas)

@app.route("/opciones_formulario", methods=["GET"])
def obtener_opciones_formulario():
    with get_db_session(engine_default) as db:
        try:
            opciones = {
                "clientes": [c[0] for c in db.query(Cliente.RazonSocial).all()],
                "tareas": [t[0] for t in db.query(Tarea.Tarea).all()],
                "piezas": [p[0] for p in db.query(Pieza.Pieza).all()],
                "maquinarias": [m[0] for m in db.query(Maquinaria.Nombre).all()],
                "materiales": [m[0] for m in db.query(Insumo.materiales_insumos).distinct().all() if m[0]],
                "insumos": [i[0] for i in db.query(Insumo.insumos).distinct().all() if i[0]]
            }
            return jsonify(opciones)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# 🔹 Ruta para recibir y guardar el formulario
@app.route("/guardar_formulario/", methods=["POST"])
def guardar_formulario():
    data = request.json
    with get_db_session(engine_respuestas) as db:
        nuevo_general = General(
            fecha=data["fecha"],
            cliente=data["cliente"],
            evaluacion=data["evaluacion"],
            mecanica=data["mecanica"],
            mecanizado=data["mecanizado"],
            ingenieria=data["ingenieria"],
            lavado=data["lavado"],
            arenado=data["arenado"],
            pintura=data["pintura"],
            soldadura=data["soldadura"],
            tratamiento_termico=data["tratamiento_termico"],
            corte=data["corte"],
            transporte=data["transporte"],
            plegado=data["plegado"]
        )
        db.add(nuevo_general)
        db.flush()

        # Guardar tareas
        for tarea in data.get("tareas", []):
            db.add(TareaRT(
                general_id=nuevo_general.id,
                tarea=tarea["tarea"],
                pieza=tarea["pieza"],
                maquinaria=tarea["maquinaria"],
                horas_trabajo=tarea["horas_trabajo"]
            ))

        for insumo in data.get("insumos", []):
            db.add(InsumoRT(
                general_id=nuevo_general.id,
                insumo=insumo["insumo"],
                material=insumo["material"],
                od=insumo["od"],
                od_unidad=insumo["od_unidad"],
                id_medida=insumo["id_medida"],
                id_unidad=insumo["id_unidad"],
                largo=insumo["largo"],
                largo_unidad=insumo["largo_unidad"],
                ancho=insumo["ancho"],
                ancho_unidad=insumo["ancho_unidad"],
                alto=insumo["alto"],
                alto_unidad=insumo["alto_unidad"],
                cantidad=insumo["cantidad"]
            ))

        return jsonify({"message": "Formulario guardado con éxito"})

if __name__ == '__main__':
    app.run(debug=True)
