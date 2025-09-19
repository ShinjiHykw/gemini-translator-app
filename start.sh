#!/bin/bash

# 仮想環境を有効にするコマンドを追加
source .venv/bin/activate

# gunicornを起動する
gunicorn app:app