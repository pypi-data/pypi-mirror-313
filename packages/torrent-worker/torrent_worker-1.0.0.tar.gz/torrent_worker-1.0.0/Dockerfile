FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update

RUN apt-get -y install software-properties-common && \
    add-apt-repository ppa:apt-fast/stable && \
    apt-get update && \
    apt-get -y install apt-fast

# Install Python 3.11
#RUN apt-get update && \
#    apt-get -y install apt-fast && \
#    apt-get update

RUN apt-fast install -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-fast update

# Install Python 3.11
RUN apt-fast install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Make Python 3.11 the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

RUN apt-fast update

# Install required packages
RUN apt-fast install -y \
    apt-transport-https \
    ca-certificates \
    dos2unix \
    p7zip-full \
    fuse \
    libfuse2 \
    libharfbuzz0b \
    libxcb-cursor0 \
    libxcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# RUN python3 -m pip install --no-cache-dir --upgrade pip
# for sending files to other devices
COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .

# Extract and prepare qBittorrent
RUN cd bin && \
    7z x qbittorrent-5.0.2_lt20_x86_64.7z.001 && \
    chmod +x qbittorrent-5.0.2_lt20_x86_64.AppImage && \
    mkdir -p extracted && \
    cd extracted && \
    7z x ../qbittorrent-5.0.2_lt20_x86_64.AppImage && \
    chmod +x AppRun AppRun.wrapped && \
    chmod +x usr/bin/* && \
    cd .. && \
    rm -rf *.7z* qbittorrent-5.0.2_lt20_x86_64.AppImage

RUN dos2unix entry_point.sh
RUN python3 -m pip install --no-cache-dir -e .
# Expose the port and then launch the app.
EXPOSE 80
CMD ["/bin/bash", "entry_point.sh"]
