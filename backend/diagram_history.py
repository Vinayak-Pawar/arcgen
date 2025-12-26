"""
Diagram History and Version Control System
Inspired by next-ai-draw-io's comprehensive history management
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import hashlib


class DiagramVersion(BaseModel):
    """Represents a single version of a diagram"""
    id: str
    timestamp: datetime
    prompt: str
    xml_content: str
    provider: str
    model: str
    metadata: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "prompt": self.prompt,
            "xml_content": self.xml_content,
            "provider": self.provider,
            "model": self.model,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiagramVersion':
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            prompt=data["prompt"],
            xml_content=data["xml_content"],
            provider=data["provider"],
            model=data["model"],
            metadata=data.get("metadata", {})
        )


class DiagramHistory(BaseModel):
    """Represents the complete history of a diagram"""
    diagram_id: str
    created_at: datetime
    updated_at: datetime
    versions: List[DiagramVersion] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diagram_id": self.diagram_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "versions": [v.to_dict() for v in self.versions]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiagramHistory':
        return cls(
            diagram_id=data["diagram_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            versions=[DiagramVersion.from_dict(v) for v in data["versions"]]
        )

    def add_version(self, prompt: str, xml_content: str, provider: str, model: str, metadata: Dict[str, Any] = None) -> DiagramVersion:
        """Add a new version to this diagram"""
        version_id = str(uuid.uuid4())
        version = DiagramVersion(
            id=version_id,
            timestamp=datetime.now(),
            prompt=prompt,
            xml_content=xml_content,
            provider=provider,
            model=model,
            metadata=metadata or {}
        )

        self.versions.append(version)
        self.updated_at = datetime.now()

        # Keep only the last 50 versions to prevent unlimited growth
        if len(self.versions) > 50:
            self.versions = self.versions[-50:]

        return version

    def get_version(self, version_id: str) -> Optional[DiagramVersion]:
        """Get a specific version by ID"""
        return next((v for v in self.versions if v.id == version_id), None)

    def get_latest_version(self) -> Optional[DiagramVersion]:
        """Get the most recent version"""
        return self.versions[-1] if self.versions else None


class DiagramHistoryManager:
    """Manages diagram history storage and retrieval"""

    def __init__(self, storage_dir: str = "diagram_history"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def _get_diagram_path(self, diagram_id: str) -> str:
        """Get the file path for a diagram"""
        return os.path.join(self.storage_dir, f"{diagram_id}.json")

    def create_diagram(self, prompt: str, xml_content: str, provider: str, model: str, metadata: Dict[str, Any] = None) -> str:
        """Create a new diagram with initial version"""
        diagram_id = str(uuid.uuid4())

        history = DiagramHistory(
            diagram_id=diagram_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add initial version
        history.add_version(prompt, xml_content, provider, model, metadata)

        # Save to disk
        self._save_diagram(history)

        return diagram_id

    def add_version(self, diagram_id: str, prompt: str, xml_content: str, provider: str, model: str, metadata: Dict[str, Any] = None) -> bool:
        """Add a new version to an existing diagram"""
        history = self._load_diagram(diagram_id)
        if not history:
            return False

        history.add_version(prompt, xml_content, provider, model, metadata)
        self._save_diagram(history)
        return True

    def get_history(self, diagram_id: str) -> Optional[DiagramHistory]:
        """Get the complete history for a diagram"""
        return self._load_diagram(diagram_id)

    def get_version(self, diagram_id: str, version_id: str) -> Optional[DiagramVersion]:
        """Get a specific version of a diagram"""
        history = self._load_diagram(diagram_id)
        if not history:
            return None
        return history.get_version(version_id)

    def list_diagrams(self) -> List[Dict[str, Any]]:
        """List all saved diagrams with metadata"""
        diagrams = []

        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                diagram_id = filename[:-5]  # Remove .json extension
                history = self._load_diagram(diagram_id)
                if history:
                    latest_version = history.get_latest_version()
                    diagrams.append({
                        "diagram_id": diagram_id,
                        "created_at": history.created_at.isoformat(),
                        "updated_at": history.updated_at.isoformat(),
                        "version_count": len(history.versions),
                        "latest_prompt": latest_version.prompt[:100] + "..." if latest_version and len(latest_version.prompt) > 100 else (latest_version.prompt if latest_version else ""),
                        "latest_provider": latest_version.provider if latest_version else "",
                        "latest_model": latest_version.model if latest_version else ""
                    })

        # Sort by updated_at descending
        diagrams.sort(key=lambda x: x["updated_at"], reverse=True)
        return diagrams

    def delete_diagram(self, diagram_id: str) -> bool:
        """Delete a diagram and all its versions"""
        diagram_path = self._get_diagram_path(diagram_id)
        if os.path.exists(diagram_path):
            os.remove(diagram_path)
            return True
        return False

    def _save_diagram(self, history: DiagramHistory) -> None:
        """Save diagram history to disk"""
        diagram_path = self._get_diagram_path(history.diagram_id)
        with open(diagram_path, 'w', encoding='utf-8') as f:
            json.dump(history.to_dict(), f, indent=2, ensure_ascii=False)

    def _load_diagram(self, diagram_id: str) -> Optional[DiagramHistory]:
        """Load diagram history from disk"""
        diagram_path = self._get_diagram_path(diagram_id)
        if not os.path.exists(diagram_path):
            return None

        try:
            with open(diagram_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return DiagramHistory.from_dict(data)
        except Exception:
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        total_diagrams = 0
        total_versions = 0
        total_size = 0

        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                total_diagrams += 1
                filepath = os.path.join(self.storage_dir, filename)
                total_size += os.path.getsize(filepath)

                # Count versions in this diagram
                history = self._load_diagram(filename[:-5])
                if history:
                    total_versions += len(history.versions)

        return {
            "total_diagrams": total_diagrams,
            "total_versions": total_versions,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "average_versions_per_diagram": round(total_versions / max(total_diagrams, 1), 1)
        }


# Global instance
_history_manager: Optional[DiagramHistoryManager] = None

def get_history_manager() -> DiagramHistoryManager:
    """Get the global diagram history manager"""
    global _history_manager
    if _history_manager is None:
        # Create storage directory in the backend folder
        storage_dir = os.path.join(os.path.dirname(__file__), "diagram_history")
        _history_manager = DiagramHistoryManager(storage_dir)
    return _history_manager