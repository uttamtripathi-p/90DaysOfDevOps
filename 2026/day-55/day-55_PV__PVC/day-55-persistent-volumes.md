# Kubernetes Persistent Storage

---

## Why Containers Need Persistent Storage

- Containers are ephemeral — when a container restarts or dies, all data inside is lost
- Default container storage is tied to the container lifecycle
- Apps like databases, file uploads, logs need data to survive restarts
- Multiple containers may need to share the same data
- Without persistent storage, stateful apps cannot run reliably in Kubernetes

---

## What PVs and PVCs Are and How They Relate

### PersistentVolume (PV)

- A piece of actual storage provisioned in the cluster
- Created by the cluster admin (or dynamically by a provisioner)
- Lives independently of any Pod
- Has its own lifecycle — not tied to a Pod or namespace

### PersistentVolumeClaim (PVC)

- A request for storage made by a user/app
- You specify how much storage you need and what access mode
- Kubernetes finds a matching PV and binds them together
- Pod uses the PVC, not the PV directly

### How They Relate

- PVC is like a ticket — PV is the actual storage
- Kubernetes matches a PVC to a suitable PV based on size, access mode, and StorageClass
- Once bound, that PV is exclusively reserved for that PVC

---

## Static vs Dynamic Provisioning

### Static Provisioning

- Admin manually creates PVs in advance
- PVCs then bind to one of the available pre-created PVs
- Admin must know storage needs ahead of time
- If no matching PV exists, PVC stays Pending

### Dynamic Provisioning

- No need to pre-create PVs manually
- PVC references a StorageClass
- Kubernetes automatically provisions a PV when the PVC is created
- Needs a provisioner running in the cluster (e.g. local-path, AWS EBS, GCE PD)
- More flexible and scalable than static

---

## Access Modes

- `ReadWriteOnce (RWO)` — mounted as read-write by a single node only
- `ReadOnlyMany (ROX)` — mounted as read-only by many nodes simultaneously
- `ReadWriteMany (RWX)` — mounted as read-write by many nodes simultaneously
- Not all storage backends support all access modes
- For example, AWS EBS only supports RWO, NFS supports RWX

---

## Reclaim Policies

- `Retain` — PV is kept after PVC is deleted, data is preserved, admin must manually clean up
- `Delete` — PV and the underlying storage are automatically deleted when PVC is deleted
- `Recycle` — deprecated, used to do a basic scrub and make PV available again
- Default policy depends on the StorageClass being used
- Use `Retain` when data must not be lost accidentally
- Use `Delete` for temporary or dev workloads where cleanup should be automatic
