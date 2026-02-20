"use client";

import { useState, useEffect, useRef } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [diagramXml, setDiagramXml] = useState("");
  const [error, setError] = useState("");
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Initialize draw.io with empty diagram
  useEffect(() => {
    const initDiagram = () => {
      if (iframeRef.current) {
        const emptyDiagram = `<mxfile host="arcgen" agent="arcgen" version="1.0">
  <diagram name="Architecture">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>`;
        
        const iframe = iframeRef.current;
        const encodedXml = encodeURIComponent(emptyDiagram);
        iframe.src = `https://embed.diagrams.net/?embed=1&proto=json&spin=1&configure=1&noSaveBtn=1&xml=${encodedXml}`;
      }
    };

    // Small delay to ensure iframe is ready
    const timer = setTimeout(initDiagram, 100);
    return () => clearTimeout(timer);
  }, []);

  // Load diagram when XML changes
  useEffect(() => {
    if (diagramXml && iframeRef.current) {
      const iframe = iframeRef.current;
      const encodedXml = encodeURIComponent(diagramXml);
      iframe.src = `https://embed.diagrams.net/?embed=1&proto=json&spin=1&configure=1&noSaveBtn=1&xml=${encodedXml}`;
    }
  }, [diagramXml]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError("Please enter a description");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Create abort controller with 90 second timeout (NVIDIA can take 30-40s)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 90000);

      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.xml) {
        // Wrap the XML in full draw.io format
        const fullXml = `<mxfile host="arcgen" agent="arcgen" version="1.0">
  <diagram name="Architecture">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        ${data.xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>`;
        
        setDiagramXml(fullXml);
      } else {
        setError("No diagram generated. Please try again.");
      }
    } catch (err) {
      console.error("Error generating diagram:", err);
      if (err instanceof Error && err.name === 'AbortError') {
        setError("Request timed out after 90 seconds. The AI service might be slow. Please try again.");
      } else {
        setError(err instanceof Error ? err.message : "Failed to generate diagram");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Draw.io Editor Panel */}
      <div className="flex-1 bg-white border-r border-gray-200">
        <div className="h-full flex flex-col">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-4 shadow-lg">
            <h2 className="text-xl font-bold">Diagram Editor</h2>
            <p className="text-blue-100 text-sm">Powered by draw.io</p>
          </div>
          <div className="flex-1 relative">
            <iframe
              ref={iframeRef}
              className="w-full h-full border-0"
              title="Draw.io Diagram Editor"
            />
          </div>
        </div>
      </div>

      {/* Chat Panel */}
      <div className="w-[400px] bg-white flex flex-col shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-6 shadow-lg">
          <h1 className="text-2xl font-bold mb-2">🎨 Arcgen</h1>
          <p className="text-indigo-100 text-sm">
            Natural Language to System Architecture
          </p>
        </div>

        {/* Chat Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="space-y-4">
            {/* Welcome Message */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-100">
              <h3 className="font-semibold text-gray-800 mb-2">
                👋 Welcome to Arcgen!
              </h3>
              <p className="text-sm text-gray-600">
                Describe your system architecture in plain English, and I&apos;ll
                generate a professional diagram for you.
              </p>
            </div>

            {/* Example Prompts */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h4 className="font-semibold text-gray-700 text-sm mb-2">
                💡 Try these examples:
              </h4>
              <ul className="text-xs text-gray-600 space-y-2">
                <li className="flex items-start">
                  <span className="text-indigo-500 mr-2">•</span>
                  <button
                    onClick={() => setPrompt("Create a microservices architecture with API Gateway, auth service, user service, and PostgreSQL")}
                    className="text-left hover:text-indigo-600 transition-colors"
                  >
                    Microservices with API Gateway
                  </button>
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-500 mr-2">•</span>
                  <button
                    onClick={() => setPrompt("AWS architecture with EC2, S3, RDS, and Load Balancer")}
                    className="text-left hover:text-indigo-600 transition-colors"
                  >
                    AWS cloud architecture
                  </button>
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-500 mr-2">•</span>
                  <button
                    onClick={() => setPrompt("User login flow with authentication and database")}
                    className="text-left hover:text-indigo-600 transition-colors"
                  >
                    User authentication flow
                  </button>
                </li>
              </ul>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-600">❌ {error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Input Form */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <form onSubmit={handleGenerate} className="space-y-3">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your system architecture..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none text-sm"
              rows={4}
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-all ${
                loading
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              }`}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Generating... (may take 30-60s)
                </span>
              ) : (
                "✨ Generate Diagram"
              )}
            </button>
          </form>
          
          {/* Footer Info */}
          <div className="mt-3 text-center">
            <p className="text-xs text-gray-500">
              Powered by AI • Built with ❤️
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
