"use client";

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatPanelProps {
    onSendMessage: (message: string) => Promise<void>;
    messages: Message[];
    isLoading: boolean;
}

export default function ChatPanel({ onSendMessage, messages, isLoading }: ChatPanelProps) {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const message = input;
        setInput('');
        await onSendMessage(message);
    };

    return (
        <div className="flex flex-col h-full glass-panel relative overflow-hidden">
            {/* Chat Header */}
            <div className="p-4 border-b border-white/5 flex items-center gap-2 bg-white/5 backdrop-blur-md">
                <div className="p-2 bg-brand-600/20 rounded-lg">
                    <Sparkles size={18} className="text-brand-500" />
                </div>
                <div>
                    <h2 className="font-semibold text-sm text-white">Arcgen AI</h2>
                    <p className="text-xs text-gray-400">System Architect</p>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6 scroll-smooth">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-50 animate-fade-in">
                        <div className="w-20 h-20 bg-white/5 rounded-2xl flex items-center justify-center mb-2 overflow-hidden shadow-2xl">
                            <img src="/arcgen-logo.png" alt="Arcgen" className="w-full h-full object-cover opacity-80" />
                        </div>
                        <p className="text-sm text-gray-400 max-w-[200px]">
                            Describe a system architecture to generate a diagram.
                        </p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex items-start gap-3 animate-slide-up ${msg.role === 'user' ? 'flex-row-reverse' : ''
                            }`}
                    >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 overflow-hidden ${msg.role === 'user' ? 'bg-brand-600' : 'bg-transparent'
                            }`}>
                            {msg.role === 'user' ? (
                                <User size={14} />
                            ) : (
                                <img src="/arcgen-logo.png" alt="Arcgen" className="w-full h-full object-cover" />
                            )}
                        </div>

                        <div
                            className={`p-3 rounded-2xl max-w-[85%] text-sm leading-relaxed shadow-lg ${msg.role === 'user'
                                ? 'bg-brand-600 text-white rounded-tr-none'
                                : 'bg-zinc-800/80 text-gray-200 border border-white/5 rounded-tl-none'
                                }`}
                        >
                            <p className="whitespace-pre-wrap">{msg.content}</p>
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex items-start gap-3 animate-fade-in">
                        <div className="w-8 h-8 rounded-full bg-transparent flex items-center justify-center shrink-0 overflow-hidden">
                            <img src="/arcgen-logo.png" alt="Arcgen" className="w-full h-full object-cover" />
                        </div>
                        <div className="bg-zinc-800/50 p-3 rounded-2xl rounded-tl-none border border-white/5 flex items-center gap-3">
                            <div className="flex gap-1">
                                <div className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <div className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <div className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                            <span className="text-xs text-gray-400 font-medium">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-white/5 bg-black/20 backdrop-blur-md">
                <form onSubmit={handleSubmit} className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Describe your system..."
                        className="w-full bg-zinc-900/50 border border-white/10 rounded-xl pl-4 pr-12 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500/50 transition-all"
                        disabled={isLoading}
                        suppressHydrationWarning
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 bg-brand-600 text-white rounded-lg hover:bg-brand-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-95"
                    >
                        <Send size={16} />
                    </button>
                </form>
            </div>
        </div>
    );
}
