# Azure 2.0 Shape Library

Microsoft Azure 2.0 icon library for draw.io diagrams. Comprehensive collection of Azure service icons.

## Usage

In your mxCell style attribute, use:
```
style="shape=mxgraph.azure.SERVICE_NAME;fillColor=#0078D4;"
```

## Common Azure Services

### Compute
- **Virtual Machines**: `shape=mxgraph.azure.virtual_machine`
- **App Services**: `shape=mxgraph.azure.app_services`
- **Azure Functions**: `shape=mxgraph.azure.function_apps`
- **Container Instances**: `shape=mxgraph.azure.container_instances`
- **Kubernetes Service (AKS)**: `shape=mxgraph.azure.kubernetes_services`
- **Batch**: `shape=mxgraph.azure.batch_accounts`

### Storage
- **Storage Accounts**: `shape=mxgraph.azure.storage_accounts`
- **Blob Storage**: `shape=mxgraph.azure.blob_storage`
- **File Storage**: `shape=mxgraph.azure.file_storage`
- **Queue Storage**: `shape=mxgraph.azure.queue_storage`
- **Table Storage**: `shape=mxgraph.azure.table_storage`
- **Disk Storage**: `shape=mxgraph.azure.disk_storage`

### Database
- **SQL Database**: `shape=mxgraph.azure.sql_database`
- **Cosmos DB**: `shape=mxgraph.azure.cosmos_db`
- **Database for MySQL**: `shape=mxgraph.azure.database_mysql`
- **Database for PostgreSQL**: `shape=mxgraph.azure.database_postgres`
- **SQL Data Warehouse**: `shape=mxgraph.azure.sql_data_warehouse`
- **Redis Cache**: `shape=mxgraph.azure.cache_redis`

### Networking
- **Virtual Network**: `shape=mxgraph.azure.virtual_network`
- **Load Balancer**: `shape=mxgraph.azure.load_balancer`
- **Application Gateway**: `shape=mxgraph.azure.application_gateway`
- **VPN Gateway**: `shape=mxgraph.azure.vpn_gateway`
- **Traffic Manager**: `shape=mxgraph.azure.traffic_manager`
- **DNS**: `shape=mxgraph.azure.dns`
- **CDN**: `shape=mxgraph.azure.cdn_profiles`

### Security & Identity
- **Azure AD**: `shape=mxgraph.azure.azure_active_directory`
- **Key Vault**: `shape=mxgraph.azure.key_vaults`
- **Security Center**: `shape=mxgraph.azure.security_center`
- **Azure AD B2C**: `shape=mxgraph.azure.azure_ad_b2c`

### Messaging & Integration
- **Service Bus**: `shape=mxgraph.azure.service_bus`
- **Event Hubs**: `shape=mxgraph.azure.event_hubs`
- **Event Grid**: `shape=mxgraph.azure.event_grid`
- **Logic Apps**: `shape=mxgraph.azure.logic_apps`
- **API Management**: `shape=mxgraph.azure.api_management`

### Analytics
- **HDInsight**: `shape=mxgraph.azure.hdinsight`
- **Stream Analytics**: `shape=mxgraph.azure.stream_analytics`
- **Data Factory**: `shape=mxgraph.azure.data_factory`
- **Databricks**: `shape=mxgraph.azure.databricks`
- **Synapse Analytics**: `shape=mxgraph.azure.synapse_analytics`

### AI & Machine Learning
- **Cognitive Services**: `shape=mxgraph.azure.cognitive_services`
- **Machine Learning**: `shape=mxgraph.azure.machine_learning`
- **Bot Service**: `shape=mxgraph.azure.bot_services`

### Monitoring & Management
- **Monitor**: `shape=mxgraph.azure.monitor`
- **Log Analytics**: `shape=mxgraph.azure.log_analytics`
- **Application Insights**: `shape=mxgraph.azure.application_insights`
- **Automation**: `shape=mxgraph.azure.automation_accounts`

### DevOps
- **Azure DevOps**: `shape=mxgraph.azure.devops`
- **DevTest Labs**: `shape=mxgraph.azure.devtest_labs`
- **Container Registry**: `shape=mxgraph.azure.container_registries`

## Example Usage

```xml
<mxCell id="2" value="Azure VM" 
  style="shape=mxgraph.azure.virtual_machine;fillColor=#0078D4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="3" value="SQL Database" 
  style="shape=mxgraph.azure.sql_database;fillColor=#0078D4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="4" value="Blob Storage" 
  style="shape=mxgraph.azure.blob_storage;fillColor=#0078D4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

## Color Guidelines

Azure uses the Microsoft blue color scheme:
- **Primary Blue**: #0078D4 (Microsoft Azure blue)
- **Stroke**: #ffffff (white) or #0078D4
- **Secondary Colors**:
  - Light Blue: #50E6FF
  - Dark Blue: #005A9E
  - Gray: #737373

## Service Categories

### Compute & Containers
- Virtual Machines
- App Services
- Functions
- AKS (Kubernetes)
- Container Instances
- Batch

### Storage & Databases
- Storage Accounts
- Cosmos DB
- SQL Database
- MySQL/PostgreSQL
- Redis Cache

### Networking
- Virtual Network
- Load Balancer
- Application Gateway
- VPN Gateway
- Traffic Manager
- CDN

### Security
- Azure AD
- Key Vault
- Security Center

### Integration
- Service Bus
- Event Hubs
- Event Grid
- Logic Apps
- API Management

## Tips

1. Always call `get_shape_library("azure2")` before generating Azure diagrams
2. Use exact shape names as listed above
3. Azure icons work best at 50x50 pixels
4. Use #0078D4 for consistent Azure branding
5. White stroke (#ffffff) provides good contrast
6. Group related services using containers

## Icon Sizing

- **Standard Icons**: 50x50 pixels
- **Large Services**: 60x60 pixels  
- **Small Indicators**: 30x30 pixels
- **Spacing**: 80-100px between icons

## Common Patterns

### Web Application
```
[App Service] → [SQL Database]
     ↓
[Blob Storage]
```

### Microservices
```
[AKS Cluster]
  ├─ [Service Bus]
  ├─ [Cosmos DB]
  └─ [Redis Cache]
```

### Data Pipeline
```
[Event Hubs] → [Stream Analytics] → [SQL Data Warehouse]
```
