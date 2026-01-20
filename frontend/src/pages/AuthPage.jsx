import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { loginUser, signupUser } from '../api/api';
import { Lock, Mail, Loader2, ShieldCheck } from 'lucide-react';

const AuthPage = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            if (isLogin) {
                const data = await loginUser(email, password);
                localStorage.setItem('token', data.access_token);
                onLogin();
            } else {
                await signupUser(email, password);
                setIsLogin(true);
                setError('Account created! Please login.');
                setLoading(false);
                return;
            }
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'An error occurred. Make sure backend is running.');
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 relative overflow-hidden">
            {/* Background blobs */}
            <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-600 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-pulse"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-cyan-600 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-pulse delay-1000"></div>

            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass p-8 rounded-2xl shadow-2xl w-full max-w-md z-10 border border-slate-700/50"
            >
                <div className="flex justify-center mb-6">
                    <div className="p-3 bg-blue-500/20 rounded-full ring-1 ring-blue-500/50">
                        <ShieldCheck className="text-blue-400 w-10 h-10" />
                    </div>
                </div>
                <h2 className="text-3xl font-bold text-center mb-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400">
                    {isLogin ? 'Welcome Back' : 'Create Account'}
                </h2>
                <p className="text-slate-400 text-center mb-8 text-sm">
                    Ayushman Bharat Policy Intelligence System
                </p>

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="relative group">
                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors" size={20} />
                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full glass-input bg-slate-800/50 border border-slate-700 py-3 pl-10 pr-4 rounded-xl text-white placeholder-slate-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                            required
                        />
                    </div>
                    <div className="relative group">
                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors" size={20} />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full glass-input bg-slate-800/50 border border-slate-700 py-3 pl-10 pr-4 rounded-xl text-white placeholder-slate-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                            required
                        />
                    </div>

                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="text-red-400 text-sm text-center bg-red-950/30 py-2 rounded-lg border border-red-500/20"
                        >
                            {error}
                        </motion.div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-blue-900/20 transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        {loading ? <Loader2 className="animate-spin" /> : (isLogin ? 'Sign In' : 'Create Account')}
                    </button>
                </form>

                <div className="mt-8 text-center">
                    <button
                        onClick={() => { setIsLogin(!isLogin); setError(''); }}
                        className="text-slate-400 hover:text-white text-sm transition-colors flex items-center justify-center gap-2 mx-auto"
                    >
                        {isLogin ? "New here? Create an account" : "Have an account? Sign in"}
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default AuthPage;
