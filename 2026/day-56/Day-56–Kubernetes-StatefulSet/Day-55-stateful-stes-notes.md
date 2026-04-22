# Kubernetes StatefulSets — Complete Notes

---

## 1. What is a StatefulSet?

A **StatefulSet** is a Kubernetes workload API object used to manage **stateful applications**. Unlike Deployments, StatefulSets give each pod a **stable, unique identity** that persists across rescheduling.

Each pod in a StatefulSet gets:
- A **stable hostname**: `nginx-stats-0`, `nginx-stats-1`, `nginx-stats-2`
- A **stable DNS name**: `<pod-name>.<service-name>.<namespace>.svc.cluster.local`
- Its **own PersistentVolumeClaim (PVC)** — data is NOT shared between pods

---

## 2. StatefulSet vs Deployment

| Feature | StatefulSet | Deployment |
|---|---|---|
| Pod identity | Stable, unique (`pod-0`, `pod-1`) | Random (`pod-abc123`) |
| Pod DNS name | Stable per pod | Not stable |
| Storage | Each pod gets its own PVC | Shared or no persistent storage |
| Scaling order | Ordered (0 → 1 → 2) | Random/parallel |
| Use case | Databases, queues, stateful apps | Stateless apps (web servers, APIs) |
| Pod restart | Same name and storage retained | New random name |

### When to use StatefulSet
- Databases (MySQL, PostgreSQL, MongoDB)
- Message queues (Kafka, RabbitMQ)
- Distributed systems (Elasticsearch, Zookeeper)
- Any app that needs **stable network identity** or **per-pod storage**

### When to use Deployment
- Stateless web servers
- REST APIs
- Frontend apps
- Any app where pods are interchangeable

---

## 3. StatefulSet YAML

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-stats
  namespace: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "my-service"      # Must match the headless service name
  replicas: 3
  minReadySeconds: 10
  template:
    metadata:
      labels:
        app: nginx
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Mi
```

---

## 4. Headless Service

A **Headless Service** has `clusterIP: None`. Instead of load balancing traffic to a virtual IP, it returns the **actual pod IPs** directly via DNS.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: nginx
spec:
  clusterIP: None       # ← This makes it headless
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
```

### Regular Service vs Headless Service

| | Regular Service | Headless Service |
|---|---|---|
| `clusterIP` | Virtual IP (e.g. `10.96.x.x`) | `None` |
| DNS resolution | Returns ClusterIP (load balanced) | Returns individual pod IPs |
| Use with | Deployments | StatefulSets |
| Pod addressable? | No | Yes (each pod has DNS) |

---

## 5. Stable DNS Names

Each StatefulSet pod gets a DNS entry in the format:

```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

For our setup:

```
nginx-stats-0.my-service.nginx.svc.cluster.local  →  10.244.1.x
nginx-stats-1.my-service.nginx.svc.cluster.local  →  10.244.1.9
nginx-stats-2.my-service.nginx.svc.cluster.local  →  10.244.1.11
```

This DNS name is **stable** — even if the pod is deleted and recreated, it gets the same DNS name and reconnects to its own storage.

---

## 6. volumeClaimTemplates

`volumeClaimTemplates` automatically creates a **separate PVC for each pod**. This is the key feature that enables per-pod storage isolation.

```yaml
volumeClaimTemplates:
- metadata:
    name: www
  spec:
    accessModes: [ "ReadWriteOnce" ]
    resources:
      requests:
        storage: 100Mi
```

This creates:

```
NAME                    STATUS   CAPACITY
www-nginx-stats-0       Bound    100Mi
www-nginx-stats-1       Bound    100Mi
www-nginx-stats-2       Bound    100Mi
```

Each pod mounts **only its own PVC**. Data written by `nginx-stats-0` is NOT visible to `nginx-stats-1`.

---

## 7. DNS Resolution — Lab Verification

### Step 1: Launch a busybox pod

```bash
kubectl run busybox --image=busybox:1.28 --rm -it --restart=Never -- /bin/sh
```

### Step 2: Run nslookup inside busybox

```bash
nslookup nginx-stats-0.my-service.nginx.svc.cluster.local
nslookup nginx-stats-1.my-service.nginx.svc.cluster.local
nslookup nginx-stats-2.my-service.nginx.svc.cluster.local
```

### Successful Output

```
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      nginx-stats-1.my-service.nginx.svc.cluster.local
Address 1: 10.244.1.9 nginx-stats-1.my-service.nginx.svc.cluster.local

Name:      nginx-stats-2.my-service.nginx.svc.cluster.local
Address 1: 10.244.1.11 nginx-stats-2.my-service.nginx.svc.cluster.local
```

> ✅ Each pod resolves to its own unique IP — DNS is working correctly.

---

## 8. Per-Pod Storage — Lab Verification

### Write unique data to each pod

```bash
kubectl exec nginx-stats-0 -n nginx -- sh -c "echo 'Data from web-0' > /usr/share/nginx/html/index.html"
kubectl exec nginx-stats-1 -n nginx -- sh -c "echo 'Data from web-1' > /usr/share/nginx/html/index.html"
kubectl exec nginx-stats-2 -n nginx -- sh -c "echo 'Data from web-2' > /usr/share/nginx/html/index.html"
```

### Verify each pod has isolated data

```bash
kubectl exec nginx-stats-0 -n nginx -- cat /usr/share/nginx/html/index.html  # → Data from web-0
kubectl exec nginx-stats-1 -n nginx -- cat /usr/share/nginx/html/index.html  # → Data from web-1
kubectl exec nginx-stats-2 -n nginx -- cat /usr/share/nginx/html/index.html  # → Data from web-2
```

Each pod returning **different data** confirms that `volumeClaimTemplates` created separate PVCs per pod.

---

## 9. Useful Commands

```bash
# Get all pods in nginx namespace
kubectl get pods -n nginx

# Watch pods in real time
kubectl get pods -n nginx -l app=nginx -w

# Check PVCs
kubectl get pvc -n nginx

# Check headless service
kubectl get svc -n nginx

# Describe service (verify selector)
kubectl describe svc my-service -n nginx

# Check DNS from inside cluster
kubectl run busybox --image=busybox:1.28 --rm -it --restart=Never -- /bin/sh
```

---

## 10. Key Takeaways

- StatefulSets give pods **stable identity** — name, DNS, and storage survive restarts
- **Headless Services** (`clusterIP: None`) enable per-pod DNS resolution
- **`volumeClaimTemplates`** auto-creates one PVC per pod — storage is isolated
- Pod DNS format: `<pod>.<service>.<namespace>.svc.cluster.local`
- Use StatefulSets for **databases and stateful apps**; use Deployments for **stateless apps**
