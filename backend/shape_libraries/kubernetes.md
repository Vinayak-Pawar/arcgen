# Kubernetes Shape Library

Kubernetes icon library for draw.io diagrams. Complete collection of K8s resource icons.

## Usage

In your mxCell style attribute, use:
```
style="shape=mxgraph.kubernetes.RESOURCE_NAME;fillColor=#326CE5;"
```

## Core Kubernetes Resources

### Workloads
- **Pod**: `shape=mxgraph.kubernetes.pod`
- **Deployment**: `shape=mxgraph.kubernetes.deploy`
- **StatefulSet**: `shape=mxgraph.kubernetes.sts`
- **DaemonSet**: `shape=mxgraph.kubernetes.ds`
- **Job**: `shape=mxgraph.kubernetes.job`
- **CronJob**: `shape=mxgraph.kubernetes.cronjob`
- **ReplicaSet**: `shape=mxgraph.kubernetes.rs`

### Services & Networking
- **Service**: `shape=mxgraph.kubernetes.svc`
- **Ingress**: `shape=mxgraph.kubernetes.ing`
- **NetworkPolicy**: `shape=mxgraph.kubernetes.netpol`
- **Endpoints**: `shape=mxgraph.kubernetes.ep`

### Config & Storage
- **ConfigMap**: `shape=mxgraph.kubernetes.cm`
- **Secret**: `shape=mxgraph.kubernetes.secret`
- **PersistentVolume**: `shape=mxgraph.kubernetes.pv`
- **PersistentVolumeClaim**: `shape=mxgraph.kubernetes.pvc`
- **StorageClass**: `shape=mxgraph.kubernetes.sc`

### Cluster Resources
- **Node**: `shape=mxgraph.kubernetes.node`
- **Namespace**: `shape=mxgraph.kubernetes.ns`
- **ServiceAccount**: `shape=mxgraph.kubernetes.sa`
- **Role**: `shape=mxgraph.kubernetes.role`
- **RoleBinding**: `shape=mxgraph.kubernetes.rb`
- **ClusterRole**: `shape=mxgraph.kubernetes.c_role`
- **ClusterRoleBinding**: `shape=mxgraph.kubernetes.crb`

### Advanced Resources
- **HorizontalPodAutoscaler**: `shape=mxgraph.kubernetes.hpa`
- **ResourceQuota**: `shape=mxgraph.kubernetes.quota`
- **LimitRange**: `shape=mxgraph.kubernetes.limits`

### Custom Resources
- **CustomResourceDefinition**: `shape=mxgraph.kubernetes.crd`
- **APIService**: `shape=mxgraph.kubernetes.api`

## Example Usage

```xml
<mxCell id="2" value="Frontend Pod" 
  style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="3" value="Service" 
  style="shape=mxgraph.kubernetes.svc;fillColor=#326CE5;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="4" value="Ingress" 
  style="shape=mxgraph.kubernetes.ing;fillColor=#326CE5;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

## Color Guidelines

Kubernetes uses the official K8s blue:
- **Primary**: #326CE5 (Kubernetes blue)
- **Stroke**: #ffffff (white) or #326CE5
- **Alternative Colors by Resource Type**:
  - **Workloads**: #326CE5 (blue)
  - **Services**: #00D3A9 (green)
  - **Config**: #FDB45C (yellow)
  - **Storage**: #9F4FC4 (purple)
  - **Security**: #FF5A5F (red)

## Resource Categories

### Workload Resources
- Pod (smallest deployable unit)
- Deployment (stateless apps)
- StatefulSet (stateful apps)
- DaemonSet (one pod per node)
- Job (run to completion)
- CronJob (scheduled jobs)

### Service Discovery
- Service (expose pods)
- Ingress (HTTP routing)
- NetworkPolicy (network rules)

### Configuration
- ConfigMap (non-sensitive config)
- Secret (sensitive data)

### Storage
- PersistentVolume (storage resource)
- PersistentVolumeClaim (storage request)
- StorageClass (dynamic provisioning)

### Cluster Management
- Node (worker machine)
- Namespace (virtual cluster)
- ServiceAccount (pod identity)
- RBAC (permissions)

## Tips

1. Always call `get_shape_library("kubernetes")` before generating K8s diagrams
2. Use exact shape names as listed above
3. K8s icons work best at 50x50 pixels
4. Use color coding for different resource types
5. Use containers to represent namespaces
6. Show pod-to-service connections clearly

## Icon Sizing

- **Standard Icons**: 50x50 pixels
- **Nodes**: 80x80 pixels
- **Namespaces** (containers): Variable
- **Spacing**: 80-100px between icons

## Common Patterns

### Simple Web Application
```
[Ingress] → [Service] → [Deployment: 3 Pods]
                              ↓
                        [PVC] → [PV]
