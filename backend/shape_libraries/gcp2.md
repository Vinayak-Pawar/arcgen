# GCP 2.0 Shape Library

Google Cloud Platform 2.0 icon library for draw.io diagrams. Complete collection of GCP service icons.

## Usage

In your mxCell style attribute, use:
```
style="shape=mxgraph.gcp2.SERVICE_NAME;fillColor=#4285F4;"
```

## Common GCP Services

### Compute
- **Compute Engine**: `shape=mxgraph.gcp2.compute_engine`
- **App Engine**: `shape=mxgraph.gcp2.app_engine`
- **Cloud Functions**: `shape=mxgraph.gcp2.cloud_functions`
- **Cloud Run**: `shape=mxgraph.gcp2.cloud_run`
- **GKE (Kubernetes Engine)**: `shape=mxgraph.gcp2.kubernetes_engine`

### Storage
- **Cloud Storage**: `shape=mxgraph.gcp2.cloud_storage`
- **Persistent Disk**: `shape=mxgraph.gcp2.persistent_disk`
- **Filestore**: `shape=mxgraph.gcp2.filestore`

### Database
- **Cloud SQL**: `shape=mxgraph.gcp2.cloud_sql`
- **Cloud Spanner**: `shape=mxgraph.gcp2.cloud_spanner`
- **Firestore**: `shape=mxgraph.gcp2.firestore`
- **Bigtable**: `shape=mxgraph.gcp2.bigtable`
- **Memorystore**: `shape=mxgraph.gcp2.memorystore`

### Networking
- **VPC Network**: `shape=mxgraph.gcp2.virtual_private_cloud`
- **Cloud Load Balancing**: `shape=mxgraph.gcp2.cloud_load_balancing`
- **Cloud CDN**: `shape=mxgraph.gcp2.cloud_cdn`
- **Cloud DNS**: `shape=mxgraph.gcp2.cloud_dns`
- **Cloud VPN**: `shape=mxgraph.gcp2.cloud_vpn`
- **Cloud Interconnect**: `shape=mxgraph.gcp2.cloud_interconnect`

### Big Data & Analytics
- **BigQuery**: `shape=mxgraph.gcp2.bigquery`
- **Dataflow**: `shape=mxgraph.gcp2.dataflow`
- **Dataproc**: `shape=mxgraph.gcp2.dataproc`
- **Pub/Sub**: `shape=mxgraph.gcp2.cloud_pubsub`
- **Data Fusion**: `shape=mxgraph.gcp2.cloud_data_fusion`

### AI & Machine Learning
- **Vertex AI**: `shape=mxgraph.gcp2.vertex_ai`
- **AI Platform**: `shape=mxgraph.gcp2.ai_platform`
- **AutoML**: `shape=mxgraph.gcp2.automl`
- **Vision AI**: `shape=mxgraph.gcp2.vision_ai`
- **Natural Language AI**: `shape=mxgraph.gcp2.natural_language_ai`

### Security & Identity
- **Cloud IAM**: `shape=mxgraph.gcp2.cloud_iam`
- **Cloud KMS**: `shape=mxgraph.gcp2.cloud_key_management_service`
- **Security Command Center**: `shape=mxgraph.gcp2.security_command_center`
- **Identity Platform**: `shape=mxgraph.gcp2.identity_platform`

### Monitoring & Management
- **Cloud Monitoring**: `shape=mxgraph.gcp2.cloud_monitoring`
- **Cloud Logging**: `shape=mxgraph.gcp2.cloud_logging`
- **Cloud Trace**: `shape=mxgraph.gcp2.cloud_trace`
- **Cloud Profiler**: `shape=mxgraph.gcp2.cloud_profiler`

### Developer Tools
- **Cloud Build**: `shape=mxgraph.gcp2.cloud_build`
- **Cloud Source Repositories**: `shape=mxgraph.gcp2.cloud_source_repositories`
- **Container Registry**: `shape=mxgraph.gcp2.container_registry`
- **Artifact Registry**: `shape=mxgraph.gcp2.artifact_registry`

## Example Usage

```xml
<mxCell id="2" value="Compute Engine" 
  style="shape=mxgraph.gcp2.compute_engine;fillColor=#4285F4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="75" height="75" as="geometry"/>
</mxCell>

<mxCell id="3" value="Cloud SQL" 
  style="shape=mxgraph.gcp2.cloud_sql;fillColor=#4285F4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="75" height="75" as="geometry"/>
</mxCell>

<mxCell id="4" value="Cloud Storage" 
  style="shape=mxgraph.gcp2.cloud_storage;fillColor=#4285F4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="75" height="75" as="geometry"/>
</mxCell>
```

