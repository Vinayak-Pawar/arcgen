'use client';

import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import axios from 'axios';

interface ChatProps {
    onXmlGenerated: (xml: string) => void;
}

const Chat: React.FC<ChatProps> = ({ onXmlGenerated }) => {
    const [prompt, setPrompt] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/generate', {
                prompt: prompt,
            });
            onXmlGenerated(response.data.xml);
        } catch (error) {
            console.error('Error generating diagram:', error);
            alert('Failed to generate diagram. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full p-4 bg-white/10 backdrop-blur-md rounded-xl border border-white/20 shadow-xl">
            <div className="flex-1 overflow-y-auto mb-4 space-y-4">
                <div className="bg-blue-500/20 p-3 rounded-lg border border-blue-500/30 text-blue-100">
                    <p className="font-semibold">Welcome to Arcgen!</p>
                    <p className="text-sm opacity-80">Describe your system architecture, and I'll generate a professional diagram for you.</p>
                </div>
                {/* Chat history could go here */}
            </div>

            <form onSubmit={handleSubmit} className="relative">
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe your system (e.g., 'A scalable AWS web app with ELB, 3 EC2 instances, and RDS')..."
                    className="w-full bg-black/20 border border-white/10 rounded-lg p-3 pr-12 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none h-24"
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit(e);
                        }
                    }}
                />
                <button
                    type="submit"
                    disabled={loading || !prompt.trim()}
                    className="absolute bottom-3 right-3 p-2 bg-blue-600 hover:bg-blue-500 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                </button>
            </form>
        </div>
    );
};

export default Chat;
