"""
File Upload and Processing System
Supports PDF text extraction and image analysis for diagram generation
Inspired by next-ai-draw-io's comprehensive file handling
"""

import os
import tempfile
import base64
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import io


class FileProcessor:
    """Processes uploaded files for diagram generation"""

    # Supported file types
    SUPPORTED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    SUPPORTED_DOCUMENT_TYPES = {'application/pdf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self):
        # Create temp directory for file processing
        self.temp_dir = Path(tempfile.gettempdir()) / "arcgen_files"
        self.temp_dir.mkdir(exist_ok=True)

    def process_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Process an uploaded file and extract relevant information

        Args:
            file_content: Raw file bytes
            filename: Original filename

        Returns:
            Dict containing processed data
        """
        file_size = len(file_content)
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes (max {self.MAX_FILE_SIZE})")

        # Determine file type
        file_extension = Path(filename).suffix.lower()
        content_type = self._guess_content_type(file_content, filename)

        # Process based on file type
        if content_type in self.SUPPORTED_DOCUMENT_TYPES:
            return self._process_pdf(file_content, filename)
        elif content_type in self.SUPPORTED_IMAGE_TYPES:
            return self._process_image(file_content, filename)
        else:
            raise ValueError(f"Unsupported file type: {content_type}")

    def _process_pdf(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Extract text and metadata from PDF files"""
        try:
            # Save to temp file for processing
            temp_path = self.temp_dir / f"temp_{hash(filename)}.pdf"
            temp_path.write_bytes(file_content)

            # Open with PyMuPDF
            doc = fitz.open(str(temp_path))

            # Extract text from all pages
            text_content = []
            metadata = {
                "page_count": len(doc),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "file_size": len(file_content)
            }

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                text_content.append(f"Page {page_num + 1}:\n{text}")

            # Clean up
            doc.close()
            temp_path.unlink(missing_ok=True)

            full_text = "\n\n".join(text_content)

            return {
                "content_type": "pdf",
                "filename": filename,
                "metadata": metadata,
                "summary": self._summarize_pdf_content(full_text, metadata),
                "extracted_text": full_text,
                "text_length": len(full_text),
                "has_images": self._pdf_has_images(file_content)
            }

        except Exception as e:
            raise ValueError(f"Failed to process PDF: {str(e)}")

    def _process_image(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Analyze image files for diagram generation"""
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(file_content))

            # Basic image analysis
            metadata = {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode,
                "file_size": len(file_content),
                "has_alpha": image.mode in ('RGBA', 'LA', 'P')
            }

            # Convert to base64 for AI processing
            base64_image = base64.b64encode(file_content).decode('utf-8')

            # Generate image description prompt for AI
            image_analysis = self._analyze_image_for_diagrams(metadata)

            return {
                "content_type": "image",
                "filename": filename,
                "metadata": metadata,
                "summary": image_analysis["description"],
                "base64_data": base64_image,
                "image_analysis": image_analysis,
                "data_url": f"data:image/{image.format.lower()};base64,{base64_image}"
            }

        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")

    def create_file_analysis_prompt(self, processed_data: Dict[str, Any]) -> str:
        """Create a specialized prompt for file-based diagram generation"""

        if processed_data["content_type"] == "pdf":
            return self._create_pdf_analysis_prompt(processed_data)
        elif processed_data["content_type"] == "image":
            return self._create_image_analysis_prompt(processed_data)
        else:
            return f"Analyze this {processed_data['content_type']} file and create a diagram: {processed_data.get('summary', '')}"

    def _create_pdf_analysis_prompt(self, pdf_data: Dict[str, Any]) -> str:
        """Create prompt for PDF-based diagram generation"""
        summary = pdf_data.get("summary", "")
        text_length = pdf_data.get("text_length", 0)
        page_count = pdf_data.get("metadata", {}).get("page_count", 0)

        prompt = f"""You have been provided with a PDF document analysis. Create a system architecture diagram that represents the content and structure described below.

PDF ANALYSIS:
{summary}

DOCUMENT DETAILS:
- Pages: {page_count}
- Text length: {text_length} characters
- Content type: Technical/business document

INSTRUCTIONS:
1. Analyze the document structure and identify key components, processes, or systems
2. Create a diagram that visually represents the main concepts from the document
3. Use appropriate shapes for different types of components (servers, databases, users, etc.)
4. Include relationships and data flow between components
5. Focus on the most important architectural elements mentioned

Generate a comprehensive diagram based on this document analysis."""

        return prompt

    def _create_image_analysis_prompt(self, image_data: Dict[str, Any]) -> str:
        """Create prompt for image-based diagram generation"""
        analysis = image_data.get("image_analysis", {})
        description = analysis.get("description", "")

        prompt = f"""You have been provided with an image analysis. Create a system architecture diagram that represents or improves upon the visual content described below.

IMAGE ANALYSIS:
{description}

INSTRUCTIONS:
1. If this appears to be an existing diagram, analyze its structure and create an improved version
2. If this is a photo/sketch, interpret it as a system design and create a professional diagram
3. Use appropriate technical shapes and connectors
4. Maintain the original intent while improving clarity and professionalism
5. Add any missing components or relationships that would make the system complete

Generate a professional diagram based on this image analysis."""

        return prompt

    def _summarize_pdf_content(self, full_text: str, metadata: Dict[str, Any]) -> str:
        """Create a summary of PDF content for diagram generation"""
        # Simple text analysis - in a real implementation, you'd use NLP
        lines = full_text.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]

        # Look for common technical terms
        technical_terms = []
        keywords = [
            'system', 'architecture', 'database', 'server', 'api', 'user', 'client',
            'service', 'component', 'module', 'interface', 'data', 'flow', 'process',
            'network', 'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes'
        ]

        found_keywords = set()
        for line in non_empty_lines[:50]:  # Check first 50 lines
            line_lower = line.lower()
            for keyword in keywords:
                if keyword in line_lower:
                    found_keywords.add(keyword)

        # Create summary
        summary_parts = []

        if metadata.get("title"):
            summary_parts.append(f"Title: {metadata['title']}")

        if found_keywords:
            summary_parts.append(f"Technical topics: {', '.join(sorted(found_keywords))}")

        # Sample content
        sample_text = ' '.join(non_empty_lines[:10])[:500]
        if sample_text:
            summary_parts.append(f"Sample content: {sample_text}...")

        return ' | '.join(summary_parts)

    def _analyze_image_for_diagrams(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze image metadata for diagram generation hints"""
        width, height = metadata["width"], metadata["height"]
        aspect_ratio = width / height if height > 0 else 1

        analysis = {
            "dimensions": f"{width}x{height}",
            "aspect_ratio": round(aspect_ratio, 2),
            "orientation": "landscape" if width > height else "portrait",
            "description": ""
        }

        # Basic analysis based on dimensions and characteristics
        if aspect_ratio > 2:
            analysis["description"] = "Wide image, possibly a flowchart or sequence diagram"
        elif aspect_ratio < 0.5:
            analysis["description"] = "Tall image, possibly a hierarchical diagram or mind map"
        else:
            analysis["description"] = "Square/rectangular image, suitable for system architecture diagrams"

        if metadata.get("has_alpha"):
            analysis["description"] += " with transparency"

        analysis["description"] += f". Image appears to be a technical diagram or system design sketch that should be converted to a professional draw.io diagram."

        return analysis

    def _pdf_has_images(self, file_content: bytes) -> bool:
        """Check if PDF contains images"""
        try:
            temp_path = self.temp_dir / "temp_check.pdf"
            temp_path.write_bytes(file_content)

            doc = fitz.open(str(temp_path))
            has_images = False

            for page in doc:
                if page.get_images():
                    has_images = True
                    break

            doc.close()
            temp_path.unlink(missing_ok=True)
            return has_images

        except:
            return False

    def _guess_content_type(self, file_content: bytes, filename: str) -> str:
        """Guess content type from file content and filename"""
        # Check file signature (magic bytes)
        if file_content.startswith(b'%PDF'):
            return 'application/pdf'
        elif file_content.startswith(b'\xff\xd8\xff'):
            return 'image/jpeg'
        elif file_content.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'image/png'
        elif file_content.startswith(b'GIF87a') or file_content.startswith(b'GIF89a'):
            return 'image/gif'
        elif file_content.startswith(b'RIFF') and file_content[8:12] == b'WEBP':
            return 'image/webp'

        # Fallback to extension
        ext = Path(filename).suffix.lower()
        if ext == '.pdf':
            return 'application/pdf'
        elif ext in ['.jpg', '.jpeg']:
            return 'image/jpeg'
        elif ext == '.png':
            return 'image/png'
        elif ext == '.gif':
            return 'image/gif'
        elif ext == '.webp':
            return 'image/webp'

        return 'application/octet-stream'


# Global instance
_file_processor: Optional[FileProcessor] = None

def get_file_processor() -> FileProcessor:
    """Get the global file processor instance"""
    global _file_processor
    if _file_processor is None:
        _file_processor = FileProcessor()
    return _file_processor