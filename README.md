# k8s-aws-devops

> Small example project showing how to build a simple Flask app, containerize it, and deploy to Kubernetes with observability values for Prometheus and Grafana.


Table of Contents
- Overview
- Repo layout
- Quickstart
- Build & push image
- Deploy to Kubernetes
- Monitoring
- Files of interest
- License
- Contact

Overview
This repo contains a tiny Flask sample app (app/app.py), a Dockerfile to build the image, Kubernetes manifests in k8s/ for deploying the app, and monitoring Helm values for Prometheus & Grafana in monitoring/.

Repo layout (key items)
- app/ — Flask app, Dockerfile, Python deps
  - app/app.py — simple Flask service
  - app/Dockerfile — Dockerfile for the Flask app
  - app/requirements.txt — Python dependencies
- k8s/ — Kubernetes manifests
  - namespace.yaml
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - flask-servicemonitor.yaml
- monitoring/ — Helm values for observability components
  - prometheus-values.yaml
  - grafana-values.yaml
- .github/workflows/ — CI/CD workflow templates (if present)
- LICENSE — MIT

Quickstart (example)
1. Clone the repo
```bash
git clone https://github.com/gouravmishra-121/k8s-aws-devops.git
cd k8s-aws-devops
```

2. Build the Docker image locally
```bash
docker build -t myapp:latest -f app/Dockerfile app/
```

3. (Optional) Tag & push to your registry (example: ECR, Docker Hub)
```bash
# Example Docker Hub
docker tag myapp:latest your-dockerhub-username/myapp:latest
docker push your-dockerhub-username/myapp:latest

# Example ECR (assumes repo exists and you are authenticated)
docker tag myapp:latest <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/myapp:latest
docker push <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/myapp:latest
```

Deploy to Kubernetes
1. Ensure kubeconfig points to your cluster
2. Apply namespace + manifests
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/flask-servicemonitor.yaml   # if you use Prometheus Operator
```

3. Verify
```bash
kubectl -n <namespace-from-namespace.yaml> get pods,svc
kubectl -n <namespace> rollout status deployment/<deployment-name>
```

Monitoring
- Prometheus/Grafana values are in monitoring/prometheus-values.yaml and monitoring/grafana-values.yaml. Use these with your Helm chart installs for prometheus/grafana to configure scraping and dashboards.
- The repo includes a ServiceMonitor manifest (k8s/flask-servicemonitor.yaml) compatible with Prometheus Operator.

Files of interest (direct links)
- app/app.py — https://github.com/gouravmishra-121/k8s-aws-devops/blob/main/app/app.py  
- app/Dockerfile — https://github.com/gouravmishra-121/k8s-aws-devops/blob/main/app/Dockerfile  
- k8s/deployment.yaml — https://github.com/gouravmishra-121/k8s-aws-devops/blob/main/k8s/deployment.yaml  
- k8s/service.yaml — https://github.com/gouravmishra-121/k8s-aws-devops/blob/main/k8s/service.yaml  
- monitoring/prometheus-values.yaml — https://github.com/gouravmishra-121/k8s-aws-devops/blob/main/monitoring/prometheus-values.yaml  
- monitoring/grafana-values.yaml — https://github.com/gouravmishra-121/k8s-aws-devops/blob/main/monitoring/grafana-values.yaml

Notes & recommendations
- Replace placeholder image references in k8s/deployment.yaml with your image registry and tag.
- If you want automated CI/CD, the .github/workflows directory contains workflow templates you can adapt to build, test, push, and deploy.
- Use Secrets (AWS Secrets Manager / Kubernetes Secrets) instead of embedding credentials in manifests.

License
This project is licensed under the MIT License — see LICENSE.

Contact
Maintainer: gouravmishra-121 — https://github.com/gouravmishra-121
