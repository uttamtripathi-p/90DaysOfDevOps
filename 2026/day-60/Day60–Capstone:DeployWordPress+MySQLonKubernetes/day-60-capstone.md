# Day 60 — Capstone: WordPress + MySQL on Kubernetes

**Challenge:** 90 Days of DevOps  
**Date:** April 22, 2026  
**Namespace:** `capstone`  
**Cluster:** 2-node Kind cluster (1 control-plane + 1 worker)

---

## Architecture

```
                        ┌─────────────────────────────────────────┐
                        │           Kubernetes Cluster             │
                        │                                          │
                        │   ┌──────────────────────────────────┐  │
                        │   │         capstone namespace        │  │
                        │   │                                   │  │
  Browser / User ──────────►│  NodePort Service (wp-service)   │  │
  :30008 / port-forward │   │         port: 80                  │  │
                        │   └──────────────┬───────────────────┘  │
                        │                  │ routes to             │
                        │   ┌──────────────▼───────────────────┐  │
                        │   │     WordPress Deployment          │  │
                        │   │     (2 replicas, HPA 2–10)        │  │
                        │   │                                   │  │
                        │   │  ┌─────────┐  ┌─────────┐        │  │
                        │   │  │ wp-pod-1│  │ wp-pod-2│        │  │
                        │   │  │         │  │         │        │  │
                        │   │  │ envFrom │  │ envFrom │        │  │
                        │   │  │ myconfig│  │ myconfig│        │  │
                        │   │  │         │  │         │        │  │
                        │   │  │ secretKeyRef         │        │  │
                        │   │  │ my-secret            │        │  │
                        │   └──┴────┬────┴──┴─────────┘        │  │
                        │           │ connects via DNS           │  │
                        │   ┌───────▼──────────────────────┐   │  │
                        │   │  Headless Service (my-service)│   │  │
                        │   │  ClusterIP: None, port: 3306  │   │  │
                        │   └───────┬──────────────────────┘   │  │
                        │           │ routes to                  │  │
                        │   ┌───────▼──────────────────────┐   │  │
                        │   │     MySQL StatefulSet         │   │  │
                        │   │     (3 replicas)              │   │  │
                        │   │                               │   │  │
                        │   │  mysql-0 (primary write)      │   │  │
                        │   │  mysql-1 (replica)            │   │  │
                        │   │  mysql-2 (replica)            │   │  │
                        │   │                               │   │  │
                        │   │  each pod → PVC (1Gi RWO)     │   │  │
                        │   └───────────────────────────────┘   │  │
                        │                                        │  │
                        │   ┌──────────────┐  ┌──────────────┐  │  │
                        │   │  ConfigMap   │  │   Secret     │  │  │
                        │   │  myconfig    │  │  my-secret   │  │  │
                        │   │              │  │              │  │  │
                        │   │ DB_HOST      │  │ MYSQL_USER   │  │  │
                        │   │ DB_NAME      │  │ MYSQL_PASS   │  │  │
                        │   │              │  │ MYSQL_ROOT   │  │  │
                        │   │              │  │ MYSQL_DB     │  │  │
                        │   └──────────────┘  └──────────────┘  │  │
                        │                                        │  │
                        │   ┌──────────────────────────────────┐ │  │
                        │   │  HorizontalPodAutoscaler (HPA)   │ │  │
                        │   │  target: wp-deployment           │ │  │
                        │   │  CPU threshold: 50%              │ │  │
                        │   │  min: 2 replicas, max: 10        │ │  │
                        │   └──────────────────────────────────┘ │  │
                        │                                         │  │
                        └─────────────────────────────────────────┘
```

---

## Resources Summary

| Resource | Kind | Name | Purpose |
|---|---|---|---|
| `myconfig` | ConfigMap | DB host + DB name | Inject non-sensitive config into WordPress pods |
| `my-secret` | Secret | DB credentials | Securely inject MySQL user/password/root |
| `mysql` | StatefulSet | 3-replica MySQL | Persistent, ordered DB cluster |
| `my-service` | Service (Headless) | MySQL DNS | Stable DNS for each MySQL pod (`mysql-0.my-service...`) |
| `wp-deployment` | Deployment | 2-replica WordPress | Stateless app layer, auto-restarts on failure |
| `wp-service` | Service (NodePort) | Expose WordPress | External access on port 30008 |
| `hpa` | HorizontalPodAutoscaler | Auto-scale WordPress | Scale 2–10 replicas based on CPU usage |
| PVC x3 | PersistentVolumeClaim | 1Gi each per MySQL pod | Durable MySQL data storage across restarts |

