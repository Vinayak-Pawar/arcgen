# IBM Cloud Shape Library

IBM Cloud service icons for cloud architecture diagrams.

## Usage

```
style="shape=mxgraph.ibm.SERVICE_NAME;fillColor=#0F62FE;"
```

## IBM Cloud Services

### Compute
- **Virtual Servers**: `shape=mxgraph.ibm.virtual_server`
- **Bare Metal Servers**: `shape=mxgraph.ibm.bare_metal`
- **Cloud Functions**: `shape=mxgraph.ibm.cloud_functions`
- **Code Engine**: `shape=mxgraph.ibm.code_engine`
- **Red Hat OpenShift**: `shape=mxgraph.ibm.openshift`
- **Kubernetes Service (IKS)**: `shape=mxgraph.ibm.kubernetes`

### Storage
- **Object Storage**: `shape=mxgraph.ibm.object_storage`
- **Block Storage**: `shape=mxgraph.ibm.block_storage`
- **File Storage**: `shape=mxgraph.ibm.file_storage`

### Database
- **Db2**: `shape=mxgraph.ibm.db2`
- **Cloudant**: `shape=mxgraph.ibm.cloudant`
- **Databases for PostgreSQL**: `shape=mxgraph.ibm.postgresql`
- **Databases for MongoDB**: `shape=mxgraph.ibm.mongodb`
- **Databases for Redis**: `shape=mxgraph.ibm.redis`
- **Databases for Elasticsearch**: `shape=mxgraph.ibm.elasticsearch`

### Networking
- **Virtual Private Cloud**: `shape=mxgraph.ibm.vpc`
- **Load Balancer**: `shape=mxgraph.ibm.load_balancer`
- **VPN Gateway**: `shape=mxgraph.ibm.vpn`
- **Direct Link**: `shape=mxgraph.ibm.direct_link`
- **Cloud Internet Services**: `shape=mxgraph.ibm.internet_services`

### AI & Data
- **Watson Studio**: `shape=mxgraph.ibm.watson_studio`
- **Watson Assistant**: `shape=mxgraph.ibm.watson_assistant`
- **Watson Discovery**: `shape=mxgraph.ibm.watson_discovery`
- **Watson Knowledge Catalog**: `shape=mxgraph.ibm.knowledge_catalog`
- **DataStage**: `shape=mxgraph.ibm.datastage`

### Integration
- **App Connect**: `shape=mxgraph.ibm.app_connect`
- **Event Streams**: `shape=mxgraph.ibm.event_streams`
- **MQ**: `shape=mxgraph.ibm.mq`
- **API Connect**: `shape=mxgraph.ibm.api_connect`

### Security
- **Key Protect**: `shape=mxgraph.ibm.key_protect`
- **Secrets Manager**: `shape=mxgraph.ibm.secrets_manager`
- **Certificate Manager**: `shape=mxgraph.ibm.certificate_manager`
- **Security Advisor**: `shape=mxgraph.ibm.security_advisor`

### DevOps
- **Continuous Delivery**: `shape=mxgraph.ibm.continuous_delivery`
- **Toolchain**: `shape=mxgraph.ibm.toolchain`
- **Schematics**: `shape=mxgraph.ibm.schematics`

### Monitoring
- **LogDNA**: `shape=mxgraph.ibm.logdna`
- **SysDig**: `shape=mxgraph.ibm.sysdig`
- **Activity Tracker**: `shape=mxgraph.ibm.activity_tracker`

## Color Guidelines

- **Primary IBM Blue**: #0F62FE
- **Secondary**: #08BDBA (cyan)  
- **Tertiary**: #FF5050 (red)
- **Neutral**: #525252 (gray)

## Example

```xml
<mxCell id="2" value="IKS Cluster" 
  style="shape=mxgraph.ibm.kubernetes;fillColor=#0F62FE;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry"/>
</mxCell>

<mxCell id="3" value="Db2" 
  style="shape=mxgraph.ibm.db2;fillColor=#0F62FE;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="80" height="80" as="geometry"/>
</mxCell>
```

## Best Practices

1. Use IBM blue (#0F62FE) for primary services
2. 80x80 pixels for standard icons
3. Group services by VPC/Resource Group
4. Show multi-zone architecture
5. Indicate public vs private endpoints
