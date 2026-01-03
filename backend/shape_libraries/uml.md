# UML (Unified Modeling Language) Shape Library

UML diagrams for software design and architecture. Complete set of UML 2.5 shapes.

## Usage

Standard shapes use basic draw.io shape names:
```
style="rectangle;fillColor=#E1D5E7;strokeColor=#9673A6;"
```

## UML Diagram Types

### Class Diagrams
**Elements**:
- **Class Box**: Rectangle divided into 3 sections (name, attributes, methods)
- **Interface**: Rectangle with «interface» stereotype
- **Abstract Class**: Class name in italics
- **Enumeration**: «enumeration» stereotype

**Relationships**:
- **Association**: Solid line
- **Aggregation**: Line with empty diamond
- **Composition**: Line with filled diamond
- **Inheritance**: Line with empty triangle arrow
- **Realization**: Dashed line with empty triangle
- **Dependency**: Dashed line with arrow

### Sequence Diagrams
- **Actor**: Stick figure
- **Object/Participant**: Rectangle
- **Lifeline**: Dashed vertical line
- **Activation**: Narrow rectangle on lifeline
- **Message**: Horizontal arrow
- **Return Message**: Dashed arrow
- **Create Message**: Arrow to new object
- **Destroy**: X at end of lifeline

### Use Case Diagrams
- **Use Case**: Ellipse
- **Actor**: Stick figure
- **System Boundary**: Rectangle
- **Association**: Solid line
- **Include**: Dashed arrow with «include»
- **Extend**: Dashed arrow with «extend»
- **Generalization**: Solid arrow

### Activity Diagrams
- **Initial Node**: Filled circle
- **Final Node**: Filled circle with outer ring
- **Action**: Rounded rectangle
- **Decision**: Diamond
- **Merge**: Diamond
- **Fork/Join**: Thick horizontal/vertical bar
- **Swimlane**: Vertical container

### State Machine Diagrams
- **State**: Rounded rectangle
- **Initial State**: Filled circle
- **Final State**: Filled circle with outer ring
- **Transition**: Arrow with label
- **Choice**: Diamond
- **Fork/Join**: Bar

### Component Diagrams
- **Component**: Rectangle with «component»
- **Interface**: Circle (provided) or half-circle (required)
- **Port**: Small square on component edge
- **Dependency**: Dashed arrow

### Deployment Diagrams
- **Node**: 3D box
- **Artifact**: Rectangle with «artifact»
- **Communication Path**: Solid line
- **Deployment**: Dashed arrow with «deploy»

## Example: Class Diagram

```xml
<!-- Class -->
<mxCell id="2" value="User&#13;&#10;---&#13;&#10;- id: int&#13;&#10;- name: string&#13;&#10;- email: string&#13;&#10;---&#13;&#10;+ login()&#13;&#10;+ logout()" 
  style="rectangle;fillColor=#E1D5E7;strokeColor=#9673A6;align=left;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="140" as="geometry"/>
</mxCell>

<!-- Another Class -->
<mxCell id="3" value="Order&#13;&#10;---&#13;&#10;- id: int&#13;&#10;- total: decimal&#13;&#10;---&#13;&#10;+ calculate()&#13;&#10;+ submit()" 
  style="rectangle;fillColor=#E1D5E7;strokeColor=#9673A6;align=left;" 
  vertex="1" parent="1">
  <mxGeometry x="350" y="100" width="160" height="120" as="geometry"/>
</mxCell>

<!-- Association -->
<mxCell id="4" value="places" 
  style="endArrow=none;html=1;" 
  edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Example: Sequence Diagram

```xml
<!-- Actor -->
<mxCell id="2" value="User" 
  style="shape=umlActor;fillColor=#DAE8FC;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="30" height="60" as="geometry"/>
</mxCell>

<!-- Object -->
<mxCell id="3" value="System" 
  style="rectangle;fillColor=#D5E8D4;" 
  vertex="1" parent="1">
  <mxGeometry x="250" y="40" width="100" height="40" as="geometry"/>
</mxCell>

<!-- Lifeline -->
<mxCell id="4" value="" 
  style="dashed=1;dashPattern=1 2;" 
  edge="1" parent="1" source="2">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="115" y="400" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- Message -->
<mxCell id="5" value="login()" 
  style="endArrow=block;html=1;" 
  edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Color Guidelines

- **Classes/Objects**: Purple (#E1D5E7)
- **Actors**: Blue (#DAE8FC)
- **States**: Green (#D5E8D4)
- **Activities**: Yellow (#FFF2CC)
- **Components**: Orange (#FFE6CC)

## Common Patterns

### MVC Pattern
```
[View] ←→ [Controller] ←→ [Model]
```

### Observer Pattern
```
[Subject] --notify--> [Observer]
    ↓
[ConcreteSubject]  [ConcreteObserver]
```

### Factory Pattern
```
      [Creator]
          ↓
   [ConcreteCreator]
          ↓ creates
      [Product]
```

## Best Practices

1. **Use Stereotypes**: «interface», «abstract», «singleton»
2. **Multiplicity**: Show cardinality (1, *, 0..1, 1..*)
3. **Visibility**: + (public), - (private), # (protected)
4. **Naming**: Classes are nouns, methods are verbs
5. **Abstraction**: Keep diagrams focused on one aspect
6. **Layout**: Left-to-right or top-to-bottom flow
