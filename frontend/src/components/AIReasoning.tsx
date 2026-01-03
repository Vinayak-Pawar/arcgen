"use client";

import React, { useState, useEffect } from 'react';
import { Brain, ChevronDown, ChevronUp, Clock } from 'lucide-react';

interface AIReasoningProps {
    isVisible: boolean;
    isStreaming: boolean;
    thinkingProcess?: string[];
    duration?: number;
    onToggle?: () => void;
}

const AIReasoning: React.FC<AIReasoningProps> = ({
    isVisible,
    isStreaming,
    thinkingProcess = [],
    duration,
    onToggle
}) => {
    const [isExpanded, setIsExpanded] = useState(true);

    if (!isVisible) return null;

    const toggleExpanded = () => {
        setIsExpanded(!isExpanded);
        onToggle?.();
    };

    return (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-4">
            <div
                className="flex items-center justify-between cursor-pointer"
                onClick={toggleExpanded}
            >
                <div className="flex items-center gap-2">
                    <Brain className={`w-4 h-4 ${isStreaming ? 'text-blue-500 animate-pulse' : 'text-blue-600'}`} />
                    <span className="text-sm font-medium text-blue-900 dark:text-blue-100">
                        AI Thinking Process
                    </span>
                    {isStreaming && (
                        <div className="flex items-center gap-1">
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        </div>
                    )}
                    {duration && (
                        <div className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400">
                            <Clock className="w-3 h-3" />
                            {(duration / 1000).toFixed(1)}s
                        </div>
                    )}
                </div>
                <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200">
                    {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </button>
            </div>

            {isExpanded && (
                <div className="mt-3 space-y-2">
                    {thinkingProcess.length > 0 ? (
                        thinkingProcess.map((step, index) => (
                            <div key={index} className="text-sm text-blue-800 dark:text-blue-200 bg-white/50 dark:bg-black/20 rounded p-2">
                                <span className="font-medium">Step {index + 1}:</span> {step}
                            </div>
                        ))
                    ) : isStreaming ? (
                        <div className="text-sm text-blue-600 dark:text-blue-400 italic">
                            AI is analyzing your request and generating the diagram...
                        </div>
                    ) : (
                        <div className="text-sm text-blue-600 dark:text-blue-400 italic">
                            No thinking process available
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default AIReasoning;
