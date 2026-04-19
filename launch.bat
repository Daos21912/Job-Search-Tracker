@echo off
cd /d "%~dp0"

echo Starting Apps...

call venv\Scripts\activate.bat

streamlit run Home.py --server.headless false