---

## Resource Connection Map

```
myconfig  ──────────────────────► wp-pod (envFrom)
my-secret ──────────────────────► wp-pod (secretKeyRef: MYSQL_USER, MYSQL_PASSWORD)
my-secret ──────────────────────► mysql-pod (envFrom: MYSQL_ROOT_PASSWORD, MYSQL_DATABASE)

wp-pod ─── DNS lookup ──────────► my-service (headless)
my-service ─── routes to ───────► mysql-0.my-service.capstone.svc.cluster.local:3306

PVC-0 ──────────────────────────► mysql-0 (/var/lib/mysql)
PVC-1 ──────────────────────────► mysql-1 (/var/lib/mysql)
PVC-2 ──────────────────────────► mysql-2 (/var/lib/mysql)

HPA ────── watches CPU ─────────► wp-deployment (scales 2 → 10 replicas)
NodePort ──────────────────────► wp-deployment (external traffic → port 80)
```

---

## Self-Healing Test Results

### Test 1 — WordPress Pod Killed Manually

```bash
kubectl delete pod wp-deployment-556f6b7d75-jzwwl -n capstone
```

| Step | Observation |
|---|---|
| Pod deleted | ReplicaSet detected 1/2 running |
| New pod spawned | Within ~5 seconds |
| Readiness probe ran | Pod marked ready after ~60s |
| Traffic restored | Automatically routed to healthy pod |

**Result: ✅ Self-healed automatically. Zero manual intervention needed.**

---

### Test 2 — Liveness Probe Failure (HTTP 500)

During debugging, WordPress pods were returning HTTP 500 due to wrong DB hostname in ConfigMap.

| Step | Observation |
|---|---|
| Liveness probe detected 500 | After `failureThreshold: 3` failures |
| Container killed | `Killing container: failed liveness probe` |
| Container restarted | New container started in same pod |
| Restart count incremented | Visible in `kubectl get pods` |

**Result: ✅ Liveness probe correctly identified unhealthy containers and triggered restarts.**

---

### Test 3 — MySQL Pod Restart with Persistent Data

MySQL pods restarted (simulated via node restart, `RESTARTS: 1` visible in output).

```bash
kubectl get pods -n capstone
# mysql-0   1/1   Running   1 (99m ago)   21h
```

| Step | Observation |
|---|---|
| MySQL pod restarted | PVC retained all data |
| Pod came back up | Same PVC re-attached |
| WordPress reconnected | No data loss, DB intact |

**Result: ✅ PersistentVolumeClaims survived pod restarts. Data persisted across restarts.**

---

## Concept → Day Learned Table

| Concept | Day Learned | Applied In Capstone |
|---|---|---|
| Linux fundamentals | Day 1–7 | Debugging inside pods with `bash`, `cat`, `env` |
| Docker & containers | Day 10–20 | WordPress & MySQL images, Dockerfile |
| Docker networking | Day 18 | K8s Services, DNS resolution |
| Docker volumes | Day 19 | K8s PersistentVolumes, PVCs |
| YAML syntax | Day 22 | All K8s manifests |
| Kubernetes basics | Day 30 | Deployments, Pods, Namespaces |
| ConfigMaps | Day 32 | `myconfig` — DB host and name |
| Secrets | Day 32 | `my-secret` — DB credentials |
| Deployments | Day 33 | `wp-deployment` — WordPress |
| Services | Day 34 | `my-service` (headless), `wp-service` (NodePort) |
| StatefulSets | Day 38 | `mysql` StatefulSet — ordered MySQL pods |
| PersistentVolumes | Day 39 | MySQL data durability across restarts |
| Liveness Probes | Day 42 | WordPress container health checking |
| Readiness Probes | Day 42 | WordPress traffic routing control |
| Resource limits | Day 43 | CPU/memory requests & limits on all pods |
| HPA autoscaling | Day 50 | Scale WordPress 2–10 replicas on CPU |
| K8s DNS | Day 35 | `mysql-0.my-service.capstone.svc.cluster.local` |
| Namespaces | Day 31 | All resources isolated in `capstone` |
| kubectl debugging | Day 31–60 | `describe`, `logs`, `exec`, `get events` |
| CI/CD (GitHub Actions) | Day 25 | Foundation for future image auto-deploy |

