"use client";

import { useState, useEffect } from 'react';
import { Settings, CheckCircle, XCircle, TestTube, ExternalLink, Key, Cpu } from 'lucide-react';

interface LLMProvider {
    name: string;
    default_model: string;
    requires_api_key: boolean;
    api_key_env: string;
    description: string;
}

interface ProviderData {
    providers: Record<string, LLMProvider>;
    current_provider: string;
    current_model: string;
}

interface TestResult {
    success: boolean;
    provider: string;
    model: string;
    message: string;
    sample_output?: string;
    error?: string;
}

export default function LLMSettings() {
    const [providerData, setProviderData] = useState<ProviderData | null>(null);
    const [testResult, setTestResult] = useState<TestResult | null>(null);
    const [isTesting, setIsTesting] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [showEnvInstructions, setShowEnvInstructions] = useState(false);

    useEffect(() => {
        fetchProviders();
    }, []);

    const fetchProviders = async () => {
        try {
            const response = await fetch('http://localhost:8000/providers');
            const data = await response.json();
            setProviderData(data);
        } catch (error) {
            console.error('Failed to fetch providers:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const testProvider = async () => {
        setIsTesting(true);
        setTestResult(null);

        try {
            const response = await fetch('http://localhost:8000/test-provider', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            });
            const result = await response.json();
            setTestResult(result);
        } catch (error) {
            setTestResult({
                success: false,
                provider: providerData?.current_provider || 'unknown',
                model: providerData?.current_model || 'unknown',
                message: 'Connection failed',
                error: 'Cannot connect to backend server'
            });
        } finally {
            setIsTesting(false);
        }
    };

    const getProviderIcon = (providerName: string) => {
        const icons: Record<string, React.ReactElement> = {
            openai: <div className="w-6 h-6 bg-green-600 rounded flex items-center justify-center text-xs font-bold text-white">O</div>,
            anthropic: <div className="w-6 h-6 bg-orange-600 rounded flex items-center justify-center text-xs font-bold text-white">A</div>,
            google: <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center text-xs font-bold text-white">G</div>,
            nvidia: <div className="w-6 h-6 bg-green-700 rounded flex items-center justify-center text-xs font-bold text-white">N</div>,
            ollama: <div className="w-6 h-6 bg-purple-600 rounded flex items-center justify-center text-xs font-bold text-white">L</div>,
            custom: <div className="w-6 h-6 bg-gray-600 rounded flex items-center justify-center text-xs font-bold text-white">C</div>,
        };
        return icons[providerName] || <Cpu size={20} className="text-gray-400" />;
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-500"></div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-brand-600/20 rounded-lg">
                    <Settings size={24} className="text-brand-500" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-white">LLM Configuration</h1>
                    <p className="text-gray-400">Choose your AI provider and manage API keys</p>
                </div>
            </div>

            {/* Current Configuration */}
            {providerData && (
                <div className="glass-panel p-6 rounded-xl">
                    <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <CheckCircle size={20} className="text-green-500" />
                        Current Configuration
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-white/5 p-4 rounded-lg">
                            <div className="text-sm text-gray-400">Provider</div>
                            <div className="text-lg font-semibold text-white capitalize flex items-center gap-2">
                                {getProviderIcon(providerData.current_provider)}
                                {providerData.current_provider}
                            </div>
                        </div>
                        <div className="bg-white/5 p-4 rounded-lg">
                            <div className="text-sm text-gray-400">Model</div>
                            <div className="text-lg font-semibold text-white">{providerData.current_model}</div>
                        </div>
                        <div className="bg-white/5 p-4 rounded-lg">
                            <div className="text-sm text-gray-400">Status</div>
                            <div className="flex items-center gap-2">
                                {testResult ? (
                                    testResult.success ? (
                                        <><CheckCircle size={16} className="text-green-500" /> Working</>
                                    ) : (
                                        <><XCircle size={16} className="text-red-500" /> Failed</>
                                    )
                                ) : (
                                    <span className="text-gray-400">Not tested</span>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Test Button */}
                    <div className="mt-6 flex gap-3">
                        <button
                            onClick={testProvider}
                            disabled={isTesting}
                            className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 rounded-lg transition-colors"
                        >
                            <TestTube size={16} />
                            {isTesting ? 'Testing...' : 'Test Configuration'}
                        </button>
                        <button
                            onClick={() => setShowEnvInstructions(!showEnvInstructions)}
                            className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
                        >
                            <Key size={16} />
                            Setup Instructions
                        </button>
                    </div>

                    {/* Test Results */}
                    {testResult && (
                        <div className={`mt-4 p-4 rounded-lg ${testResult.success ? 'bg-green-900/20 border border-green-700' : 'bg-red-900/20 border border-red-700'}`}>
                            <div className="flex items-center gap-2 mb-2">
                                {testResult.success ? (
                                    <CheckCircle size={16} className="text-green-500" />
                                ) : (
                                    <XCircle size={16} className="text-red-500" />
                                )}
                                <span className="font-semibold text-white">
                                    {testResult.success ? 'Success' : 'Failed'}
                                </span>
                            </div>
                            <p className="text-gray-300">{testResult.message}</p>
                            {testResult.error && (
                                <p className="text-red-400 mt-2 text-sm">{testResult.error}</p>
                            )}
                        </div>
                    )}
                </div>
            )}

            {/* Environment Setup Instructions */}
            {showEnvInstructions && (
                <div className="glass-panel p-6 rounded-xl">
                    <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Key size={20} className="text-brand-500" />
                        Environment Setup (Google Colab Style)
                    </h2>

                    <div className="space-y-4">
                        <div className="bg-yellow-900/20 border border-yellow-700 p-4 rounded-lg">
                            <p className="text-yellow-200 font-semibold mb-2">🔑 Google Colab Style Configuration</p>
                            <p className="text-gray-300 text-sm">
                                Just like Google Colab's <code>userdata.get('secretName')</code>, set environment variables with your API keys.
                            </p>
                        </div>

                        <div className="bg-white/5 p-4 rounded-lg font-mono text-sm">
                            <p className="text-gray-400 mb-2"># Copy the example file:</p>
                            <p className="text-white">cp env-example.txt .env</p>

                            <p className="text-gray-400 mt-4 mb-2"># Edit .env and set your provider:</p>
                            <div className="space-y-1">
                                <p className="text-green-400"># For OpenAI:</p>
                                <p className="text-white">ARCGEN_LLM_PROVIDER=openai</p>
                                <p className="text-white">OPENAI_API_KEY=sk-your-key-here</p>

                                <p className="text-green-400 mt-3"># For Anthropic:</p>
                                <p className="text-white">ARCGEN_LLM_PROVIDER=anthropic</p>
                                <p className="text-white">ANTHROPIC_API_KEY=sk-ant-your-key-here</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {providerData && Object.entries(providerData.providers).map(([key, provider]) => (
                                <div key={key} className="bg-white/5 p-4 rounded-lg">
                                    <div className="flex items-center gap-2 mb-2">
                                        {getProviderIcon(key)}
                                        <span className="font-semibold text-white capitalize">{key}</span>
                                        {providerData.current_provider === key && (
                                            <span className="text-xs bg-brand-600 px-2 py-1 rounded">Active</span>
                                        )}
                                    </div>
                                    <p className="text-gray-400 text-sm mb-2">{provider.description}</p>
                                    <div className="text-xs text-gray-500">
                                        Model: {provider.default_model}
                                    </div>
                                    {provider.requires_api_key && (
                                        <div className="text-xs text-gray-500 mt-1">
                                            Key: {provider.api_key_env}
                                        </div>
                                    )}
                                    {!provider.requires_api_key && (
                                        <div className="text-xs text-green-400 mt-1">
                                            No API key required
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Available Providers */}
            <div className="glass-panel p-6 rounded-xl">
                <h2 className="text-lg font-semibold text-white mb-4">Available Providers</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {providerData && Object.entries(providerData.providers).map(([key, provider]) => (
                        <div key={key} className={`p-4 rounded-lg border transition-colors ${
                            providerData.current_provider === key
                                ? 'bg-brand-600/20 border-brand-500'
                                : 'bg-white/5 border-white/10 hover:bg-white/10'
                        }`}>
                            <div className="flex items-center gap-3 mb-3">
                                {getProviderIcon(key)}
                                <div>
                                    <h3 className="font-semibold text-white capitalize">{key}</h3>
                                    <p className="text-xs text-gray-400">{provider.default_model}</p>
                                </div>
                            </div>
                            <p className="text-gray-300 text-sm mb-3">{provider.description}</p>

                            <div className="flex items-center justify-between text-xs">
                                <span className={provider.requires_api_key ? 'text-orange-400' : 'text-green-400'}>
                                    {provider.requires_api_key ? 'API Key Required' : 'No API Key'}
                                </span>
                                {providerData.current_provider === key && (
                                    <span className="bg-brand-600 text-white px-2 py-1 rounded">Current</span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Footer */}
            <div className="text-center text-gray-400 text-sm">
                <p>🔄 Restart the backend server after changing environment variables</p>
                <p className="mt-1">📚 Check <code>env-example.txt</code> for detailed setup instructions</p>
            </div>
        </div>
    );
}
