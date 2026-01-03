'use client';

import React, { useEffect, useRef, useState } from 'react';

interface DrawioEditorProps {
    xml: string | null;
}

const DrawioEditor: React.FC<DrawioEditorProps> = ({ xml }) => {
    const iframeRef = useRef<HTMLIFrameElement>(null);
    const [isReady, setIsReady] = useState(false);

    useEffect(() => {
        const handleMessage = (event: MessageEvent) => {
            if (event.data === 'ready') {
                setIsReady(true);
            }
        };

        window.addEventListener('message', handleMessage);
        return () => window.removeEventListener('message', handleMessage);
    }, []);

    useEffect(() => {
        if (xml && isReady && iframeRef.current) {
            iframeRef.current.contentWindow?.postMessage(
                JSON.stringify({
                    action: 'load',
                    xml: xml,
                    autosave: 1,
                }),
                '*'
            );
        }
    }, [xml, isReady]);

    return (
        <div className="w-full h-full rounded-xl overflow-hidden border border-white/20 shadow-2xl bg-white/5 backdrop-blur-sm">
            <iframe
                ref={iframeRef}
                src="https://embed.diagrams.net/?embed=1&ui=min&spin=1&modified=unsavedChanges&proto=json"
                className="w-full h-full border-none"
                title="Draw.io Editor"
            />
        </div>
    );
};

export default DrawioEditor;
