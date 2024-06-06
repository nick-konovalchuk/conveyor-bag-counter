FROM python:3.10-slim

RUN mkdir /app

COPY requirements.txt .
RUN pip install uv && uv pip install --system -r requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-dev \
        libsm6 libxext6 libxrender-dev libglib2.0-0 \
        libopenblas-dev \
        libomp5 libomp-dev

COPY . .
WORKDIR src

ENTRYPOINT streamlit run main.py --server.address 0.0.0.0 --server.port 5000