# ER Diagram (Entity-Relationship) Shape Library

Database modeling and entity-relationship diagrams. For designing database schemas.

## Usage

```
style="rectangle;fillColor=#E1D5E7;strokeColor=#9673A6;"
```

## ER Diagram Elements

### Entities
- **Entity (Strong)**: Rectangle
- **Entity (Weak)**: Double rectangle
- **Attribute**: Ellipse/Oval
- **Key Attribute**: Ellipse with underline
- **Multi-valued Attribute**: Double ellipse
- **Derived Attribute**: Dashed ellipse
- **Composite Attribute**: Ellipse with connected sub-ellipses

### Relationships
- **Relationship**: Diamond
- **Identifying Relationship**: Double diamond
- **Relationship Attribute**: Ellipse connected to diamond

### Cardinality Notations
- **One**: 1
- **Many**: N, M, *
- **One-to-One**: 1:1
- **One-to-Many**: 1:N
- **Many-to-Many**: M:N

### Chen Notation
- Entities: Rectangles
- Relationships: Diamonds
- Attributes: Ovals
- Lines show connections

### Crow's Foot Notation
- **One**: Single line perpendicular
- **Many**: Crow's foot (three lines)
- **Zero or One**: Circle + perpendicular line
- **Zero or Many**: Circle + crow's foot
- **One or Many**: Perpendicular line + crow's foot

## Example: Simple ER Diagram

```xml
<!-- Entity: Customer -->
<mxCell id="2" value="Customer" 
  style="rectangle;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- Entity: Order -->
<mxCell id="3" value="Order" 
  style="rectangle;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
  vertex="1" parent="1">
  <mxGeometry x="400" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- Relationship: Places -->
<mxCell id="4" value="Places" 
  style="rhombus;fillColor=#FFF2CC;strokeColor=#D6B656;" 
  vertex="1" parent="1">
  <mxGeometry x="260" y="90" width="100" height="80" as="geometry"/>
</mxCell>

<!-- Connect Customer to Relationship -->
<mxCell id="5" value="1" 
  style="endArrow=none;html=1;" 
  edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Connect Relationship to Order -->
<mxCell id="6" value="N" 
  style="endArrow=none;html=1;" 
  edge="1" parent="1" source="4" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Attribute: Customer ID -->
<mxCell id="7" value="customer_id" 
  style="ellipse;fillColor=#E1D5E7;strokeColor=#9673A6;" 
  vertex="1" parent="1">
  <mxGeometry x="50" y="40" width="100" height="40" as="geometry"/>
</mxCell>

<!-- Connect Attribute to Entity -->
<mxCell id="8" value="" 
  style="endArrow=none;html=1;" 
  edge="1" parent="1" source="7" target="2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Example: Crow's Foot Notation

```xml
<!-- Customer Entity -->
<mxCell id="2" value="Customer&#13;&#10;---&#13;&#10;PK: customer_id&#13;&#10;name&#13;&#10;email" 
  style="rectangle;fillColor=#DAE8FC;strokeColor=#6C8EBF;align=left;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="100" as="geometry"/>
</mxCell>

<!-- Order Entity -->
<mxCell id="3" value="Order&#13;&#10;---&#13;&#10;PK: order_id&#13;&#10;FK: customer_id&#13;&#10;total&#13;&#10;date" 
  style="rectangle;fillColor=#DAE8FC;strokeColor=#6C8EBF;align=left;" 
  vertex="1" parent="1">
  <mxGeometry x="350" y="100" width="140" height="110" as="geometry"/>
</mxCell>

<!-- One-to-Many Relationship -->
<mxCell id="4" value="" 
  style="endArrow=ERmany;startArrow=ERone;html=1;" 
  edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Database Table Representation

```xml
<mxCell id="2" value="users&#13;&#10;---&#13;&#10;PK: id (INTEGER)&#13;&#10;username (VARCHAR)&#13;&#10;email (VARCHAR)&#13;&#10;created_at (TIMESTAMP)" 
  style="rectangle;fillColor=#D5E8D4;strokeColor=#82B366;align=left;verticalAlign=top;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="120" as="geometry"/>
</mxCell>
```

## Color Guidelines

- **Entities**: Blue (#DAE8FC)
- **Relationships**: Yellow (#FFF2CC)
- **Attributes**: Purple (#E1D5E7)
- **Tables**: Green (#D5E8D4)

## Common Patterns

### One-to-One
```
[User] ─── 1:1 ─── [Profile]
```

### One-to-Many
```
[Customer] ─── 1:N ─── [Order]
```

### Many-to-Many
```
[Student] ─── M:N ─── [Course]
     (through Enrollment)
```

### Inheritance/Generalization
```
      [Employee]
      /        \
   [Manager]  [Developer]
```

## Key Notations

### Primary Key (PK)
- Underlined attribute
- Or: PK: field_name

### Foreign Key (FK)
- Dashed underline
- Or: FK: field_name

### Composite Key
- Multiple underlined attributes

### Mandatory/Optional
- **Mandatory**: Solid line
- **Optional**: Dashed line or (0,1)

## Best Practices

1. **Name Entities**: Use singular nouns (User, not Users)
2. **Name Relationships**: Use verbs (owns, contains, has)
3. **Normalize**: Aim for 3NF (3rd Normal Form)
4. **Show Cardinality**: Always indicate 1:1, 1:N, M:N
5. **Label Keys**: Clearly mark PK and FK
6. **Group Tables**: Related entities together
7. **Use Colors**: Different colors for entity types
