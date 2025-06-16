FROM openfabric/tee-python-cpu:dev

# --- Step 1: Upgrade SQLite ---
RUN apt-get update && \
    apt-get install -y wget build-essential libreadline-dev libssl-dev libsqlite3-dev && \
    wget https://www.sqlite.org/2022/sqlite-autoconf-3390200.tar.gz && \
    tar xzf sqlite-autoconf-3390200.tar.gz && \
    cd sqlite-autoconf-3390200 && \
    ./configure --prefix=/usr/local && \
    make && make install && \
    ldconfig && \
    sqlite3 --version

# --- Step 2: Poetry & Dependency Installation ---
COPY pyproject.toml ./
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts}

# --- Step 3: Additional Packages ---
RUN python3 -m pip install --no-cache-dir \
    faiss-cpu \
    numpy \
    pillow \
    ollama \ 
    sentence-transformers

# --- Step 4: Copy Code ---
COPY . .

# --- Step 5: Port & Entrypoint ---
EXPOSE 8888
CMD ["sh", "start.sh"]
