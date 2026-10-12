FROM python:3.12-slim
# JRE (для plantuml.jar) + Graphviz для layout'а
# диаграмм (component, deployment, usecase, class)
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-jre-headless graphviz \
    && rm -rf /var/lib/apt/lists/*
# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем FastMCP
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY plantuml.jar .
# Копируем код сервера
COPY server.py .

ENV PLANTUML_JAR=/app/plantuml.jar
ENV JAVA_BIN=java
