# Network & Rack Diagram Shape Library

Data center and network infrastructure diagrams.

## Usage

```
style="shape=mxgraph.rack.DEVICE;fillColor=#B0B0B0;"
```

## Rack Equipment

### Servers
- **1U Server**: `shape=mxgraph.rack.server_1u`
- **2U Server**: `shape=mxgraph.rack.server_2u`
- **4U Server**: `shape=mxgraph.rack.server_4u`
- **Blade Server**: `shape=mxgraph.rack.blade_server`
- **Blade Chassis**: `shape=mxgraph.rack.blade_chassis`

### Networking
- **Network Switch (1U)**: `shape=mxgraph.rack.switch_1u`
- **Core Switch**: `shape=mxgraph.rack.core_switch`
- **Router**: `shape=mxgraph.rack.router`
- **Firewall**: `shape=mxgraph.rack.firewall`
- **Load Balancer**: `shape=mxgraph.rack.load_balancer`
- **Patch Panel**: `shape=mxgraph.rack.patch_panel`

### Storage
- **SAN Array**: `shape=mxgraph.rack.san`
- **NAS Device**: `shape=mxgraph.rack.nas`
- **Tape Library**: `shape=mxgraph.rack.tape_library`
- **Disk Array**: `shape=mxgraph.rack.disk_array`

### Power & Cooling
- **UPS**: `shape=mxgraph.rack.ups`
- **PDU (Power Distribution)**: `shape=mxgraph.rack.pdu`
- **Rack Cooling Unit**: `shape=mxgraph.rack.cooling`
- **Power Supply**: `shape=mxgraph.rack.power`

### Other
- **KVM Switch**: `shape=mxgraph.rack.kvm`
- **Console**: `shape=mxgraph.rack.console`
- **Monitor**: `shape=mxgraph.rack.monitor`
- **Blank Plate**: `shape=mxgraph.rack.blank`

## Rack Sizes

Standard rack unit (U) measurements:
- **1U**: 1.75 inches (44.45mm)
- **2U**: 3.5 inches
- **4U**: 7 inches
- **Full Rack**: 42U (typically)
- **Half Rack**: 21U

## Example: Server Rack

```xml
<!-- Rack Container (42U) -->
<mxCell id="rack" value="Rack 01" 
  style="rounded=0;fillColor=#f5f5f5;strokeColor=#666666;align=center;verticalAlign=top;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="200" height="840" as="geometry"/>
</mxCell>

<!-- Switch (1U) at top -->
<mxCell id="2" value="Core Switch" 
  style="rectangle;fillColor=#4D4D4D;strokeColor=#333333;fontColor=#ffffff;" 
  vertex="1" parent="rack">
  <mxGeometry x="10" y="20" width="180" height="20" as="geometry"/>
</mxCell>

<!-- Server (2U) -->
<mxCell id="3" value="Web Server 01" 
  style="rectangle;fillColor=#666666;strokeColor=#333333;fontColor=#ffffff;" 
  vertex="1" parent="rack">
  <mxGeometry x="10" y="60" width="180" height="40" as="geometry"/>
</mxCell>

<!-- Server (2U) -->
<mxCell id="4" value="App Server 01" 
  style="rectangle;fillColor=#666666;strokeColor=#333333;fontColor=#ffffff;" 
  vertex="1" parent="rack">
  <mxGeometry x="10" y="120" width="180" height="40" as="geometry"/>
</mxCell>

<!-- Storage (4U) -->
<mxCell id="5" value="SAN Array" 
  style="rectangle;fillColor=#999999;strokeColor=#333333;fontColor=#ffffff;" 
  vertex="1" parent="rack">
  <mxGeometry x="10" y="180" width="180" height="80" as="geometry"/>
</mxCell>

<!-- UPS (2U) at bottom -->
<mxCell id="6" value="UPS" 
  style="rectangle;fillColor=#333333;strokeColor=#000000;fontColor=#ffffff;" 
  vertex="1" parent="rack">
  <mxGeometry x="10" y="780" width="180" height="40" as="geometry"/>
</mxCell>
```

## Network Topology Shapes

### Physical Devices
- **Patch Panel**: Horizontal bar with ports
- **Cable Tray**: Container above racks
- **Cable**: Line connector
- **Fiber Optic**: Red/orange line
- **Ethernet**: Blue/black line

### Rack Layout
- **42U Rack**: 840px height (20px per U)
- **Device Spacing**: 10px margins
- **Labels**: Left-aligned, white text

## Color Guidelines

- **Servers**: Dark gray (#666666)
- **Networking**: Medium gray (#4D4D4D)
- **Storage**: Light gray (#999999)
- **Power**: Very dark (#333333)
- **Blank Panels**: Light (#B0B0B0)

## Cable Management

```xml
<!-- Fiber Connection (red) -->
<mxCell id="fiber" value="" 
  style="endArrow=none;strokeColor=#FF0000;strokeWidth=2;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Ethernet (blue) -->
<mxCell id="eth" value="" 
  style="endArrow=none;strokeColor=#0000FF;strokeWidth=1;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Power (black) -->
<mxCell id="power" value="" 
  style="endArrow=none;strokeColor=#000000;strokeWidth=3;" 
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Data Center Layout

```
┌─ Row A ──────────────────────────┐
│ [Rack 1] [Rack 2] [Rack 3]      │
└──────────────────────────────────┘

     ┌─ Hot Aisle ──┐
     
┌─ Row B ──────────────────────────┐
│ [Rack 4] [Rack 5] [Rack 6]      │
└──────────────────────────────────┘

     ┌─ Cold Aisle ──┐
```

## Best Practices

1. **Label Everything**: Rack number, device name, U position
2. **Show Port Connections**: Indicate which ports connect
3. **Cable Colors**: Use standard (fiber=red, eth=blue, power=black)
4. **U Positions**: Mark starting U for each device
5. **Power Redundancy**: Show dual power supplies
6. **Cooling**: Indicate hot/cold aisles
7. **Management**: Include KVM and management network

## Rack Elevation View

```
U42 [Blank Panel]
U41 [Core Switch]
U40 [Patch Panel]
U39-U38 [Firewall (2U)]
U37-U36 [Load Balancer (2U)]
U35-U34 [Server 1 (2U)]
U33-U32 [Server 2 (2U)]
...
U04-U01 [UPS (4U)]
```

## Example: Full Data Center

```
[Building]
  ├─ Floor 1: Operations Center
  │    ├─ NOC (Network Operations)
  │    └─ Security Office
  │
  └─ Floor 2: Data Center
       ├─ Server Room A
       │    ├─ Row 1 (10 Racks)
       │    └─ Row 2 (10 Racks)
       │
       ├─ Server Room B
       │    └─ Storage Arrays
       │
       └─ Infrastructure
            ├─ UPS Room
            ├─ Generator Room
            └─ Cooling Plant
```
