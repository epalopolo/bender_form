from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from pydantic import BaseModel
from datetime import date

DATABASE_URL_MAIN = "sqlite:///./test.db"
DATABASE_URL_RESPUESTAS = "sqlite:///./rt_respuestas.db"

engine_main = create_engine(DATABASE_URL_MAIN, connect_args={"check_same_thread": False})
engine_respuestas = create_engine(DATABASE_URL_RESPUESTAS, connect_args={"check_same_thread": False})

SessionLocalMain = sessionmaker(autocommit=False, autoflush=False, bind=engine_main)
SessionLocalRespuestas = sessionmaker(autocommit=False, autoflush=False, bind=engine_respuestas)

Base = declarative_base()

# Database Models for main DB
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

class TareaOpcion(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

class Pieza(Base):
    __tablename__ = "piezas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

class Maquinaria(Base):
    __tablename__ = "maquinarias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

class Insumo(Base):
    __tablename__ = "insumos"
    id = Column(Integer, primary_key=True, index=True)
    materiales_insumos = Column(String, index=True)
    insumo = Column(String, unique=True, index=True)

# Pydantic Models
class GeneralBase(BaseModel):
    cliente_id: int
    evaluacion: bool = False
    mecanica: bool = False
    mecanizado: bool = False
    ingenieria: bool = False
    lavado: bool = False
    arenado: bool = False
    pintura: bool = False
    soldadura: bool = False
    tratamiento_termico: bool = False
    corte: bool = False
    transporte: bool = False
    plegado: bool = False

class TareaBase(BaseModel):
    tarea: str
    pieza: str
    maquinaria: str
    horas_trabajo: float

class InsumoBase(BaseModel):
    insumo: str
    material: str
    od: float
    od_unidad: str
    id_medida: float
    id_unidad: str
    largo: float
    largo_unidad: str
    ancho: float
    ancho_unidad: str
    alto: float
    alto_unidad: str

class Formulario(BaseModel):
    general: GeneralBase
    tareas: list[TareaBase] = []
    insumos: list[InsumoBase] = []

# Database Models for RT respuestas
class GeneralRT(Base):
    __tablename__ = "general"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, default=str(date.today()))
    cliente_id = Column(Integer)
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

class TareaRT(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    general_id = Column(Integer, ForeignKey("general.id"))
    tarea = Column(String)
    pieza = Column(String)
    maquinaria = Column(String)
    horas_trabajo = Column(Float)

class InsumoRT(Base):
    __tablename__ = "insumos"
    id = Column(Integer, primary_key=True, index=True)
    general_id = Column(Integer, ForeignKey("general.id"))
    insumo = Column(String)
    material = Column(String)
    od = Column(Float)
    od_unidad = Column(String)
    id_medida = Column(Float)
    id_unidad = Column(String)
    largo = Column(Float)
    largo_unidad = Column(String)
    ancho = Column(Float)
    ancho_unidad = Column(String)
    alto = Column(Float)
    alto_unidad = Column(String)

Base.metadata.create_all(bind=engine_main)
Base.metadata.create_all(bind=engine_respuestas)

app = FastAPI()

def get_db_main():
    db = SessionLocalMain()
    try:
        yield db
    finally:
        db.close()

def get_db_respuestas():
    db = SessionLocalRespuestas()
    try:
        yield db
    finally:
        db.close()

@app.post("/formulario/")
def guardar_formulario(formulario: Formulario, db: Session = Depends(get_db_respuestas)):
    nuevo_general = GeneralRT(**formulario.general.dict())
    db.add(nuevo_general)
    db.commit()
    db.refresh(nuevo_general)

    for tarea in formulario.tareas:
        nueva_tarea = TareaRT(**tarea.dict(), general_id=nuevo_general.id)
        db.add(nueva_tarea)
    
    for insumo in formulario.insumos:
        nuevo_insumo = InsumoRT(**insumo.dict(), general_id=nuevo_general.id)
        db.add(nuevo_insumo)
    
    db.commit()
    return {"message": "El formulario se ha cargado correctamente, muchas gracias."}

@app.get("/clientes/")
def obtener_clientes(db: Session = Depends(get_db_main)):
    return db.query(Cliente).all()

@app.get("/tareas/")
def obtener_tareas(db: Session = Depends(get_db_main)):
    return db.query(TareaOpcion).all()

@app.get("/piezas/")
def obtener_piezas(db: Session = Depends(get_db_main)):
    return db.query(Pieza).all()

@app.get("/maquinarias/")
def obtener_maquinarias(db: Session = Depends(get_db_main)):
    return db.query(Maquinaria).all()

@app.get("/insumos/")
def obtener_insumos(db: Session = Depends(get_db_main)):
    return db.query(Insumo).all()

@app.get("/insumos/{material}")
def obtener_insumos_por_material(material: str, db: Session = Depends(get_db_main)):
    return db.query(Insumo).filter(Insumo.materiales_insumos == material).all()