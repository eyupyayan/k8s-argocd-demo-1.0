# Kubernetes + Argo CD GitOps Demo

Dette prosjektet er laget for å lære **Kubernetes**, **Kustomize**, **Docker** og **Argo CD (GitOps)** fra bunnen av.
Målet er å bygge en realistisk app, containerisere den, deploye den i flere miljøer og styre alt deklarativt via Git.

---

## Innhold

* Python FastAPI applikasjon
* Docker container
* Docker Hub image
* Kubernetes manifests
* Kustomize overlays (dev / prod)
* Namespaces
* ConfigMaps
* Secrets
* Ingress
* Argo CD GitOps
* (Senere: Prometheus + Grafana)

---

## Teknologier

* Python / FastAPI
* Docker
* Kubernetes (Docker Desktop)
* Kustomize
* Argo CD
* Git

---

## Prosjektstruktur

```text
.
├─ app/
│  ├─ main.py
│  └─ requirements.txt
│
├─ Dockerfile
├─ .dockerignore
│
├─ k8s/
│  ├─ base/
│  │  ├─ deployment.yaml
│  │  ├─ service.yaml
│  │  ├─ configmap.yaml
│  │  ├─ secret.yaml
│  │  ├─ ingress.yaml
│  │  └─ kustomization.yaml
│  │
│  └─ overlays/
│     ├─ dev/
│     │  ├─ namespace.yaml
│     │  ├─ patch-deployment.yaml
│     │  ├─ configmap-patch.yaml
│     │  ├─ secret-patch.yaml
│     │  ├─ ingress-patch.yaml
│     │  └─ kustomization.yaml
│     │
│     └─ prod/
│        ├─ namespace.yaml
│        ├─ patch-deployment.yaml
│        ├─ configmap-patch.yaml
│        ├─ secret-patch.yaml
│        ├─ ingress-patch.yaml
│        └─ kustomization.yaml
│
└─ argocd/
   ├─ apps/
   │  ├─ demo-dev.yaml
   │  └─ demo-prod.yaml
   │
   └─ root/
      └─ app-of-apps.yaml
```

---

## Applikasjon

FastAPI app med:

* `/` – hovedside
* `/healthz` – liveness probe
* `/readyz` – readiness probe
* `/metrics` – Prometheus metrics
* miljøvariabler via ConfigMap og Secret

---

## Docker

### Bygg image

```bash
docker build -t <dockerhub_user>/k8s-argocd-demo:0.1.0 .
```

### Kjør lokalt

```bash
docker run -p 8000:8000 <dockerhub_user>/k8s-argocd-demo:0.1.0
```

### Push til Docker Hub

```bash
docker login
docker push <dockerhub_user>/k8s-argocd-demo:0.1.0
```

---

## Kubernetes

### Opprett namespaces

```bash
kubectl create ns dev
kubectl create ns prod
```

### Deploy med Kustomize

#### Dev

```bash
kubectl apply -k k8s/overlays/dev
```

#### Prod

```bash
kubectl apply -k k8s/overlays/prod
```

---

## Ingress

Legg til i hosts-fil:

```text
127.0.0.1 dev.demo.local
127.0.0.1 demo.local
```

Test:

* [http://dev.demo.local](http://dev.demo.local)
* [http://demo.local](http://demo.local)

---

## Argo CD

### Installer Argo CD

```bash
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Åpne UI

```bash
kubectl -n argocd port-forward svc/argocd-server 8081:80
```

Hent passord:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 --decode; echo
```

Åpne:
[http://localhost:8081](http://localhost:8081)

---

## Argo CD Applications

Prosjektet bruker **deklarativ GitOps**:

* `demo-dev.yaml` → deployer `k8s/overlays/dev`
* `demo-prod.yaml` → deployer `k8s/overlays/prod`
* `app-of-apps.yaml` → root som styrer alle apps

Sync policy:

* **automated**
* **prune**
* **selfHeal**
* **CreateNamespace**

---

## Læringsmål

Dette prosjektet trener på:

* Containerisering
* Kubernetes objekter
* Namespaces
* ConfigMaps vs Secrets
* Ingress networking
* Kustomize overlays
* GitOps prinsipper
* Argo CD Applications
* App-of-Apps pattern
* Drift av flere miljøer

---

## Neste steg

* Prometheus
* Grafana dashboards
* HPA (Horizontal Pod Autoscaler)
* Sealed Secrets / External Secrets
* RBAC
* CI/CD pipeline

---

## Kommandoer for feilsøking

```bash
kubectl get all -n dev
kubectl describe pod <pod> -n dev
kubectl logs <pod> -n dev
kubectl -n argocd get applications
```

---

Dette repoet er ment som en **praktisk læringsplattform** for Kubernetes og GitOps, ikke bare en demo-app.
