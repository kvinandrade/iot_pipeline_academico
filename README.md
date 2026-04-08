# Pipeline de Dados com IoT e PostgreSQL

Projeto acadêmico para ingestão, tratamento e análise de dados de temperatura de sensores IoT com Python, PostgreSQL e Streamlit.

Disciplina: Disruptive Architectures: IoT, Big Data e IA (UniFECAF)

## Tecnologias Utilizadas

- Python 3.11
- Pandas
- SQLAlchemy
- psycopg2-binary
- PostgreSQL
- Streamlit
- Plotly
- Docker Compose

## Estrutura de Pastas

```text
iot_pipeline_academico/
├── src/
│   ├── main.py
│   ├── dashboard.py
│   └── views.sql
├── data/
│   └── iot_temperature.csv
├── docs/
│   ├── grafico1_media_por_dispositivo.png
│   ├── grafico2_leituras_por_hora.png
│   └── grafico3_temp_max_min.png
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/kvinandrade/iot_pipeline_academico.git
cd iot_pipeline_academico
```

### 2. Criar ambiente virtual e instalar dependências

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```bash
copy .env.example .env
```

### 4. Subir PostgreSQL com Docker

```bash
docker compose up -d
```

### 5. Executar pipeline de ingestão

```bash
python src/main.py
```

### 6. Executar dashboard

```bash
streamlit run src/dashboard.py
```

Acesse no navegador: http://localhost:8501

## Views SQL Implementadas

As views estão no arquivo `src/views.sql`:

- `avg_temp_por_dispositivo`: calcula média de temperatura por sensor.
- `leituras_por_hora`: conta total de leituras por hora.
- `temp_max_min_por_dia`: mostra temperatura máxima e mínima por dia.

## Dashboard (3 Gráficos)

### Gráfico 1 - Média por dispositivo
![Grafico 1](docs/grafico1_media_por_dispositivo.png)

### Gráfico 2 - Leituras por hora
![Grafico 2](docs/grafico2_leituras_por_hora.png)

### Gráfico 3 - Temperatura máxima e mínima por dia
![Grafico 3](docs/grafico3_temp_max_min.png)

## Insights Obtidos

- O sensor_03 apresentou a maior média de temperatura.
- A frequência de leituras variou ao longo das horas.
- A diferença entre temperatura máxima e mínima por dia foi identificável no período analisado.

## Comandos Git Utilizados

```bash
git init
git add .
git commit -m "Projeto IoT completo"
git remote add origin https://github.com/kvinandrade/iot_pipeline_academico.git
git push -u origin master
```
