FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./start.sh

EXPOSE 80

RUN pip install psycopg2-binary

# Run all services using the script
CMD ["./start.sh"]
