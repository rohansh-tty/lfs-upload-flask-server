FROM python:3.10.2-slim

WORKDIR /app 
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt requirements.txt 

RUN python3 -m pip install -r requirements.txt 

COPY . .    
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main.py"]
