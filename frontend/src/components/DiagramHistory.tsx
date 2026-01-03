"use client";

import React, { useState, useEffect } from 'react';
import { History, Clock, Trash2, Download, Eye, ChevronDown, ChevronUp } from 'lucide-react';

interface DiagramVersion {
    id: string;
    timestamp: string;
    prompt: string;
    provider: string;
    model: string;
    metadata: Record<string, any>;
}

interface DiagramHistoryProps {
    isOpen: boolean;
    onClose: () => void;
    onLoadVersion: (xmlContent: string) => void;
    currentDiagramId?: string;
}

const DiagramHistory: React.FC<DiagramHistoryProps> = ({
    isOpen,
    onClose,
    onLoadVersion,
    currentDiagramId
}) => {
    const [diagrams, setDiagrams] = useState<any[]>([]);
    const [selectedDiagram, setSelectedDiagram] = useState<any>(null);
    const [versions, setVersions] = useState<DiagramVersion[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen) {
            loadDiagrams();
        }
    }, [isOpen]);

    const loadDiagrams = async () => {
        try {
            const response = await fetch('http://localhost:8000/history/list');
            const data = await response.json();
            setDiagrams(data.diagrams || []);
        } catch (error) {
            console.error('Failed to load diagrams:', error);
        }
    };

    const loadDiagramVersions = async (diagramId: string) => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/history/${diagramId}`);
            const data = await response.json();
            setVersions(data.versions || []);
            setSelectedDiagram(diagrams.find(d => d.diagram_id === diagramId));
        } catch (error) {
            console.error('Failed to load diagram versions:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadVersion = async (diagramId: string, versionId: string) => {
        try {
            const response = await fetch(`http://localhost:8000/history/${diagramId}/${versionId}`);
            const data = await response.json();
            onLoadVersion(data.xml_content);
            onClose();
        } catch (error) {
            console.error('Failed to load version:', error);
        }
    };

    const deleteDiagram = async (diagramId: string) => {
        if (!confirm('Are you sure you want to delete this diagram and all its versions?')) {
            return;
        }

        try {
            await fetch(`http://localhost:8000/history/${diagramId}`, {
                method: 'DELETE'
            });
            loadDiagrams();
            if (selectedDiagram?.diagram_id === diagramId) {
                setSelectedDiagram(null);
                setVersions([]);
            }
        } catch (error) {
            console.error('Failed to delete diagram:', error);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
            <div className="bg-zinc-800 border border-white/10 rounded-xl shadow-2xl w-full max-w-4xl h-[80vh] flex flex-col">
                <div className="flex items-center justify-between p-6 border-b border-white/10">
                    <div className="flex items-center gap-2">
                        <History className="w-5 h-5 text-blue-400" />
                        <h2 className="text-xl font-bold text-white">Diagram History</h2>
                    </div>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-white"
                    >
                        ✕
                    </button>
                </div>

                <div className="flex-1 flex overflow-hidden">
                    {/* Diagrams List */}
                    <div className="w-1/3 border-r border-white/10 p-4 overflow-y-auto">
                        <h3 className="text-sm font-medium text-gray-300 mb-3">Saved Diagrams</h3>
                        {diagrams.length === 0 ? (
                            <p className="text-gray-500 text-sm">No saved diagrams yet</p>
                        ) : (
                            <div className="space-y-2">
                                {diagrams.map((diagram) => (
                                    <div
                                        key={diagram.diagram_id}
                                        className={`p-3 rounded-lg cursor-pointer transition-colors ${
                                            selectedDiagram?.diagram_id === diagram.diagram_id
                                                ? 'bg-blue-600/20 border border-blue-500/50'
                                                : 'bg-zinc-700/50 hover:bg-zinc-700'
                                        }`}
                                        onClick={() => loadDiagramVersions(diagram.diagram_id)}
                                    >
                                        <div className="text-sm font-medium text-white truncate">
                                            {diagram.latest_prompt}
                                        </div>
                                        <div className="text-xs text-gray-400 mt-1">
                                            {diagram.versions_count} versions • {diagram.latest_provider}
                                        </div>
                                        <div className="text-xs text-gray-500">
                                            {new Date(diagram.updated_at).toLocaleDateString()}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Versions List */}
                    <div className="flex-1 p-4 overflow-y-auto">
                        {selectedDiagram ? (
                            <>
                                <div className="flex items-center justify-between mb-4">
                                    <h3 className="text-sm font-medium text-gray-300">
                                        Versions for "{selectedDiagram.latest_prompt.substring(0, 50)}..."
                                    </h3>
                                    <button
                                        onClick={() => deleteDiagram(selectedDiagram.diagram_id)}
                                        className="text-red-400 hover:text-red-300 p-1"
                                        title="Delete diagram"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>

                                {loading ? (
                                    <div className="text-center text-gray-400">Loading versions...</div>
                                ) : (
                                    <div className="space-y-3">
                                        {versions.map((version, index) => (
                                            <div
                                                key={version.id}
                                                className="bg-zinc-700/50 rounded-lg p-3"
                                            >
                                                <div className="flex items-start justify-between">
                                                    <div className="flex-1">
                                                        <div className="flex items-center gap-2 mb-2">
                                                            <span className="text-xs bg-blue-600/20 text-blue-300 px-2 py-1 rounded">
                                                                v{versions.length - index}
                                                            </span>
                                                            <span className="text-xs text-gray-400">
                                                                {version.provider} • {version.model}
                                                            </span>
                                                        </div>
                                                        <p className="text-sm text-gray-300 mb-2">
                                                            {version.prompt}
                                                        </p>
                                                        <div className="flex items-center gap-1 text-xs text-gray-500">
                                                            <Clock className="w-3 h-3" />
                                                            {new Date(version.timestamp).toLocaleString()}
                                                        </div>
                                                    </div>
                                                    <button
                                                        onClick={() => loadVersion(selectedDiagram.diagram_id, version.id)}
                                                        className="ml-3 bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded text-sm transition-colors"
                                                    >
                                                        Load
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </>
                        ) : (
                            <div className="text-center text-gray-500 mt-20">
                                <History className="w-12 h-12 mx-auto mb-4 opacity-50" />
                                <p>Select a diagram to view its versions</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DiagramHistory;
