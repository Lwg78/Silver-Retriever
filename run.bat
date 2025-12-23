@echo off
echo Starting Silver Retriever...
if not exist "data\raw" mkdir data\raw
if not exist "data\temp" mkdir data\temp
streamlit run app.py
pause