# Flowchart Shape Library

Standard flowchart shapes for process diagrams and workflows.

## Usage

In your mxCell style attribute, use standard shape names:
```
style="ellipse;fillColor=#dae8fc;strokeColor=#6c8ebf;"
```

## Standard Flowchart Shapes

### Basic Shapes
- **Rectangle**: `rectangle` - Process/Action
- **Ellipse**: `ellipse` - Start/End
- **Diamond**: `rhombus` - Decision
- **Parallelogram**: `parallelogram` - Input/Output
- **Cylinder**: `cylinder` - Database
- **Document**: `document` - Document/Report
- **Triangle**: `triangle` - Manual Operation

### Advanced Shapes
- **Hexagon**: `hexagon` - Preparation
- **Trapezoid**: `trapezoid` - Manual Input
- **Cloud**: `cloud` - Cloud Process
- **Note**: `note` - Annotation
- **Card**: `card` - Punch Card
- **Tape**: `tape` - Tape/Sequential Access

## Connector Styles

### Arrow Types
- **Classic Arrow**: `endArrow=classic`
- **Open Arrow**: `endArrow=open`
- **Block Arrow**: `endArrow=block`
- **Diamond Arrow**: `endArrow=diamond`
- **Oval Arrow**: `endArrow=oval`

### Line Styles
- **Solid**: `dashed=0`
- **Dashed**: `dashed=1`
- **Dotted**: `dashed=1;dashPattern=1 4`

## Color Schemes

### Process Colors (Light)
- **Blue**: fillColor=#dae8fc; strokeColor=#6c8ebf
- **Green**: fillColor=#d5e8d4; strokeColor=#82b366
- **Yellow**: fillColor=#fff2cc; strokeColor=#d6b656
- **Orange**: fillColor=#ffe6cc; strokeColor=#d79b00
- **Red**: fillColor=#f8cecc; strokeColor=#b85450

### Process Colors (Dark)
- **Dark Blue**: fillColor=#1ba1e2; strokeColor=#006EAF
- **Dark Green**: fillColor=#60a917; strokeColor=#2D7600
- **Dark Orange**: fillColor=#fa6800; strokeColor=#C73500

## Examples

### Start/End Terminal
```xml
<mxCell id="2" value="Start" 
  style="ellipse;fillColor=#d5e8d4;strokeColor=#82b366;" 
  vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

### Process Rectangle
```xml
<mxCell id="3" value="Process Data" 
  style="rectangle;fillColor=#dae8fc;strokeColor=#6c8ebf;" 
  vertex="1" parent="1">
  <mxGeometry x="40" y="140" width="120" height="60" as="geometry"/>
</mxCell>
```

### Decision Diamond
```xml
<mxCell id="4" value="Valid?" 
  style="rhombus;fillColor=#fff2cc;strokeColor=#d6b656;" 
  vertex="1" parent="1">
  <mxGeometry x="50" y="240" width="100" height="80" as="geometry"/>
</mxCell>
```

### Database Cylinder
```xml
<mxCell id="5" value="Database" 
  style="cylinder;fillColor=#e1d5e7;strokeColor=#9673a6;" 
  vertex="1" parent="1">
  <mxGeometry x="300" y="140" width="80" height="80" as="geometry"/>
</mxCell>
```

### Arrow Connection
```xml
<mxCell id="6" value="" 
  style="endArrow=classic;html=1;" 
  edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Labeled Arrow
```xml
<mxCell id="7" value="Yes" 
  style="endArrow=classic;html=1;" 
  edge="1" parent="1" source="4" target="5">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="150" y="280" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

## Best Practices

1. **Start/End**: Use ellipses with green fill
2. **Processes**: Use rectangles with blue fill
3. **Decisions**: Use rhombus (diamond) with yellow fill
4. **Data/Database**: Use cylinder with purple fill
5. **Input/Output**: Use parallelogram with orange fill

6. **Consistent Sizing**:
   - Ellipse: 120x60
   - Rectangle: 120x60
   - Diamond: 100x80
   - Cylinder: 80x80

7. **Spacing**: Leave 80-120px between shapes

8. **Arrows**: Use classic arrow style for most connections

## Common Workflows

### Simple Process Flow
```
[Start] → [Process 1] → [Process 2] → [End]
```

### Decision Flow
```
[Start] → [Input] → [Decision?]
                         ├─ Yes → [Process A] → [End]
                         └─ No  → [Process B] → [End]
```

### Loop Flow
```
[Start] → [Initialize] → [Process] → [Decision?]
                              └─ No (loop back to Process)
                              └─ Yes → [End]
```
