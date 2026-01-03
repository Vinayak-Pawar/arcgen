'use client';

import React, { useState } from 'react';
import DrawioEditor from '@/components/DrawioEditor';
import Chat from '@/components/Chat';

export default function Home() {
  const [xml, setXml] = useState<string | null>(null);

  return (
    <main className="flex h-screen w-full bg-gradient-to-br from-gray-900 via-slate-800 to-black text-white overflow-hidden">
      {/* Left Sidebar: Chat */}
      <div className="w-1/3 max-w-md p-6 flex flex-col z-10">
        <h1 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
          Arcgen
        </h1>
        <Chat onXmlGenerated={setXml} />
      </div>

      {/* Right Area: Diagram Editor */}
      <div className="flex-1 p-6 pl-0 relative">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>
        <DrawioEditor xml={xml} />
      </div>
    </main>
  );
}
