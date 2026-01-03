"""
XML Validation and Processing Utilities

Handles draw.io XML validation, formatting, and manipulation.
Based on next-ai-draw-io utils.ts patterns.
"""

import re
import xml.etree.ElementTree as ET
from typing import Optional, List, Dict, Tuple


class XMLValidationError(Exception):
    """Raised when XML validation fails"""
    pass


def validate_mxcell_xml(xml: str) -> Tuple[bool, Optional[str]]:
    """
    Validate mxCell XML fragments
    
    Rules:
    1. Must contain only mxCell elements
    2. No wrapper tags (mxfile, mxGraphModel, root)
    3. No root cells (id="0" or id="1")
    4. All mxCell elements are siblings
    5. Every mxCell has unique id
    6. Every mxCell has parent attribute
    7. Every cell has mxGeometry child (if vertex or edge)
    
    Args:
        xml: XML string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check for wrapper tags that shouldn't be there
        forbidden_tags = ['<mxfile', '<mxGraphModel', '<root']
        for tag in forbidden_tags:
            if tag in xml:
                return False, f"XML must not contain {tag} tag - only mxCell elements"
        
        # Parse XML
        # Wrap in temporary root for parsing
        wrapped = f"<root>{xml}</root>"
        try:
            tree = ET.fromstring(wrapped)
        except ET.ParseError as e:
            return False, f"XML parsing error: {str(e)}"
        
        # Check all elements are mxCell
        cells = list(tree)
        if not cells:
            return False, "No mxCell elements found"
        
        for cell in cells:
            if cell.tag != 'mxCell':
                return False, f"Found non-mxCell element: {cell.tag}"
        
        # Check for root cells (id="0" or id="1")
        ids = set()
        for cell in cells:
            cell_id = cell.get('id')
            if not cell_id:
                return False, "Found mxCell without id attribute"
            
            if cell_id in ['0', '1']:
                return False, f"Root cells (id='0' or id='1') should not be included"
            
            # Check for duplicate IDs
            if cell_id in ids:
                return False, f"Duplicate cell ID found: {cell_id}"
            ids.add(cell_id)
            
            # Check parent attribute exists
            if not cell.get('parent'):
                return False, f"mxCell id='{cell_id}' missing parent attribute"
            
            # Check for mxGeometry if vertex or edge
            is_vertex = cell.get('vertex') == '1'
            is_edge = cell.get('edge') == '1'
            
            if is_vertex or is_edge:
                geometry = cell.find('mxGeometry')
                if geometry is None:
                    return False, f"mxCell id='{cell_id}' is missing mxGeometry element"
        
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def wrap_mxfile(mxcells: str) -> str:
    """
    Wrap mxCell elements in complete draw.io XML structure
    
    Args:
        mxcells: String of mxCell elements
        
    Returns:
        Complete XML with mxfile wrapper
    """
    return f'''<mxfile host="arcgen" agent="arcgen" version="1.0">
  <diagram name="Architecture">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {mxcells}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''


def extract_mxcells(full_xml: str) -> str:
    """
    Extract mxCell elements from complete draw.io XML
    
    Args:
        full_xml: Complete draw.io XML document
        
    Returns:
        String containing only mxCell elements (excluding root cells)
    """
    try:
        tree = ET.fromstring(full_xml)
        
        # Find all mxCell elements
        cells = tree.findall(".//mxCell")
        
        # Filter out root cells
        non_root_cells = [
            cell for cell in cells 
            if cell.get('id') not in ['0', '1']
        ]
        
        # Convert back to string
        result = []
        for cell in non_root_cells:
            result.append(ET.tostring(cell, encoding='unicode'))
        
        return '\n'.join(result)
        
    except Exception as e:
        raise XMLValidationError(f"Failed to extract mxCells: {str(e)}")


def validate_and_fix_xml(xml: str) -> str:
    """
    Validate XML and attempt to fix common issues
    
    Args:
        xml: XML string to validate and fix
        
    Returns:
        Fixed XML string
        
    Raises:
        XMLValidationError: If XML cannot be fixed
    """
    # Remove any leading/trailing whitespace
    xml = xml.strip()
    
    # Fix common XML entity issues
    xml = xml.replace('&', '&amp;')
    xml = xml.replace('&amp;amp;', '&amp;')  # Don't double-escape
    xml = xml.replace('&amp;lt;', '&lt;')
    xml = xml.replace('&amp;gt;', '&gt;')
    xml = xml.replace('&amp;quot;', '&quot;')
    
    # Validate
    is_valid, error = validate_mxcell_xml(xml)
    if not is_valid:
        raise XMLValidationError(error)
    
    return xml


def apply_edit_operation(
    current_xml: str,
    operation: str,
    cell_id: str,
    new_xml: Optional[str] = None
) -> str:
    """
    Apply an edit operation to existing diagram XML
    
    Args:
        current_xml: Current complete diagram XML
        operation: One of 'add', 'update', 'delete'
        cell_id: ID of cell to modify
        new_xml: New XML for add/update operations
        
    Returns:
        Updated complete XML
        
    Raises:
        XMLValidationError: If operation fails
    """
    try:
        # Parse current XML
        tree = ET.fromstring(current_xml)
        root_element = tree.find(".//root")
        
        if root_element is None:
            raise XMLValidationError("Cannot find root element in current XML")
        
        if operation == 'delete':
            # Find and remove cell
            for cell in root_element.findall(".//mxCell"):
                if cell.get('id') == cell_id:
                    root_element.remove(cell)
                    return ET.tostring(tree, encoding='unicode')
            raise XMLValidationError(f"Cell with id '{cell_id}' not found for deletion")
        
        elif operation == 'update':
            if not new_xml:
                raise XMLValidationError("new_xml required for update operation")
            
            # Parse new cell
            new_cell = ET.fromstring(new_xml)
            
            # Find and replace cell
            for i, cell in enumerate(root_element.findall(".//mxCell")):
                if cell.get('id') == cell_id:
                    root_element[i] = new_cell
                    return ET.tostring(tree, encoding='unicode')
            raise XMLValidationError(f"Cell with id '{cell_id}' not found for update")
        
        elif operation == 'add':
            if not new_xml:
                raise XMLValidationError("new_xml required for add operation")
            
            # Parse and add new cell
            new_cell = ET.fromstring(new_xml)
            
            # Check for duplicate ID
            for cell in root_element.findall(".//mxCell"):
                if cell.get('id') == cell_id:
                    raise XMLValidationError(f"Cell with id '{cell_id}' already exists")
            
            root_element.append(new_cell)
            return ET.tostring(tree, encoding='unicode')
        
        else:
            raise XMLValidationError(f"Unknown operation: {operation}")
            
    except ET.ParseError as e:
        raise XMLValidationError(f"XML parsing error: {str(e)}")
    except Exception as e:
        raise XMLValidationError(f"Edit operation failed: {str(e)}")


def get_cell_ids(xml: str) -> List[str]:
    """
    Extract all cell IDs from XML
    
    Args:
        xml: XML string
        
    Returns:
        List of cell IDs
    """
    try:
        tree = ET.fromstring(xml)
        cells = tree.findall(".//mxCell")
        return [cell.get('id') for cell in cells if cell.get('id')]
    except Exception:
        return []


def generate_unique_id(existing_ids: List[str], prefix: str = "cell") -> str:
    """
    Generate a unique cell ID
    
    Args:
        existing_ids: List of existing IDs to avoid
        prefix: Prefix for the ID
        
    Returns:
        Unique ID string
    """
    counter = 2  # Start from 2 (0 and 1 are root cells)
    while True:
        new_id = f"{prefix}-{counter}"
        if new_id not in existing_ids:
            return new_id
        counter += 1