```

### Microservices
```
[Ingress]
  ├─ [Service A] → [Deployment A]
  ├─ [Service B] → [Deployment B]
  └─ [Service C] → [StatefulSet C]
                         ↓
                    [PVC/PV]
```

### Batch Processing
```
[CronJob] → [Job] → [Pod]
                      ↓
                 [ConfigMap]
```

## Diagram Organization

### By Namespace
```
┌─ Namespace: production ──────┐
│ [Service] → [Deployment]     │
│       ↓                       │
│   [ConfigMap] [Secret]        │
└───────────────────────────────┘
```

### By Layer
```
┌─ Ingress Layer ───────┐
│  [Ingress]            │
└───────────────────────┘
         ↓
┌─ Service Layer ───────┐
│  [Service A] [Svc B]  │
└───────────────────────┘
         ↓
┌─ Application Layer ───┐
│  [Deploy A] [Deploy B]│
└───────────────────────┘
         ↓
┌─ Data Layer ──────────┐
│  [StatefulSet] [PVC]  │
└───────────────────────┘
```

## Example: Complete Application

```xml
<!-- Namespace Container -->
<mxCell id="ns" value="production" 
  style="rounded=1;dashed=1;fillColor=#E8F5E8;" 
  vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="700" height="400" as="geometry"/>
</mxCell>

<!-- Ingress -->
<mxCell id="2" value="web-ingress" 
  style="shape=mxgraph.kubernetes.ing;fillColor=#326CE5;" 
  vertex="1" parent="ns">
  <mxGeometry x="300" y="20" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Service -->
<mxCell id="3" value="web-svc" 
  style="shape=mxgraph.kubernetes.svc;fillColor=#00D3A9;" 
  vertex="1" parent="ns">
  <mxGeometry x="300" y="120" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Deployment -->
<mxCell id="4" value="web-deploy" 
  style="shape=mxgraph.kubernetes.deploy;fillColor=#326CE5;" 
  vertex="1" parent="ns">
  <mxGeometry x="300" y="220" width="50" height="50" as="geometry"/>
</mxCell>

<!-- ConfigMap -->
<mxCell id="5" value="app-config" 
  style="shape=mxgraph.kubernetes.cm;fillColor=#FDB45C;" 
  vertex="1" parent="ns">
  <mxGeometry x="450" y="220" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Secret -->
<mxCell id="6" value="db-secret" 
  style="shape=mxgraph.kubernetes.secret;fillColor=#FF5A5F;" 
  vertex="1" parent="ns">
  <mxGeometry x="550" y="220" width="50" height="50" as="geometry"/>
</mxCell>

<!-- PVC -->
<mxCell id="7" value="data-pvc" 
  style="shape=mxgraph.kubernetes.pvc;fillColor=#9F4FC4;" 
  vertex="1" parent="ns">
  <mxGeometry x="300" y="320" width="50" height="50" as="geometry"/>
</mxCell>
```

## Abbreviations

- **Pod**: po
- **Deployment**: deploy
- **Service**: svc
- **Ingress**: ing
- **ConfigMap**: cm
- **StatefulSet**: sts
- **DaemonSet**: ds
- **PersistentVolume**: pv
- **PersistentVolumeClaim**: pvc
- **Namespace**: ns
- **ServiceAccount**: sa
- **HorizontalPodAutoscaler**: hpa

## Best Practices

1. **Use Namespaces**: Group resources by namespace using containers
2. **Color Code**: Different colors for different resource types
3. **Label Clearly**: Include resource type and name
4. **Show Flow**: Use arrows to show traffic flow
5. **Indicate Replicas**: Use labels like "×3" for multiple pods
6. **Storage**: Clearly show PV/PVC relationships
7. **RBAC**: Include ServiceAccount, Role, RoleBinding for security

## Advanced: Helm Charts

For Helm chart diagrams, use containers to group related resources:

```
┌─ Chart: nginx-ingress ────────┐
│ [Deployment]                  │
│ [Service]                     │
│ [ConfigMap]                   │
│ [ServiceAccount]              │
└───────────────────────────────┘
```

## Multi-Cluster Setup

```
┌─ Cluster: Production ─────┐  ┌─ Cluster: Staging ────┐
│ [Deployment] [Service]    │  │ [Deployment] [Svc]    │
└───────────────────────────┘  └───────────────────────┘
            ↕                              ↕
    ┌─ Shared Services ─────────────────┐
    │  [External DNS] [Cert Manager]   │
    └──────────────────────────────────┘
```
