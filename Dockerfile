        FROM python:3.9-slim-buster

        WORKDIR /app

        COPY requirements.txt .
        RUN pip install -r requirements.txt

        COPY . .

        RUN echo "Current PYTHONPATH: $PYTHONPATH"  # Check the current PYTHONPATH
        RUN export PYTHONPATH=/app:$PYTHONPATH     # Add /app to PYTHONPATH
        RUN echo "Modified PYTHONPATH: $PYTHONPATH" # Verify the change

        CMD ["python", "bot.py"]
        
