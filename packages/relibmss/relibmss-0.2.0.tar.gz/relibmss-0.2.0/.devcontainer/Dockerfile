# ベースイメージとして最新のUbuntuを使用
FROM ubuntu:22.04

# 環境変数の設定
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    pkg-config \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# ユーザー作成
RUN useradd -m vscode

# 作業ディレクトリの設定
WORKDIR /home/vscode

# vscode ユーザーに切り替え
USER vscode

# Rust のインストール（vscode ユーザーとして）
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# 環境変数 PATH の設定（vscode ユーザー用）
ENV PATH="/home/vscode/.cargo/bin:${PATH}"

# maturin のインストール（vscode ユーザーとして）
RUN pip3 install --user --upgrade pip
RUN pip3 install --user maturin

# .local/bin を PATH に追加
ENV PATH="/home/vscode/.local/bin:${PATH}"

# 作業ディレクトリをホームに設定
WORKDIR /home/vscode

CMD ["/bin/bash"]
