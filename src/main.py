import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "iot_temperature.csv"
VIEWS_SQL_PATH = Path(__file__).resolve().parent / "views.sql"


def conectar_banco():
    load_dotenv(BASE_DIR / ".env")

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "iot_db")
    db_user = os.getenv("DB_USER", "student")
    db_password = os.getenv("DB_PASSWORD", "student123")

    conn_str = (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return create_engine(conn_str)


def carregar_dados(caminho_csv=CSV_PATH):
    return pd.read_csv(caminho_csv)


def tratar_dados(df):
    colunas_obrigatorias = {"device_id", "temperature", "timestamp"}
    colunas_recebidas = set(df.columns)

    if not colunas_obrigatorias.issubset(colunas_recebidas):
        faltando = colunas_obrigatorias - colunas_recebidas
        raise ValueError(f"CSV sem colunas obrigatorias: {faltando}")

    dados = df.copy()

    # ajusta tipos e evita erro com valor quebrado
    dados["temperature"] = pd.to_numeric(dados["temperature"], errors="coerce")
    dados["timestamp"] = pd.to_datetime(dados["timestamp"], errors="coerce")

    # remove linhas incompletas depois da conversao
    dados = dados.dropna(subset=["device_id", "temperature", "timestamp"])

    return dados


def inserir_dados(df, engine, tabela="temperature_readings"):
    df.to_sql(tabela, engine, if_exists="append", index=False)


def criar_views(engine, arquivo_sql=VIEWS_SQL_PATH):
    with open(arquivo_sql, "r", encoding="utf-8") as f:
        script = f.read()

    comandos = [cmd.strip() for cmd in script.split(";") if cmd.strip()]

    with engine.begin() as conn:
        for comando in comandos:
            conn.execute(text(comando))


if __name__ == "__main__":
    engine = conectar_banco()
    dados_brutos = carregar_dados()
    dados_tratados = tratar_dados(dados_brutos)
    inserir_dados(dados_tratados, engine)
    criar_views(engine)
