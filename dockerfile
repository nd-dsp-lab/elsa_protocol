# -------------------------------------------------------------
# NDSS Artifact — ELSA 
# -------------------------------------------------------------
  FROM ubuntu:22.04

  ARG DEBIAN_FRONTEND=noninteractive
  ENV OFHE_VERSION=v1.2.3 \
      OFHE_DIR=/opt/openfhe \
      SRC_DIR=/opt/src \
      PYTHONUNBUFFERED=1 \
      MPLBACKEND=Agg \
      PATH="/usr/local/bin:${PATH}"
  
  # 1) System packages (build + useful tools) + Python runtime
  RUN apt-get update && \
      apt-get install -y --no-install-recommends \
        ca-certificates curl git build-essential cmake g++ \
        libjsonrpccpp-dev libjsonrpccpp-tools \
        libomp-dev openssl libssl-dev \
        parallel time tzdata \
        python3 python3-pip python3-venv \
        fonts-dejavu-core \
      && rm -rf /var/lib/apt/lists/*
  
  # 1.1) Python libs for plotting (headless)
  RUN python3 -m pip install --no-cache-dir \
        numpy==1.26.* pandas==2.2.* matplotlib==3.8.*
  
  # 2) OpenFHE (pinned v1.2.3)
  RUN git clone --depth 1 --branch "${OFHE_VERSION}" \
        https://github.com/openfheorg/openfhe-development.git "${OFHE_DIR}" && \
      mkdir -p "${OFHE_DIR}/build" && cd "${OFHE_DIR}/build" && \
      cmake .. && make -j"$(nproc)" && make install && ldconfig
  
  # 3) Project source → /opt/src (assumes Dockerfile at repo root)
  WORKDIR /opt
  COPY . "${SRC_DIR}"
  
  # 3.5) Make /data resolve to the repo’s data dir expected by the binary
  RUN test -d "${SRC_DIR}/data" && ln -s "${SRC_DIR}/data" /data || mkdir -p /data
  
  # 3.6) Optional symlink for logreg assets
  RUN if [ -d "${SRC_DIR}/logreg" ] && [ ! -e /logreg ]; then ln -s "${SRC_DIR}/logreg" /logreg; fi
  
  # 3.7) Output dir for charts/artifacts (bind-mount host here)
  ENV OUT_DIR=/tmp
  RUN mkdir -p "$OUT_DIR"
  
  # 3.8) Chart runner: executes the 4 scripts and copies figures to $OUT_DIR
  COPY generate_charts/gen_charts.sh /usr/local/bin/gen_charts
  RUN chmod +x /usr/local/bin/gen_charts
  
  # 4) Build into /opt and copy final binaries to /opt/
  RUN rm -rf /opt/build && mkdir -p /opt/build && \
      cmake -S "${SRC_DIR}" -B /opt/build \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=/opt \
        -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=/opt \
        -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=/opt && \
      make -C /opt/build -j"$(nproc)" && \
      if [ -f /opt/build/main ]; then cp /opt/build/main /opt/; fi && \
      if [ -f /opt/build/main_vaf ]; then cp /opt/build/main_vaf /opt/; fi && \
      mkdir -p /opt/data
  
  # 5) Default workdir
  WORKDIR /opt
  