## Color Guidelines

Google Cloud uses a multi-color palette:
- **Primary Blue**: #4285F4 (Google blue)
- **Red**: #EA4335
- **Yellow**: #FBBC04
- **Green**: #34A853

### Recommended Colors by Category
- **Compute**: Blue (#4285F4)
- **Storage**: Red (#EA4335)
- **Databases**: Yellow (#FBBC04)
- **Networking**: Green (#34A853)
- **AI/ML**: Purple (#9334E6)
- **Analytics**: Orange (#FF6D01)

## Service Categories

### Compute
- Compute Engine (VMs)
- App Engine (PaaS)
- Cloud Functions (Serverless)
- Cloud Run (Containers)
- GKE (Kubernetes)

### Storage & Databases
- Cloud Storage (Object)
- Cloud SQL (Relational)
- Firestore (NoSQL)
- Bigtable (Wide-column)
- Spanner (Global SQL)

### Networking
- VPC Network
- Cloud Load Balancing
- Cloud CDN
- Cloud DNS
- Cloud VPN

### Big Data
- BigQuery (Data Warehouse)
- Dataflow (Stream/Batch)
- Pub/Sub (Messaging)
- Dataproc (Hadoop/Spark)

### AI & ML
- Vertex AI (ML Platform)
- AutoML
- Vision AI
- Natural Language AI

## Tips

1. Always call `get_shape_library("gcp2")` before generating GCP diagrams
2. Use exact shape names as listed above
3. GCP icons work best at 75x75 pixels (slightly larger than AWS/Azure)
4. Use Google's color palette for authenticity
5. White stroke provides good contrast

## Icon Sizing

- **Standard Icons**: 75x75 pixels
- **Large Services**: 90x90 pixels
- **Small Indicators**: 40x40 pixels
- **Spacing**: 100-120px between icons

## Common Patterns

### Web Application
```
[Cloud Run] → [Cloud SQL]
     ↓
[Cloud Storage]
```

### Kubernetes Microservices
```
[GKE]
  ├─ [Cloud SQL]
  ├─ [Memorystore]
  └─ [Pub/Sub]
```

### Data Pipeline
```
[Pub/Sub] → [Dataflow] → [BigQuery]
     ↓
[Cloud Storage]
```

### Machine Learning
```
[Cloud Storage] → [Vertex AI] → [Cloud Functions]
                        ↓
                   [BigQuery]
```

## Best Practices

1. **Color Coding**: Use different colors for different service types
2. **Grouping**: Use VPC containers to group related resources
3. **Labels**: Always add descriptive labels
4. **Regions**: Indicate multi-region setups with grouped containers
5. **Data Flow**: Use arrows to show data movement

## GCP-Specific Features

### Zones & Regions
- Use containers to represent zones
- Use larger containers for regions
- Label clearly (e.g., "us-central1-a")

### VPC Networks
- Use VPC shape as container
- Place compute resources inside
- Show subnets with nested containers

### Load Balancing
- Place load balancer icon at entry point
- Show distribution to backend services
- Indicate health checks

## Example: Full Stack Application

```xml
<!-- VPC -->
<mxCell id="vpc" value="VPC Network" style="container;" .../>

<!-- Frontend -->
<mxCell id="2" value="Cloud Run" 
  style="shape=mxgraph.gcp2.cloud_run;fillColor=#4285F4;" 
  vertex="1" parent="vpc">
  <mxGeometry x="100" y="100" width="75" height="75"/>
</mxCell>

<!-- Backend -->
<mxCell id="3" value="GKE" 
  style="shape=mxgraph.gcp2.kubernetes_engine;fillColor=#4285F4;" 
  vertex="1" parent="vpc">
  <mxGeometry x="300" y="100" width="75" height="75"/>
</mxCell>

<!-- Database -->
<mxCell id="4" value="Cloud SQL" 
  style="shape=mxgraph.gcp2.cloud_sql;fillColor=#FBBC04;" 
  vertex="1" parent="vpc">
  <mxGeometry x="500" y="100" width="75" height="75"/>
</mxCell>

<!-- Cache -->
<mxCell id="5" value="Memorystore" 
  style="shape=mxgraph.gcp2.memorystore;fillColor=#EA4335;" 
  vertex="1" parent="vpc">
  <mxGeometry x="500" y="200" width="75" height="75"/>
</mxCell>
```
