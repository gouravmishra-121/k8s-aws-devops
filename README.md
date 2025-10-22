Kubernetes on AWS (EKS) with CI/CD, Monitoring & GitHub Actions

This repository demonstrates a production-grade DevOps setup deploying a Flask app to AWS EKS using CI/CD with GitHub Actions, containerized images on ECR, and monitoring via Prometheus & Grafana.

Features

Flask app with Prometheus metrics endpoint (/metrics)

Dockerized container ready for production with Gunicorn

Kubernetes manifests:

Deployment

Service (LoadBalancer)

ConfigMap

Horizontal Pod Autoscaler (HPA)

CI/CD pipeline:

GitHub Actions workflow builds Docker image, pushes to ECR, deploys to EKS

Monitoring stack:

Prometheus + Grafana via Helm

Metrics scraping of the app + cluster resources

Scalable and configurable for production-grade use

Prerequisites

AWS account with an EKS cluster and ECR repository

Local AWS CLI configured (for initial setup)

kubectl installed locally

GitHub repository with Secrets for CI/CD:

AWS_ACCESS_KEY_ID → GitHub Actions IAM user access key

AWS_SECRET_ACCESS_KEY → GitHub Actions IAM secret key

EKS_CLUSTER_NAME → your EKS cluster name

Note: A one-time update to the cluster aws-auth ConfigMap is required to allow the GitHub Actions IAM user to deploy.

Repo Structure
k8s-aws-devops/
├── app/
│   ├── app.py              # Flask app
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── configmap.yaml
├── monitoring/
│   ├── prometheus-values.yaml
│   └── grafana-values.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yaml
├── aws-auth.yaml           # Local copy for cluster update (do not push)
└── README.md

Setup Instructions
1. Clone the repo
git clone <your-repo-url>
cd k8s-aws-devops

2. Create ECR repository
aws ecr create-repository --repository-name flask-demo --region us-east-1

3. Create EKS cluster (if not done already)
eksctl create cluster --name k8AWSDevops --region us-east-1 --nodes 2

4. Update aws-auth ConfigMap

One-time setup to allow GitHub Actions IAM user to deploy:

Export current configmap:

kubectl get configmap aws-auth -n kube-system -o yaml > aws-auth.yaml


Edit aws-auth.yaml and add your GitHub IAM user under mapUsers:

  mapUsers: |
    - userarn: arn:aws:iam::<account-id>:user/github-actions-user
      username: github-actions-user
      groups:
        - system:masters


Apply changes:

kubectl apply -f aws-auth.yaml


Do not push aws-auth.yaml to GitHub; it contains sensitive cluster info.

5. Configure GitHub Secrets

AWS_ACCESS_KEY_ID → GitHub Actions IAM user key

AWS_SECRET_ACCESS_KEY → GitHub Actions IAM user secret

EKS_CLUSTER_NAME → your EKS cluster name

6. Install Prometheus & Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f monitoring/prometheus-values.yaml \
  -f monitoring/grafana-values.yaml


Access Grafana:

kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# open http://localhost:3000
# admin / prom-operator

7. CI/CD Workflow

On push to main (or your branch), GitHub Actions will:

Build Docker image

Push image to ECR

Update Kubernetes deployment manifests

Deploy the Flask app to EKS

IMAGE_TAG is automatically generated from the commit SHA.

8. Test Deployment
kubectl get pods -n demo-app
kubectl get svc -n demo-app
kubectl get hpa -n demo-app


Visit the LoadBalancer URL to see your Flask app running.

Visit Grafana to monitor metrics.

Next Steps / Improvements

Use GitHub OIDC for secure IAM role assumption (no long-lived keys)

Implement Blue/Green or Canary deployments with Argo Rollouts

Configure Grafana dashboards and alerts (Slack/Email)

Use Terraform to manage cluster and ECR infrastructure

Notes

Secrets in GitHub Actions keep your credentials safe.

aws-auth changes are cluster-specific and do not need to be pushed to GitHub.

This README is concise but production-grade ready, covering setup, CI/CD, and monitoring.
