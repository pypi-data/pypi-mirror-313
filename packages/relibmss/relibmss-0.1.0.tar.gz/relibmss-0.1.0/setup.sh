#!/bin/bash
set -e

# 仮想環境の作成
python3 -m venv .venv

# 仮想環境の有効化
source .venv/bin/activate

# pip のアップグレード
pip install --upgrade pip

# 依存関係のインストール
pip install -r dev-requirements.txt

