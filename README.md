# Minium Demo for K8s

This is a simplest demo for k8s.
In this project, we will show you how to deploy a web application to k8s step by step.

1. Here we use Python and the Flask framework. We need to prepare two docker images, i.e., `demo-k8s-app` and `demo-k8s-worker`.
    - `demo-k8s-app` is the web application entry point, it has two endpoints:
        - `/hello`: return a hello message.
        - `/time`: call `demo-k8s-worker` to get the local time.
    - `demo-k8s-worker` is the worker that will be called by `demo-k8s-app`.
2. For `demo-k8s-app`, create a file named `app.py` and input the following code:
```python
from flask import Flask
import requests
app = Flask(__name__)


@app.route('/hello')
def hello():
    return "Hello, welcome to the K8s example!"


@app.route('/time')
def get_time():
    url = "http://127.0.0.1:5000/local_time"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

2. Create a file named `requirements.txt`:
```
Flask
request
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
docker build -t your_dockerhub_username/demo-k8s-app .
```

5. Push the docker image to dockerhub:
```bash
docker push your_dockerhub_username/demo-k8s-app 
```
Note that you need to login to dockerhub first using `docker login`.

6. Create `demo-k8s-worker` docker image using the similar steps above. 
Note that we expose the port 5000 for `demo-k8s-worker`, so that `demo-k8s-app` can access it by calling `http://localhost:5000/local_time`.


7. Create a YAML file named `demo-k8s.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-k8s
spec:
  replicas: 3
  selector:
    matchLabels:
      app: demo-k8s
  template:
    metadata:
      labels:
        app: demo-k8s
    spec:
      containers:
      - name: demo-k8s-app
        image: your_dockerhub_username/demo-k8s-app:latest
        ports:
        - containerPort: 80
      - name: demo-k8s-worker
        image: your_dockerhub_username/demo-k8s-worker:latest
        ports:
          - containerPort: 5000

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
curl  --location <external_ip_address>/hello
curl  --location <external_ip_address>/time
```
