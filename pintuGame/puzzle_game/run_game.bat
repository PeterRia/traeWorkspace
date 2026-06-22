@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -c "import PIL, pygame" >nul 2>nul
if errorlevel 1 (
  echo 正在安装依赖...
  python -m pip install -r requirements.txt
)
python tools\generate_assets.py
python main.py
pause
