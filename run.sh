#!/bin/bash
# Скрипт для запуска приложения "Подготовка к охотничьему экзамену"
# Устанавливает путь к библиотекам tk и tcl, скопированным в пользовательскую директорию

export LD_LIBRARY_PATH="/home/went/.local/lib:$LD_LIBRARY_PATH"
cd "$(dirname "$0")"
python3 main.py "$@"
