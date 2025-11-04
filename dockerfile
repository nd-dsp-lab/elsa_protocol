# -------------------------------------------------------------
# NDSS Artifact — ELSA 
# -------------------------------------------------------------
  
  FROM ubuntu:22.04

  ARG DEBIAN_FRONTEND=noninteractive
  ENV OFHE_VERSION=v1.2.3 \
      OFHE_DIR=/opt/openfhe \
      SRC_DIR=/opt/src
  
  # 1) System packages (build + useful tools)
  RUN apt-get update && \
      apt-get install -y --no-install-recommends \
        ca-certificates curl git build-essential cmake g++ \
        libjsonrpccpp-dev libjsonrpccpp-tools \
        libomp-dev openssl libssl-dev \
        parallel time tzdata && \
      rm -rf /var/lib/apt/lists/*
  
  # 2) OpenFHE (pinned v1.2.3)
  RUN git clone --depth 1 --branch "${OFHE_VERSION}" \
        https://github.com/openfheorg/openfhe-development.git "${OFHE_DIR}" && \
      mkdir -p "${OFHE_DIR}/build" && cd "${OFHE_DIR}/build" && \
      cmake .. && make -j"$(nproc)" && make install && ldconfig
  
  # 3) Project source → /opt/src (assumes Dockerfile at repo root)
  WORKDIR /opt
  COPY . "${SRC_DIR}"
  
  # 4) Build into /opt and copy final binaries to /opt/
  #    - Out-of-source build at /opt/build
  #    - RUNTIME/LIB/ARCHIVE outputs directed to /opt
  RUN rm -rf /opt/build && mkdir -p /opt/build && \
      cmake -S "${SRC_DIR}" -B /opt/build \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=/opt \
        -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=/opt \
        -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=/opt && \
      make -C /opt/build -j"$(nproc)" && \
      # Fallback copy in case project overrides output dirs
      if [ -f /opt/build/main ]; then cp /opt/build/main /opt/; fi && \
      if [ -f /opt/build/main_vaf ]; then cp /opt/build/main_vaf /opt/; fi && \
      # Ensure a data dir exists for bind-mounts or synthetic sets
      mkdir -p /opt/data
  
  # 5) Default to /opt working directory
  WORKDIR /opt
  
  # No entrypoint; container can be used interactively or with explicit commands.
  # Example (after build):
  #   docker run --rm -it <image> /opt/main 20 5
  #   docker run --rm -it <image> /opt/main_vaf 17 4 4 2 3 0 16 1
  