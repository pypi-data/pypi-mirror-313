FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/opt/conda/bin:${PATH}"
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY environment.yml /app/
COPY pyproject.toml /app/
COPY server.sh /app/

RUN conda env create -f /app/environment.yml -n executor && conda init bash
RUN poetry config virtualenvs.create false
RUN conda run -n executor poetry install --only main
RUN chmod +x /app/server.sh

CMD ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate executor && /app/server.sh"]
