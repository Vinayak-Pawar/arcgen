# Cisco 19 Shape Library

Cisco networking equipment icon library for draw.io diagrams. Comprehensive collection of Cisco device icons.

## Usage

In your mxCell style attribute, use:
```
style="shape=mxgraph.cisco19.DEVICE_NAME;fillColor=#1BA0D7;"
```

## Network Devices

### Routers
- **Router**: `shape=mxgraph.cisco19.router`
- **Branch Router**: `shape=mxgraph.cisco19.branch_router`
- **Edge Router**: `shape=mxgraph.cisco19.edge_router`
- **Core Router**: `shape=mxgraph.cisco19.core_router`
- **Wireless Router**: `shape=mxgraph.cisco19.wireless_router`

### Switches
- **Switch**: `shape=mxgraph.cisco19.switch`
- **Multilayer Switch**: `shape=mxgraph.cisco19.multilayer_switch`
- **Access Switch**: `shape=mxgraph.cisco19.access_switch`
- **Core Switch**: `shape=mxgraph.cisco19.core_switch`
- **PoE Switch**: `shape=mxgraph.cisco19.poe_switch`

### Wireless
- **Access Point**: `shape=mxgraph.cisco19.access_point`
- **Wireless Controller**: `shape=mxgraph.cisco19.wireless_controller`
- **Wireless Bridge**: `shape=mxgraph.cisco19.wireless_bridge`

### Security
- **Firewall**: `shape=mxgraph.cisco19.firewall`
- **ASA (Adaptive Security Appliance)**: `shape=mxgraph.cisco19.asa`
- **IPS/IDS**: `shape=mxgraph.cisco19.ips`
- **VPN Concentrator**: `shape=mxgraph.cisco19.vpn_concentrator`

### WAN & Cloud
- **Cloud**: `shape=mxgraph.cisco19.cloud`
- **WAN**: `shape=mxgraph.cisco19.wan`
- **Internet**: `shape=mxgraph.cisco19.internet`
- **MPLS**: `shape=mxgraph.cisco19.mpls`

### Endpoints
- **PC**: `shape=mxgraph.cisco19.pc`
- **Laptop**: `shape=mxgraph.cisco19.laptop`
- **Server**: `shape=mxgraph.cisco19.server`
- **Printer**: `shape=mxgraph.cisco19.printer`
- **IP Phone**: `shape=mxgraph.cisco19.ip_phone`
- **Mobile Device**: `shape=mxgraph.cisco19.mobile_device`

### Data Center
- **UCS Server**: `shape=mxgraph.cisco19.ucs`
- **Nexus Switch**: `shape=mxgraph.cisco19.nexus`
- **Storage**: `shape=mxgraph.cisco19.storage`
- **Load Balancer**: `shape=mxgraph.cisco19.load_balancer`

### Collaboration
- **UC Server**: `shape=mxgraph.cisco19.unified_communications`
- **Call Manager**: `shape=mxgraph.cisco19.call_manager`
- **Webex**: `shape=mxgraph.cisco19.webex`
- **TelePresence**: `shape=mxgraph.cisco19.telepresence`

## Example Usage

```xml
<mxCell id="2" value="Core Router" 
  style="shape=mxgraph.cisco19.router;fillColor=#1BA0D7;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry"/>
</mxCell>

<mxCell id="3" value="Firewall" 
  style="shape=mxgraph.cisco19.firewall;fillColor=#FF6B35;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="60" height="60" as="geometry"/>
</mxCell>

<mxCell id="4" value="Access Switch" 
  style="shape=mxgraph.cisco19.switch;fillColor=#1BA0D7;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="60" height="60" as="geometry"/>
</mxCell>
```

## Color Guidelines

Cisco uses a blue color scheme:
- **Primary Blue**: #1BA0D7 (Cisco blue)
- **Dark Blue**: #049FD9
- **Security Red**: #FF6B35
- **Cloud Gray**: #B0B0B0

### Color by Device Type
- **Routers**: #1BA0D7 (blue)
- **Switches**: #1BA0D7 (blue)
- **Security**: #FF6B35 (red/orange)
- **Wireless**: #00BCEB (light blue)
- **Cloud/WAN**: #B0B0B0 (gray)
- **Endpoints**: #4A4A4A (dark gray)

## Network Topologies

### Simple Office Network
```
[Internet] → [Router] → [Firewall] → [Core Switch]
                                           ↓
                            [Access Switch] [Access Switch]
                               ↓    ↓              ↓    ↓
                              [PC] [PC]          [PC] [PC]
```

### Campus Network
```
[Internet]
    ↓
[Edge Router]
    ↓
[Core Switch] ←→ [Core Switch]
    ↓                  ↓
[Distribution]    [Distribution]
    ↓                  ↓
[Access Switch]   [Access Switch]
```

