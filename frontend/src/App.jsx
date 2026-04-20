import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, CheckCircle, AlertTriangle, BookOpen, ChevronDown, ChevronUp, HelpCircle } from 'lucide-react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    const userMsg = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    const currentQuery = query;
    setQuery('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/query', {
        query: currentQuery
      });

      const aiMsg = {
        role: 'ai',
        answer: response.data.answer,
        confidence: response.data.confidence,
        sources: response.data.sources,
        showSources: false
      };
      
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prev => [...prev, { 
        role: 'ai', 
        answer: "I encountered an error connecting to the server. Please make sure the Flask backend is running with `python server.py`.",
        error: true 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleSources = (index) => {
    setMessages(prev => prev.map((msg, i) => 
      i === index ? { ...msg, showSources: !msg.showSources } : msg
    ));
  };

  return (
    <div className="app-container">
      {/* Header Bar */}
      <header className="header">
        <div className="header-left">
          <div className="header-logo">A</div>
          <span className="header-title">Academic City AI</span>
        </div>
        <div className="header-right">
          <HelpCircle size={22} style={{ cursor: 'pointer', opacity: 0.8 }} />
        </div>
      </header>

      {/* Main Chat Feed */}
      <main className="chat-area">
        {messages.length === 0 && (
          <div className="welcome-card">
            <h1 style={{ fontSize: '1.8rem', color: '#C41E3A', marginBottom: '16px' }}>🇬🇭 Ghana Data Assistant</h1>
            <p style={{ color: '#546e7a', fontSize: '1.1rem' }}>
              Ask me anything about the 2025 Budget Statement or the Ghana Election results.
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role === 'user' ? 'user-message' : 'ai-message'}`}>
            {msg.role === 'user' ? (
              <div className="user-content">{msg.content}</div>
            ) : (
              <div className="ai-content">
                {/* The Synthesized Answer (The most important part) */}
                <div className="answer-text">
                  {msg.answer}
                </div>
                
                {!msg.error && msg.confidence && (
                  <>
                    {/* Metadata Row: Confidence and Source Count */}
                    <div className="meta-row">
                      <div className={`badge badge-${msg.confidence.level.toLowerCase()}`}>
                        {msg.confidence.level === 'HIGH' ? <CheckCircle size={14} /> : <AlertTriangle size={14} />}
                        {msg.confidence.level} Confidence
                      </div>
                      
                      <div className="source-tag">
                        <BookOpen size={16} />
                        {msg.sources?.length || 0} Sources
                      </div>

                      <button 
                        className="sources-toggle" 
                        onClick={() => toggleSources(index)}
                      >
                        {msg.showSources ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                        Sources
                      </button>
                    </div>

                    {/* Collapsible Source List */}
                    {msg.showSources && (
                      <div className="sources-grid">
                        {msg.sources.map((src, sIdx) => (
                          <div key={sIdx} className="source-card">
                            <div className="source-label">Source: {src.source} | Score: {src.score}</div>
                            <div>"{src.text}"</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        ))}
        
        {/* Loading Animation */}
        {isLoading && (
          <div className="message ai-message">
            <div className="typing-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </main>

      {/* Persistent Input Bar */}
      <div className="input-area">
        <form className="input-container" onSubmit={handleSend}>
          <input 
            type="text" 
            placeholder="Type your question about budget or elections..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="send-button" disabled={isLoading || !query.trim()}>
            SEND <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
