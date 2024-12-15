FROM python:3.9-slim
WORKDIR /
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
RUN apt-get update && apt-get install -y bash && \
    echo "source .env" >> ~/.bashrc
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]