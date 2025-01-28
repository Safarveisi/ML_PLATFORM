FROM docker.stackable.tech/stackable/spark-k8s:3.5.2-stackable24.11.0 

COPY requirements.txt  ./

RUN pip install --no-cache-dir --upgrade pip && \   
    pip install --no-cache-dir -r requirements.txt