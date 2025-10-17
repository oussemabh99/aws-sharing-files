FROM python:3.13.5
WORKDIR /app    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
COPY auth-server .
ENTRYPOINT ["python", "run.py"]
EXPOSE 5000 
