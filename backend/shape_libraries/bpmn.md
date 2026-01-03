# BPMN (Business Process Model and Notation) Shape Library

Business process modeling shapes for workflow and process diagrams.

## Usage

```
style="ellipse;fillColor=#D5E8D4;strokeColor=#82B366;"
```

## BPMN Elements

### Events
**Start Events**:
- **Start Event**: Circle (thin border)
- **Message Start**: Circle with envelope icon
- **Timer Start**: Circle with clock icon
- **Conditional Start**: Circle with document icon

**Intermediate Events**:
- **Intermediate Event**: Circle (double border)
- **Message Intermediate**: Double circle with envelope
- **Timer Intermediate**: Double circle with clock
- **Error Intermediate**: Double circle with lightning

**End Events**:
- **End Event**: Circle (thick border)
- **Message End**: Thick circle with filled envelope
- **Error End**: Thick circle with filled lightning
- **Terminate End**: Thick circle with filled circle

### Activities
- **Task**: Rounded rectangle
- **Sub-Process**: Rounded rectangle with + symbol
- **Call Activity**: Rounded rectangle (thick border)
- **User Task**: Rounded rectangle with person icon
- **Service Task**: Rounded rectangle with gear icon
- **Script Task**: Rounded rectangle with script icon
- **Manual Task**: Rounded rectangle with hand icon
- **Business Rule Task**: Rounded rectangle with table icon
- **Send Task**: Rounded rectangle with filled envelope
- **Receive Task**: Rounded rectangle with empty envelope

### Gateways
- **Exclusive Gateway (XOR)**: Diamond with X
- **Inclusive Gateway (OR)**: Diamond with O
- **Parallel Gateway (AND)**: Diamond with +
- **Event-Based Gateway**: Diamond with pentagon
- **Complex Gateway**: Diamond with asterisk

### Connecting Objects
- **Sequence Flow**: Solid arrow
- **Message Flow**: Dashed arrow
- **Association**: Dotted line
- **Data Association**: Dashed line with arrow

### Swimlanes
- **Pool**: Large container representing organization
- **Lane**: Subdivision within pool for roles/departments

### Artifacts
- **Data Object**: Document shape
- **Data Store**: Cylinder
- **Group**: Dashed rectangle
- **Text Annotation**: Open rectangle with dashed line

## Example: Simple Process

```xml
<!-- Start Event -->
<mxCell id="2" value="Start" 
  style="ellipse;fillColor=#D5E8D4;strokeColor=#82B366;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="115" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Task -->
<mxCell id="3" value="Process Order" 
  style="rounded=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
  vertex="1" parent="1">
  <mxGeometry x="200" y="110" width="120" height="60" as="geometry"/>
</mxCell>

<!-- Gateway -->
<mxCell id="4" value="" 
  style="rhombus;fillColor=#FFF2CC;strokeColor=#D6B656;" 
  vertex="1" parent="1">
  <mxGeometry x="370" y="115" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Task (Approved) -->
<mxCell id="5" value="Ship Product" 
  style="rounded=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
  vertex="1" parent="1">
  <mxGeometry x="470" y="50" width="120" height="60" as="geometry"/>
</mxCell>

<!-- Task (Rejected) -->
<mxCell id="6" value="Notify Customer" 
  style="rounded=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
  vertex="1" parent="1">
  <mxGeometry x="470" y="170" width="120" height="60" as="geometry"/>
</mxCell>

<!-- End Event -->
<mxCell id="7" value="End" 
  style="ellipse;fillColor=#F8CECC;strokeColor=#B85450;strokeWidth=3;" 
  vertex="1" parent="1">
  <mxGeometry x="640" y="115" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Sequence Flows -->
<mxCell id="8" value="" style="endArrow=classic;" edge="1" parent="1" source="2" target="3"/>
<mxCell id="9" value="" style="endArrow=classic;" edge="1" parent="1" source="3" target="4"/>
<mxCell id="10" value="Approved" style="endArrow=classic;" edge="1" parent="1" source="4" target="5"/>
<mxCell id="11" value="Rejected" style="endArrow=classic;" edge="1" parent="1" source="4" target="6"/>
```

## Example: Swimlane Diagram

```xml
<!-- Pool -->
<mxCell id="pool" value="Order Processing" 
  style="swimlane;horizontal=0;startSize=30;fillColor=#E1D5E7;" 
  vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="700" height="300" as="geometry"/>
</mxCell>

<!-- Lane 1: Customer -->
<mxCell id="lane1" value="Customer" 
  style="swimlane;horizontal=0;startSize=30;fillColor=#DAE8FC;" 
  vertex="1" parent="pool">
  <mxGeometry y="30" width="700" height="90" as="geometry"/>
</mxCell>

<!-- Lane 2: Sales -->
<mxCell id="lane2" value="Sales" 
  style="swimlane;horizontal=0;startSize=30;fillColor=#D5E8D4;" 
  vertex="1" parent="pool">
  <mxGeometry y="120" width="700" height="90" as="geometry"/>
</mxCell>

<!-- Lane 3: Warehouse -->
<mxCell id="lane3" value="Warehouse" 
  style="swimlane;horizontal=0;startSize=30;fillColor=#FFF2CC;" 
  vertex="1" parent="pool">
  <mxGeometry y="210" width="700" height="90" as="geometry"/>
</mxCell>
```

## Color Guidelines

- **Start Events**: Green (#D5E8D4)
- **End Events**: Red/Pink (#F8CECC)
- **Tasks**: Blue (#DAE8FC)
- **Gateways**: Yellow (#FFF2CC)
- **Pools/Lanes**: Purple/Varied (#E1D5E7)

## Common Patterns

### Sequential Flow
```
[Start] → [Task A] → [Task B] → [End]
```

### Exclusive Decision
```
[Task] → [XOR Gateway] → [Option A]
                       → [Option B]
```

### Parallel Activities
```
[Start] → [AND Gateway] → [Task A]
                        → [Task B]
         (both must complete)
         [AND Gateway] → [End]
```

### Event-Based Decision
```
[Task] → [Event Gateway] → [Message Event]
                         → [Timer Event]
```

### Subprocess
```
[Start] → [Task] → [+Subprocess] → [Task] → [End]
```

## Task Types

- **User Task**: Human interaction required
- **Service Task**: Automated service call
- **Script Task**: Execute script
- **Manual Task**: Manual work (not system)
- **Business Rule Task**: Apply business rules
- **Send/Receive Task**: Message handling

## Gateway Types

- **XOR (Exclusive)**: One path only
- **OR (Inclusive)**: One or more paths
- **AND (Parallel)**: All paths
- **Event-Based**: Wait for event

## Best Practices

1. **Start/End**: Every process has start and end events
2. **Gateway Pairs**: Open with gateway, close with matching gateway
3. **Label Flows**: Label decision branches clearly
4. **Swimlanes**: Use lanes for different roles
5. **Keep Simple**: One diagram per process level
6. **Data Objects**: Show important data
7. **Error Handling**: Include error events and paths
