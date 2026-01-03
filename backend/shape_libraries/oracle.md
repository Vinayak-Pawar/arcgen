# Oracle Cloud (OCI) Shape Library

Oracle Cloud Infrastructure service icons.

## Usage

```
style="shape=mxgraph.oracle.SERVICE_NAME;fillColor=#FF0000;"
```

## OCI Services

### Compute
- **Compute Instances**: `shape=mxgraph.oracle.compute`
- **Container Engine (OKE)**: `shape=mxgraph.oracle.kubernetes`
- **Functions**: `shape=mxgraph.oracle.functions`
- **Container Instances**: `shape=mxgraph.oracle.container_instances`

### Storage
- **Object Storage**: `shape=mxgraph.oracle.object_storage`
- **Block Volume**: `shape=mxgraph.oracle.block_volume`
- **File Storage**: `shape=mxgraph.oracle.file_storage`
- **Archive Storage**: `shape=mxgraph.oracle.archive`

### Database
- **Autonomous Database**: `shape=mxgraph.oracle.autonomous_database`
- **Database Cloud Service**: `shape=mxgraph.oracle.database`
- **MySQL**: `shape=mxgraph.oracle.mysql`
- **NoSQL**: `shape=mxgraph.oracle.nosql`
- **Oracle RAC**: `shape=mxgraph.oracle.rac`

### Networking  
- **Virtual Cloud Network (VCN)**: `shape=mxgraph.oracle.vcn`
- **Load Balancer**: `shape=mxgraph.oracle.load_balancer`
- **VPN Connect**: `shape=mxgraph.oracle.vpn`
- **FastConnect**: `shape=mxgraph.oracle.fastconnect`
- **DNS**: `shape=mxgraph.oracle.dns`

### Integration
- **API Gateway**: `shape=mxgraph.oracle.api_gateway`
- **Service Mesh**: `shape=mxgraph.oracle.service_mesh`
- **Streaming**: `shape=mxgraph.oracle.streaming`
- **Integration Cloud**: `shape=mxgraph.oracle.integration`

### Analytics & AI
- **Data Science**: `shape=mxgraph.oracle.data_science`
- **Analytics Cloud**: `shape=mxgraph.oracle.analytics`
- **AI Services**: `shape=mxgraph.oracle.ai_services`
- **Data Flow**: `shape=mxgraph.oracle.data_flow`

### Security
- **Identity & Access Mgmt**: `shape=mxgraph.oracle.iam`
- **Key Management**: `shape=mxgraph.oracle.key_management`
- **Vault**: `shape=mxgraph.oracle.vault`
- **Web Application Firewall**: `shape=mxgraph.oracle.waf`

### Monitoring
- **Monitoring**: `shape=mxgraph.oracle.monitoring`
- **Logging**: `shape=mxgraph.oracle.logging`
- **Application Performance**: `shape=mxgraph.oracle.apm`

## Color Guidelines

- **Oracle Red**: #FF0000
- **Alternative**: #C74634 (darker red)
- **Black**: #000000 (for icons)

## Example

```xml
<mxCell id="2" value="OKE Cluster" 
  style="shape=mxgraph.oracle.kubernetes;fillColor=#FF0000;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="75" height="75" as="geometry"/>
</mxCell>

<mxCell id="3" value="Autonomous DB" 
  style="shape=mxgraph.oracle.autonomous_database;fillColor=#FF0000;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="75" height="75" as="geometry"/>
</mxCell>
```

## Best Practices

1. Use Oracle red (#FF0000)
2. 75x75 pixels for icons
3. Group by compartment
4. Show availability domain architecture
5. Indicate public vs private subnets
