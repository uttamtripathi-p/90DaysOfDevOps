# Day 59 — Helm: The Kubernetes Package Manager

---

## What is Helm?

Helm is the **package manager for Kubernetes** — just like `apt` for Ubuntu or `npm` for Node.js. Instead of writing and managing multiple Kubernetes YAML files manually, Helm bundles everything into a single reusable unit called a **chart**.

Without Helm, deploying an app to Kubernetes means manually writing and applying separate YAML files for Deployments, Services, ConfigMaps, Ingress, and more. Helm packages all of that together and lets you install, upgrade, and rollback with a single command.

---

## The Three Core Concepts

### 1. Chart
A Chart is a **package** — a collection of Kubernetes YAML templates bundled together. Think of it like a Docker image but for Kubernetes deployments. Charts can be shared and reused.

```
my-app/
├── Chart.yaml          ← chart metadata (name, version, description)
├── values.yaml         ← default configuration values
├── charts/             ← dependent charts
└── templates/          ← Kubernetes YAML templates with placeholders
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── _helpers.tpl    ← reusable template functions
```

### 2. Repository
A Repository is a **collection of charts** hosted online — just like Docker Hub for images or npm registry for packages.

```bash
# Bitnami's chart repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Search for charts
helm search repo nginx
```

### 3. Release
A Release is a **running instance** of a chart in your cluster. You can install the same chart multiple times with different release names — each is an independent release.

```bash
helm install my-nginx      bitnami/nginx   # release 1 → production
helm install staging-nginx bitnami/nginx   # release 2 → staging
helm install test-nginx    bitnami/nginx   # release 3 → testing
```

---

## Install, Customize, Upgrade, and Rollback

### Install

```bash
# Basic install
helm install my-nginx bitnami/nginx

# Install with custom values inline
helm install my-nginx bitnami/nginx \
  --set replicaCount=3 \
  --set service.type=NodePort

# Install with a values file
helm install my-nginx bitnami/nginx -f custom-values.yaml

# Install or upgrade in one command (best for CI/CD)
helm upgrade --install my-nginx bitnami/nginx -f custom-values.yaml
```

### Customize

Before installing, check what values you can change:

```bash
# View all default values
helm show values bitnami/nginx

# Filter specific section
helm show values bitnami/nginx | grep -A 10 "^service:"
```

### Upgrade

```bash
# Upgrade with new values
helm upgrade my-nginx bitnami/nginx \
  --set replicaCount=5

# Upgrade keeping existing values
helm upgrade my-nginx bitnami/nginx \
  --set replicaCount=5 \
  --reuse-values
```

### Rollback

```bash
# Check release history
helm history my-nginx

# Rollback to previous version
helm rollback my-nginx 1

# Rollback to specific revision
helm rollback my-nginx 2
```

---

## Helm Chart Structure

```
my-app/
├── Chart.yaml
├── values.yaml
├── charts/
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── serviceaccount.yaml
    ├── NOTES.txt
    └── _helpers.tpl
```

### Chart.yaml — Chart Metadata

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for Kubernetes
type: application
version: 0.1.0        # chart version
appVersion: "1.16.0"  # actual app version
```

### values.yaml — Default Values

```yaml
replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""

service:
  type: ClusterIP
  port: 80

resources: {}
```

---

## Go Template Syntax

Helm uses Go's templating engine to dynamically fill in Kubernetes YAML at install time. The `{{ }}` syntax marks placeholders that get replaced with real values.

### Basic Value Injection

```yaml
replicas: {{ .Values.replicaCount }}        # → replicas: 3
- name: {{ .Chart.Name }}                   # → - name: my-app
namespace: {{ .Release.Namespace }}         # → namespace: default
```

### Three Template Data Sources

| Source | Example | Comes From |
|---|---|---|
| `.Values` | `{{ .Values.replicaCount }}` | values.yaml |
| `.Chart` | `{{ .Chart.Name }}` | Chart.yaml |
| `.Release` | `{{ .Release.Name }}` | helm install command |

### Common Template Functions

```yaml
# include — reusable helper functions from _helpers.tpl
name: {{ include "my-app.fullname" . }}

# nindent — control indentation
labels:
  {{- include "my-app.labels" . | nindent 4 }}

# default — fallback value if empty
image: "nginx:{{ .Values.image.tag | default .Chart.AppVersion }}"

# if/end — conditional blocks
{{- if not .Values.autoscaling.enabled }}
replicas: {{ .Values.replicaCount }}
{{- end }}

# with/end — conditional + context change
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 12 }}
{{- end }}

# toYaml — convert object to YAML string
{{- toYaml .Values.resources | nindent 12 }}
```

### Whitespace Control

```yaml
{{-   →  trim whitespace BEFORE this tag
-}}   →  trim whitespace AFTER this tag
|     →  pipe output into next function (just like Linux pipes!)
```

### Debug Templates Without Installing

```bash
# See final rendered YAML without touching the cluster
helm template my-release my-app/

# Validate against cluster
helm template my-release my-app/ | kubectl apply --dry-run=client -f -

# Lint the chart
helm lint my-app/
```

---

## custom-values.yaml

```yaml
# Number of pod replicas to run
replicaCount: 3

# Expose app via NodePort so it's accessible on the node's IP
service:
  type: NodePort
  nodePorts:
    http: 30080     # pin to a specific port (30000-32767 range)

# Resource limits — controls how much CPU/memory each pod can use
resources:

  # requests = guaranteed minimum resources reserved for the pod
  requests:
    cpu: "100m"       # 100 millicores = 0.1 of a CPU core
    memory: "128Mi"   # 128 megabytes guaranteed

  # limits = hard maximum — pod gets killed if it exceeds memory limit
  limits:
    cpu: "250m"       # max 0.25 of a CPU core
    memory: "256Mi"   # max 256 megabytes — OOMKilled if exceeded
```

### Apply It

```bash
# Fresh install
helm install my-nginx bitnami/nginx -f custom-values.yaml

# Upgrade existing release
helm upgrade --install my-nginx bitnami/nginx -f custom-values.yaml

# Combine file with inline override
helm upgrade --install my-nginx bitnami/nginx \
  -f custom-values.yaml \
  --set replicaCount=5    # --set always overrides -f
```

### Verify Resources Were Applied

```bash
kubectl describe pod -l app.kubernetes.io/instance=my-nginx | grep -A 6 "Limits:"
```

---

## Key Commands Cheatsheet

```bash
# Repo management
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx

# Chart info
helm show values bitnami/nginx
helm show chart bitnami/nginx

# Install / Upgrade
helm install <release> <chart> -f values.yaml
helm upgrade --install <release> <chart> -f values.yaml

# Inspect
helm list
helm status my-nginx
helm history my-nginx

# Rollback
helm rollback my-nginx 1

# Remove
helm uninstall my-nginx

# Development
helm create my-app
helm lint my-app/
helm template my-release my-app/
helm package my-app/
```

---

## Mental Model

```
Chart      =  the recipe
Values     =  your ingredients
Release    =  the cooked dish running in your cluster

helm install  =  cook the dish using the recipe + your ingredients
helm upgrade  =  remake the dish with new ingredients
helm rollback =  go back to how the dish was before
```

> Helm doesn't just deploy — it manages the full lifecycle of your app in Kubernetes. Install, upgrade, rollback, uninstall — all with one tool. 🚀
