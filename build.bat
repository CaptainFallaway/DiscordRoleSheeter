@echo off
python -m PyInstaller --name DiscordRoleSheeter --onefile --add-data "src/kv;src/kv" --add-data "src/assets;src/assets" --windowed --icon src\assets\icon.ico src\main.py