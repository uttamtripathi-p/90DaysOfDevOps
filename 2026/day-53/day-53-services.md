# What problem Services solve and how they relate to Pods and Deployments
## Pods are ephemeral and get new IP addresses when they restart; Services provide a single, permanent IP and DNS name to act as a stable entry point. They decouple the requester from the specific backend Pods, ensuring traffic always finds a healthy instance.


# Your three Service manifests with an explanation of each type
```yml
# loadbalancer-service.yml
kind: Service
apiVersion: v1
metadata:
  name: web-app-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
```

```yml
# cluster-service.yml
kind: Service
apiVersion: v1
metadata:
  name: web-app-clusterip
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
```

```yml
# nodeport-service.yml
kind: Service
apiVersion: v1
metadata:
  name: web-app-nodeport
spec:
  type: NodePort
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```



# The difference between ClusterIP, NodePort, and LoadBalancer
## ClusterIP is for internal communication,
## NodePort is a basic way to expose services to the outside world via the host IP, and 
## LoadBalancer is the enterprise-standard for external access using a dedicated cloud IP. Think of them as levels of visibility: Internal $\rightarrow$ Host Network $\rightarrow$ Public Internet.

# How Kubernetes DNS works for service discovery
## Kubernetes runs a built-in DNS service (CoreDNS) that watches for new Services and creates a record for each (e.g., my-svc.my-namespace.svc.cluster.local). Pods can simply "call" another service by its name instead of tracking volatile IP addresses.

# What Endpoints are and how to inspect them
## Endpoints are the list of actual Pod IP addresses that match a Service's selector and are currently "Ready" to receive traffic. You can inspect them using kubectl get endpoints <service-name> or see them detailed under the "Endpoints" section of kubectl describe svc <service-name>.

