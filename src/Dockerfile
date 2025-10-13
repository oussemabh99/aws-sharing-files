FROM python:3.9.21-slim
WORKDIR /app    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
COPY auth-server .
CMD ["python", "app.py"]
EXPOSE 5000 