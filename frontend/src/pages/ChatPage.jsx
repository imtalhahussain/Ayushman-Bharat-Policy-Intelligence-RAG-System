import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { askQuestion } from '../api/api';
import { Send, LogOut, Bot, User, Loader2, Sparkles, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';

const ChatPage = ({ onLogout }) => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am your Ayushman Bharat Policy assistant. How can I help you today?', sources: [] }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage, sources: [] }]);
        setLoading(true);

        try {
            const response = await askQuestion(userMessage);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.answer,
                sources: response.sources || []
            }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error connecting to the server.', sources: [] }]);
        }
        setLoading(false);
    };

    return (
        <div className="flex h-screen bg-slate-900 text-white overflow-hidden">
            {/* Sidebar - could be expandable, for now static width or hidden on mobile */}
            <div className="hidden md:flex flex-col w-64 bg-slate-950 border-r border-slate-800 p-4">
                <div className="flex items-center gap-2 mb-8 px-2">
                    <div className="p-2 bg-blue-600 rounded-lg">
                        <Sparkles className="w-5 h-5 text-white" />
                    </div>
                    <h1 className="font-bold text-lg bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400">
                        Policy Chat
                    </h1>
                </div>

                <div className="flex-1 overflow-y-auto">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 px-2">History</div>
                    {/* Placeholder for history */}
                    <div className="px-2 py-2 text-sm text-slate-400 hover:bg-slate-900 rounded cursor-pointer transition-colors truncate">
                        Current Session
                    </div>
                </div>

                <button
                    onClick={onLogout}
                    className="flex items-center gap-2 text-slate-400 hover:text-white p-2 rounded hover:bg-slate-900 transition-colors mt-auto"
                >
                    <LogOut size={18} />
                    <span>Sign Out</span>
                </button>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col h-full bg-slate-900 relative">
                {/* Header (Mobile only mainly) */}
                <div className="md:hidden flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950">
                    <span className="font-bold text-blue-400">Policy Chat</span>
                    <button onClick={onLogout}><LogOut size={18} className="text-slate-400" /></button>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth">
                    <AnimatePresence>
                        {messages.map((msg, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={clsx(
                                    "flex gap-4 max-w-4xl mx-auto",
                                    msg.role === 'user' ? "flex-row-reverse" : "flex-row"
                                )}
                            >
                                {/* Avatar */}
                                <div className={clsx(
                                    "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1",
                                    msg.role === 'user' ? "bg-blue-600" : "bg-cyan-600"
                                )}>
                                    {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                                </div>

                                {/* Bubble */}
                                <div className={clsx(
                                    "flex flex-col max-w-[80%] md:max-w-[70%]",
                                    msg.role === 'user' ? "items-end" : "items-start"
                                )}>
                                    <div className={clsx(
                                        "p-4 rounded-2xl shadow-md",
                                        msg.role === 'user'
                                            ? "bg-blue-600 text-white rounded-tr-sm"
                                            : "bg-slate-800 border border-slate-700 text-slate-200 rounded-tl-sm"
                                    )}>
                                        <div className="prose prose-invert prose-sm max-w-none">
                                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                                        </div>
                                    </div>

                                    {/* Sources */}
                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="mt-2 text-left w-full">
                                            <p className="text-xs text-slate-500 font-semibold mb-1 flex items-center gap-1">
                                                <Sparkles size={10} /> Sources:
                                            </p>
                                            <div className="flex flex-wrap gap-2">
                                                {msg.sources.map((src, i) => (
                                                    <div key={i} className="flex items-center gap-1 bg-slate-800/50 border border-slate-700 px-2 py-1 rounded text-xs text-cyan-400">
                                                        <FileText size={10} />
                                                        <span className="truncate max-w-[150px]">{typeof src === 'string' ? src : JSON.stringify(src)}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {loading && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex gap-4 max-w-4xl mx-auto"
                        >
                            <div className="w-8 h-8 rounded-full bg-cyan-600 flex items-center justify-center flex-shrink-0 mt-1">
                                <Bot size={16} />
                            </div>
                            <div className="bg-slate-800 border border-slate-700 rounded-2xl p-4 rounded-tl-sm flex items-center gap-2">
                                <Loader2 className="animate-spin text-cyan-400" size={18} />
                                <span className="text-slate-400 text-sm">Thinking...</span>
                            </div>
                        </motion.div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-slate-800/50 bg-slate-900/50 backdrop-blur-sm z-10 w-full mb-0">
                    <div className="max-w-4xl mx-auto relative group">
                        <form onSubmit={handleSend} className="relative">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask about Ayushman Bharat policy..."
                                className="w-full glass-input bg-slate-800 border-none py-4 pl-6 pr-14 rounded-full text-white placeholder-slate-500 focus:ring-2 focus:ring-blue-500 shadow-xl transition-all"
                                disabled={loading}
                            />
                            <button
                                type="submit"
                                disabled={!input.trim() || loading}
                                className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-full transition-all disabled:opacity-50 disabled:hover:bg-blue-600"
                            >
                                <Send size={18} />
                            </button>
                        </form>
                        <div className="text-center mt-2">
                            <p className="text-xs text-slate-600">AI can make mistakes. Check important info.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatPage;