---

## Reflection

### 🔴 What Was Hardest

**DNS and service naming** was the single most painful issue. The ConfigMap had `mysql` as the service name but the actual service was named `my-service`. This caused `Name or service not known` errors that took significant debugging to trace. The lesson: always run `kubectl get svc -n <namespace>` before writing any hostname into config files.

**Database name mismatch** was equally subtle — MySQL created a database called `mydb` (from the Secret's `MYSQL_DATABASE` key) but the ConfigMap told WordPress to connect to `wordpress`. No error message said "database not found" directly — it just showed a generic HTTP 500, requiring deeper log inspection to discover.

**Memory pressure** on the single worker node was a constant constraint. With 3 MySQL pods already consuming ~1.5Gi in requests, WordPress pods kept hitting `Insufficient memory` scheduling failures. Tuning resource requests down from 500Mi to 128Mi per pod was necessary to fit everything on one worker node.

---

### 🟢 What Clicked

**The StatefulSet + Headless Service + PVC pattern** finally made complete sense after seeing it work live. The way `mysql-0.my-service.capstone.svc.cluster.local` resolves to a specific pod — not a random one — is elegant and exactly why StatefulSets exist for databases.

**Probes as a self-healing mechanism** clicked deeply. Watching the liveness probe kill and restart a container that was stuck in HTTP 500, and then watching it recover automatically once the config was fixed — that's the real power of Kubernetes declarative model.

**The ConfigMap + Secret separation** felt natural by the end. Non-sensitive config in ConfigMap, sensitive credentials in Secret. Clean, auditable, and easy to rotate independently.

---

### 🔵 What I Would Add for Production

| Addition | Reason |
|---|---|
| **MySQL replication config** | Currently 3 pods but no actual primary/replica replication setup — add `mysql-router` or `Vitess` |
| **Ingress + TLS (cert-manager)** | Replace NodePort with proper HTTPS Ingress |
| **Network Policies** | Restrict WordPress pods to only talk to MySQL, not arbitrary services |
| **PodDisruptionBudget** | Ensure at least 1 MySQL pod stays up during node maintenance |
| **Backup CronJob** | Scheduled `mysqldump` to object storage (S3/GCS) |
| **Resource quotas per namespace** | Prevent any single app from starving the cluster |
| **Monitoring (Prometheus + Grafana)** | CPU/memory/request metrics dashboards |
| **Image pinning** | Replace `wordpress:latest` and `mysql:8.0` with specific digest-pinned versions |
| **Init containers** | Wait for MySQL to be ready before WordPress starts, instead of relying on probe retries |
| **External Secrets Operator** | Pull secrets from Vault or AWS Secrets Manager instead of raw K8s Secrets |

---

## Final kubectl Output (Healthy State)

```bash
kubectl get all -n capstone

NAME                                     READY   STATUS    RESTARTS       AGE
pod/mysql-0                              1/1     Running   1 (121m ago)   22h
pod/mysql-1                              1/1     Running   1 (121m ago)   22h
pod/mysql-2                              1/1     Running   1 (121m ago)   22h
pod/wp-deployment-556f6b7d75-jzwwl       1/1     Running   0              12m
pod/wp-deployment-556f6b7d75-xktxb       1/1     Running   0              12m

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)        AGE
service/my-service   ClusterIP   None         <none>        3306/TCP       22h
service/wp-service   NodePort    10.x.x.x     <none>        80:30008/TCP   5m

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/wp-deployment   2/2     2            2           37m

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/wp-deployment-556f6b7d75   2         2         2       12m

NAME                     READY   AGE
statefulset.apps/mysql   3/3     22h

NAME                                      REFERENCE                  TARGETS       MINPODS   MAXPODS   REPLICAS
horizontalpodautoscaler.autoscaling/hpa   Deployment/wp-deployment   cpu: 13%/50%  2         10        2
```

---

*Day 60 of 90 — WordPress + MySQL on Kubernetes ✅*  
*Uttam Tripathi — DevOps Engineer — Kanpur, India*
