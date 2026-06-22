@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -c "import PIL, pygame, PyInstaller" >nul 2>nul
if errorlevel 1 (
  echo 正在安装打包依赖...
  python -m pip install -r requirements.txt
)
python tools\generate_assets.py
pyinstaller --noconfirm --windowed --name PuzzleGame --add-data "assets;assets" main.py
if errorlevel 1 (
  echo 打包失败，请查看上方 PyInstaller 输出。
  pause
  exit /b 1
)
echo 打包完成：dist\PuzzleGame\PuzzleGame.exe
pause
