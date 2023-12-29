# Minium Demo for K8s

This is a simplest demo for k8s.
In this project, we will show you how to deploy a web application to k8s step by step.

1. Here we use Python and the Flask framework. Create a file named `app.py` and input the following code:
```python
from flask import Flask  
  
app = Flask(__name__)  
  
@app.route('/')  
def hello():  
    return "Hello, welcome to the K8s example!"  
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=80) 
```

2. Create a file named `requirements.txt`:
```
Flask
```

3. Create a file named `Dockerfile`:
```
FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

4. Build the docker image:
```bash
docker build -t your_dockerhub_username/demo-k8s .
```

5. Test the docker image locally:
```bash
docker run -p 80:80 your_dockerhub_username/demo-k8s
```

6. Push the docker image to dockerhub:
```bash
docker push your_dockerhub_username/demo-k8s
```
Note that you need to login to dockerhub first using `docker login`.

7. Create a YAML file named `demo-k8s.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-k8s
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-k8s
  template:
    metadata:
      labels:
        app: demo-k8s
    spec:
      containers:
      - name: demo-k8s
        image: your_dockerhub_username/demo-k8s:latest
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: demo-k8s
spec:
  selector:
    app: demo-k8s
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

8. Deploy the application to k8s:
```bash
kubectl apply -f demo-k8s.yaml
```

9. Get the external IP address of the service:
```bash
kubectl get service demo-k8s
```

10. Visit the application using the external IP address.
```bash
curl  --location <external_ip_address>
```
