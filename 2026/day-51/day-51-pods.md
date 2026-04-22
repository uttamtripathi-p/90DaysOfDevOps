# The four required fields of a Kubernetes manifest and what each does?
## apiVersion — which version of the Kubernetes API to use (e.g. apps/v1, v1)
## kind — the type of resource to create (e.g. Deployment, Service, Pod)
## metadata — identifying info about the object, at minimum a name
## spec — the desired state of the object; what you want Kubernetes to create/maintain

## nginx pod:
```yml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx
```

## busybox pod:
```yml
apiVersion: v1
kind: Pod
metadata:
  name: busybox-pod
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
```

## third pod (alpine):

```yml
apiVersion: v1
kind: Pod
metadata:
  name: third-pod
spec:
  containers:
  - name: alpine
    image: alpine
    command: ["sleep", "3600"]
```

## Difference between imperative (kubectl run) and declarative (kubectl apply -f)
### Imperative (kubectl run) — you tell Kubernetes what to do directly via a command, quick but not reproducible. Declarative (kubectl apply -f) — you define the desired state in a YAML file and Kubernetes figures out how to get there, repeatable and version-controllable.

## What happens when you delete a standalone Pod?
### It's gone permanently. Unlike a Pod managed by a Deployment or ReplicaSet, there's no controller watching it — so Kubernetes does not reschedule or recreate it.



