from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os

# Configuração do banco de dados SQLite local
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "performance.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Jogador(Base):
    __tablename__ = "jogadores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    posicao = Column(String)
    numero = Column(Integer)
    idade = Column(Integer)
    minutos_jogados = Column(Integer, default=0)
    
    # Relações
    eventos = relationship("Evento", back_populates="jogador")

class Partida(Base):
    __tablename__ = "partidas"
    
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date)
    adversario = Column(String)
    local = Column(String) # 'Casa' ou 'Fora'
    gols_pro = Column(Integer)
    gols_contra = Column(Integer)
    vitoria = Column(Boolean)
    empate = Column(Boolean)
    derrota = Column(Boolean)
    
    # Relações
    eventos = relationship("Evento", back_populates="partida")

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"))
    jogador_id = Column(Integer, ForeignKey("jogadores.id"))
    
    tipo = Column(String) # 'Chute', 'Passe', 'Defesa', 'Cartao_Amarelo', etc
    minuto = Column(Integer)
    
    # Coordenadas do campo para mapas (0 a 100 ou 0 a 120 dependendo da config)
    x = Column(Float, nullable=True) 
    y = Column(Float, nullable=True)
    
    # Métricas avançadas
    xg = Column(Float, nullable=True) # Expected Goals
    xa = Column(Float, nullable=True) # Expected Assists
    sucesso = Column(Boolean, default=True) # Se foi gol, se o passe foi certo, etc.
    
    # Relações
    jogador = relationship("Jogador", back_populates="eventos")
    partida = relationship("Partida", back_populates="eventos")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
