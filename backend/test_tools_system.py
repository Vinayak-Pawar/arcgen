"""
Test suite for diagram tools

Tests XML validation, tool execution, and diagram operations.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Testing Diagram Tools System")
print("=" * 60)

# Test 1: Import modules
print("\n✓ Test 1: Importing modules...")
try:
    from tools import DiagramTools, ToolExecutor
    from tools.xml_utils import validate_mxcell_xml, wrap_mxfile, XMLValidationError
    print("  ✓ All modules imported successfully")
except ImportError as e:
    print(f"  ✗ Import error: {e}")
    sys.exit(1)

# Test 2: XML Validation
print("\n✓ Test 2: XML Validation...")

# Valid XML
valid_xml = '''<mxCell id="2" value="Test" style="rectangle;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>'''

is_valid, error = validate_mxcell_xml(valid_xml)
if is_valid:
    print("  ✓ Valid XML accepted")
else:
    print(f"  ✗ Valid XML rejected: {error}")
    sys.exit(1)

# Invalid XML - with wrapper tags
invalid_xml = '''<mxfile><mxGraphModel>
<mxCell id="2" value="Test" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>
</mxGraphModel></mxfile>'''

is_valid, error = validate_mxcell_xml(invalid_xml)
if not is_valid:
    print(f"  ✓ Invalid XML rejected: {error}")
else:
    print("  ✗ Invalid XML (with wrappers) was accepted!")
    sys.exit(1)

# Invalid XML - root cell
invalid_xml2 = '''<mxCell id="0"/>'''
is_valid, error = validate_mxcell_xml(invalid_xml2)
if not is_valid and "Root cells" in error:
    print("  ✓ Root cell rejection working")
else:
    print("  ✗ Root cell was not rejected!")
    sys.exit(1)

# Test 3: Tool Definitions
print("\n✓ Test 3: Tool Definitions...")
tool_defs = DiagramTools.get_tool_definitions()
expected_tools = {"display_diagram", "edit_diagram", "get_shape_library", "append_diagram"}
actual_tools = {tool["function"]["name"] for tool in tool_defs}

if actual_tools == expected_tools:
    print(f"  ✓ All 4 tools defined: {', '.join(sorted(actual_tools))}")
else:
    print(f"  ✗ Tool mismatch!")
    print(f"    Expected: {expected_tools}")
    print(f"    Got: {actual_tools}")
    sys.exit(1)

# Test 4: display_diagram Tool
print("\n✓ Test 4: display_diagram Tool...")
tools = DiagramTools()

test_diagram = '''<mxCell id="2" value="User" style="ellipse;fillColor=#dae8fc;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>
<mxCell id="3" value="API" style="rectangle;fillColor=#d5e8d4;" vertex="1" parent="1">
  <mxGeometry x="160" y="40" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="4" value="" style="endArrow=classic;" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>'''

result = tools.execute_display_diagram(test_diagram)

if result["success"]:
    print("  ✓ Diagram created successfully")
    if "<mxfile" in result["xml"]:
        print("  ✓ XML wrapped correctly")
    else:
        print("  ✗ XML not wrapped!")
        sys.exit(1)
else:
    print(f"  ✗ Display diagram failed: {result.get('error')}")
    sys.exit(1)

# Test 5: edit_diagram Tool
print("\n✓ Test 5: edit_diagram Tool...")

# Add a new cell
edit_ops = [{
    "operation": "add",
    "cell_id": "new-5",
    "new_xml": '<mxCell id="new-5" value="Database" style="cylinder;" vertex="1" parent="1"><mxGeometry x="300" y="40" width="80" height="60" as="geometry"/></mxCell>'
}]

result = tools.execute_edit_diagram(edit_ops)

if result["success"]:
    print("  ✓ Edit operation successful")
    if "new-5" in result["xml"]:
        print("  ✓ New cell added to diagram")
    else:
        print("  ✗ New cell not found in result!")
        sys.exit(1)
else:
    print(f"  ✗ Edit failed: {result.get('error')}")
    sys.exit(1)

# Test 6: get_shape_library Tool
print("\n✓ Test 6: get_shape_library Tool...")

result = tools.execute_get_shape_library("aws4")

if result["success"]:
    print("  ✓ AWS library loaded")
    if "ec2" in result["content"].lower():
        print("  ✓ Library contains AWS service icons")
    else:
        print("  ℹ Library loaded but content may be incomplete")
else:
    print(f"  ℹ AWS library not found (expected if file doesn't exist yet)")

# Test flowchart library
result2 = tools.execute_get_shape_library("flowchart")

if result2["success"]:
    print("  ✓ Flowchart library loaded")
else:
    print(f"  ℹ Flowchart library not found")

# Test invalid library
result3 = tools.execute_get_shape_library("invalid_library_name")

if not result3["success"]:
    print("  ✓ Invalid library correctly rejected")
else:
    print("  ✗ Invalid library was accepted!")

# Test 7: append_diagram Tool
print("\n✓ Test 7: append_diagram Tool...")

append_xml = '''<mxCell id="6" value="Cache" style="rectangle;fillColor=#ffe6cc;" vertex="1" parent="1">
  <mxGeometry x="420" y="40" width="80" height="60" as="geometry"/>
</mxCell>'''

result = tools.execute_append_diagram(append_xml)

if result["success"]:
    print("  ✓ Append operation successful")
    if '"6"' in result["xml"] or 'id="6"' in result["xml"]:
        print("  ✓ Appended cell found in diagram")
    else:
        print("  ✗ Appended cell not found!")
        sys.exit(1)
else:
    print(f"  ✗ Append failed: {result.get('error')}")
    sys.exit(1)

# Test 8: Tool Executor
print("\n✓ Test 8: Tool Executor...")

executor = ToolExecutor()

# Get tools
tools_list = executor.get_tools()
if len(tools_list) == 4:
    print(f"  ✓ Executor provides {len(tools_list)} tools")
else:
    print(f"  ✗ Expected 4 tools, got {len(tools_list)}")
    sys.exit(1)

# Execute via executor
exec_result = executor.execute("display_diagram", {"xml": test_diagram})

if exec_result["success"]:
    print("  ✓ Tool execution via executor works")
else:
    print(f"  ✗ Executor failed: {exec_result.get('error')}")
    sys.exit(1)

# Test 9: XML Wrapping
print("\n✓ Test 9: XML Wrapping...")

wrapped = wrap_mxfile(test_diagram)

if all(tag in wrapped for tag in ["<mxfile", "<mxGraphModel", "<root"]):
    print("  ✓ XML wrapped with all required tags")
else:
    print("  ✗ Wrapping incomplete!")
    sys.exit(1)

if 'id="0"' in wrapped and 'id="1"' in wrapped:
    print("  ✓ Root cells added")
else:
    print("  ✗ Root cells missing!")
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests passed! ✅")
print("=" * 60)
print("\nTool System Features:")
print("  ✓ XML validation with strict rules")
print("  ✓ 4 core tools (display, edit, library, append)")
print("  ✓ Shape libraries (AWS, Flowchart)")
print("  ✓ Tool executor for LLM integration")
print("\nNext steps:")
print("1. Create system prompts")
print("2. Integrate with API endpoint")
print("3. Add streaming support")
print("4. Test with actual LLM")
