import os
import pandas as pd
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent


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


def carregar_view(engine, nome_view):
    views_validas = {
        "avg_temp_por_dispositivo",
        "leituras_por_hora",
        "temp_max_min_por_dia",
    }

    if nome_view not in views_validas:
        raise ValueError("Nome de view invalido")

    query = text(f"SELECT * FROM {nome_view}")

    with engine.connect() as conn:
        return pd.read_sql(query, conn)


def main():
    st.set_page_config(page_title="Dashboard IoT", layout="wide")
    st.title("Dashboard de Temperatura IoT")

    engine = conectar_banco()

    df_media = carregar_view(engine, "avg_temp_por_dispositivo")
    df_hora = carregar_view(engine, "leituras_por_hora")
    df_dia = carregar_view(engine, "temp_max_min_por_dia")

    fig1 = px.bar(
        df_media,
        x="device_id",
        y="media_temperatura",
        title="Media por dispositivo",
        labels={"device_id": "Dispositivo", "media_temperatura": "Media"},
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        df_hora,
        x="hora",
        y="total_leituras",
        title="Leituras por hora",
        labels={"hora": "Hora", "total_leituras": "Total de leituras"},
    )
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=df_dia["dia"],
            y=df_dia["temp_max"],
            mode="lines+markers",
            name="Temp maxima",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=df_dia["dia"],
            y=df_dia["temp_min"],
            mode="lines+markers",
            name="Temp minima",
        )
    )
    fig3.update_layout(
        title="Temperatura maxima e minima por dia",
        xaxis_title="Dia",
        yaxis_title="Temperatura",
    )
    st.plotly_chart(fig3, use_container_width=True)


if __name__ == "__main__":
    main()
