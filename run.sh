#!/bin/bash
echo "Starting Silver Retriever..."
# Check if data folders exist, if not create them
mkdir -p data/raw
mkdir -p data/temp

# Run the app
streamlit run app.py