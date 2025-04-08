import os
import re
from typing import Any, Dict, List

import pandas as pd
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Movie
import logging


app = FastAPI()

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependência do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CSV_PATH = os.path.join(os.path.dirname(__file__), "./static/Movielist.csv")

# Carregar os dados do CSV e inserir no banco
def load_csv_to_db(db: Session, csv_path: str = CSV_PATH):
    logger = logging.getLogger(__name__)
    if db.query(Movie).first() is None:
        logger.info("📁 Lendo CSV...")
        df = pd.read_csv(csv_path, sep=";")
        df = df.where(pd.notna(df), None)

        for _, row in df.iterrows():
            logger.debug(f"Inserindo filme: {row['title']}")
            movie = Movie(
                year=int(row["year"]),
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner=True if row["winner"] == "yes" else False
            )
            db.add(movie)
        db.commit()
        logger.info("🎉 Dados inseridos no banco.")
    else:
        logger.info("📦 Banco já contém dados. Pulando carga.")
    db.close()


def get_unique_producers(producers_str):
    producer_set = set()
    for producers in producers_str:
        for producer in producers.split(","):
            producer_set.add(producer.strip())

    return {"unique_producers": list(producer_set)}


def parse_producers(producers_str):
    producers = []
    for producer in producers_str.replace(" and ", ",").split(","):
        producers.append(producer.strip())
    return producers


# Chamar a função para carregar os dados ao iniciar a API
# db = SessionLocal()
# load_csv_to_db(db)

@app.on_event("startup")
def startup_event():
    logger.info("🔄 Inicializando aplicação...")

    logger.info("🔄 Limpando o banco e recarregando os dados...")
    db = SessionLocal()

    # Deleta tudo da tabela Movie
    db.query(Movie).delete()
    db.commit()

    db = SessionLocal()
    load_csv_to_db(db)
    logger.info("✅ Banco carregado com sucesso.")


@app.get("/")
def read_root():
    return {'message': 'API para desafio Outsera!'}


@app.get("/awards/intervals", response_model=Dict[str, Any])
def get_award_intervals(db: Session = Depends(get_db)):
    movies_winners: Movie = db.query(Movie).filter(Movie.winner == True).order_by(Movie.year).all()


    producer_wins: Dict = {}

    for movie in movies_winners:
        producers = parse_producers(movie.producers)
        for producer in producers:
            if producer not in producer_wins:
                producer_wins[producer] = []
            producer_wins[producer].append(movie.year)

    producer_intervals = []
    for producer, years in producer_wins.items():
        if len(years) < 2:
            continue
        years.sort()
        for i in range(1, len(years)):
            interval = years[i] - years[i - 1]
            producer_intervals.append({
                "producer": producer,
                "interval": interval,
                "previousWin": years[i - 1],
                "followingWin": years[i]
            })

    if not producer_intervals:
        return {"min": [], "max": []}

    # min_interval = min([p["interval"] for p in producer_intervals]) if producer_intervals else 0
    # max_interval = max([p["interval"] for p in producer_intervals]) if producer_intervals else 0

    # min_producers = [p for p in producer_intervals if p["interval"] == min_interval]
    # max_producers = [p for p in producer_intervals if p["interval"] == max_interval]

    max_interval = max(producer_intervals, key=lambda x: x["interval"])
    min_interval = min(producer_intervals, key=lambda x: x["interval"])

    return {
        "max": max_interval,
        "min": min_interval
    }