### Data Center
```
[Firewall]
    ↓
[Core Switch]
    ↓
[Nexus Switch] ←→ [Nexus Switch]
    ↓                  ↓
[UCS Server]      [UCS Server]
    ↓                  ↓
[Storage]         [Storage]
```

## Example: Enterprise Network

```xml
<!-- Internet -->
<mxCell id="1" value="Internet" 
  style="shape=mxgraph.cisco19.internet;fillColor=#B0B0B0;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="20" width="60" height="60" as="geometry"/>
</mxCell>

<!-- Edge Router -->
<mxCell id="2" value="Edge Router" 
  style="shape=mxgraph.cisco19.edge_router;fillColor=#1BA0D7;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="120" width="60" height="60" as="geometry"/>
</mxCell>

<!-- Firewall -->
<mxCell id="3" value="Firewall" 
  style="shape=mxgraph.cisco19.firewall;fillColor=#FF6B35;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="220" width="60" height="60" as="geometry"/>
</mxCell>

<!-- Core Switch -->
<mxCell id="4" value="Core Switch" 
  style="shape=mxgraph.cisco19.core_switch;fillColor=#1BA0D7;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="320" width="60" height="60" as="geometry"/>
</mxCell>

<!-- Access Switches -->
<mxCell id="5" value="Access SW 1" 
  style="shape=mxgraph.cisco19.access_switch;fillColor=#1BA0D7;" 
  vertex="1" parent="1">
  <mxGeometry x="150" y="420" width="60" height="60" as="geometry"/>
</mxCell>

<mxCell id="6" value="Access SW 2" 
  style="shape=mxgraph.cisco19.access_switch;fillColor=#1BA0D7;" 
  vertex="1" parent="1">
  <mxGeometry x="450" y="420" width="60" height="60" as="geometry"/>
</mxCell>

<!-- Endpoints -->
<mxCell id="7" value="PC" 
  style="shape=mxgraph.cisco19.pc;fillColor=#4A4A4A;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="520" width="40" height="40" as="geometry"/>
</mxCell>

<mxCell id="8" value="Server" 
  style="shape=mxgraph.cisco19.server;fillColor=#4A4A4A;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="520" width="40" height="40" as="geometry"/>
</mxCell>
```

## Icon Sizing

- **Core Devices (Routers, Switches)**: 60x60 pixels
- **Access Devices**: 50x50 pixels
- **Endpoints**: 40x40 pixels
- **Cloud/WAN**: 80x80 pixels
- **Spacing**: 100-120px vertical, 80-100px horizontal

## Network Zones

Use containers to represent security zones:

```
┌─ DMZ ─────────────┐
│ [Web Server]      │
│ [Email Server]    │
└───────────────────┘
        ↓
  [Firewall]
        ↓
┌─ Internal ────────┐
│ [App Server]      │
│ [DB Server]       │
└───────────────────┘
```

## VLAN Representation

Use colored containers for VLANs:

```
┌─ VLAN 10 (Blue) ──┐  ┌─ VLAN 20 (Green) ─┐
│ [PC] [PC]         │  │ [Server] [Server] │
└───────────────────┘  └───────────────────┘
          ↓                      ↓
      [Multilayer Switch]
```

## Tips

1. Always call `get_shape_library("cisco19")` before generating network diagrams
2. Use exact shape names as listed above
3. Use color coding for different device types
4. Show redundancy with parallel paths
5. Label VLANs and subnets clearly
6. Indicate port numbers on connections
7. Use containers for security zones

## Common Network Patterns

### Three-Tier Architecture
```
┌─ Core Layer ──────┐
│ [Core Switch]     │
└───────────────────┘
         ↓
┌─ Distribution ────┐
│ [Dist Switch]     │
└───────────────────┘
         ↓
┌─ Access Layer ────┐
│ [Access Switches] │
└───────────────────────┘
```

### SD-WAN
```
[Branch Router] ──→ [SD-WAN Cloud] ←── [Data Center]
                           ↓
                    [Branch Sites]
```

### VPN Topology
```
[Remote User] → [Internet] → [VPN Concentrator] → [Internal Network]
                                     ↓
                                [Firewall]
```

## Best Practices

1. **Hierarchy**: Arrange devices in layers (core, distribution, access)
2. **Redundancy**: Show backup paths with dashed lines
3. **Security**: Clearly mark security boundaries
4. **Labeling**: Include IP addresses, VLANs, port numbers
5. **Color Coding**: Consistent colors for device types
6. **Physical vs Logical**: Indicate whether it's physical or logical topology
7. **Documentation**: Add notes for configuration details
