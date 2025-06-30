import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputText.trim() && !isLoading) {
      const userMessage = {
        id: Date.now(),
        text: inputText.trim(),
        timestamp: new Date().toLocaleTimeString(),
        sender: 'user'
      };
      
      setMessages(prev => [...prev, userMessage]);
      const currentQuery = inputText.trim();
      setInputText('');
      setIsLoading(true);

      // Add loading message
      const loadingMessage = {
        id: Date.now() + 1,
        text: 'Processing your query...',
        timestamp: new Date().toLocaleTimeString(),
        sender: 'assistant',
        isLoading: true
      };
      setMessages(prev => [...prev, loadingMessage]);

      try {
        // Make API call to your backend
        const response = await fetch('http://localhost:5001/api/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: currentQuery
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Remove loading message and add AI response
        setMessages(prev => {
          const withoutLoading = prev.filter(msg => !msg.isLoading);
          return [...withoutLoading, {
            id: Date.now() + 2,
            text: data.natural_response || 'I received your query but couldn\'t generate a response.',
            timestamp: new Date().toLocaleTimeString(),
            sender: 'assistant',
            sqlQuery: data.sql_query,
            additionalContext: data.additional_context,
            results: data.results
          }];
        });

      } catch (error) {
        console.error('Error calling API:', error);
        
        // Remove loading message and add error response
        setMessages(prev => {
          const withoutLoading = prev.filter(msg => !msg.isLoading);
          return [...withoutLoading, {
            id: Date.now() + 2,
            text: `Sorry, I encountered an error while processing your request: ${error.message}. Please make sure the API server is running on http://localhost:5001`,
            timestamp: new Date().toLocaleTimeString(),
            sender: 'assistant',
            isError: true
          }];
        });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>DB-AI Chat Interface.</h1>
        <p>Ask questions about the construction project Database</p>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <div className="welcome-content">
              <h2>Welcome to DB-AI!</h2>
              <p>Type your question below and press Enter to start chatting.</p>
              <div className="example-queries">
                <p><strong>Example queries:</strong></p>
                <ul>
                  <li>"Show all elements in the ground floor"</li>
                  <li>"How many smoke detectors are needed in total?"</li>
                  <li>"List all electrical elements in the basement"</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`message ${message.sender} ${message.isError ? 'error' : ''}`}>
              <div className="message-content">
                {message.isLoading ? (
                  <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <div className="message-text">{message.text}</div>
                  </div>
                ) : (
                  <>
                    <div className="message-text">
                      {message.sender === 'assistant' ? (
                        <div className="markdown-content">
                          <ReactMarkdown 
                            components={{
                              // Custom components for better styling
                              p: ({children}) => <p className="markdown-p">{children}</p>,
                              strong: ({children}) => <strong className="markdown-strong">{children}</strong>,
                              em: ({children}) => <em className="markdown-em">{children}</em>,
                              ul: ({children}) => <ul className="markdown-ul">{children}</ul>,
                              ol: ({children}) => <ol className="markdown-ol">{children}</ol>,
                              li: ({children}) => <li className="markdown-li">{children}</li>,
                              code: ({children}) => <code className="markdown-code">{children}</code>,
                              pre: ({children}) => <pre className="markdown-pre">{children}</pre>,
                              blockquote: ({children}) => <blockquote className="markdown-blockquote">{children}</blockquote>,
                              h1: ({children}) => <h1 className="markdown-h1">{children}</h1>,
                              h2: ({children}) => <h2 className="markdown-h2">{children}</h2>,
                              h3: ({children}) => <h3 className="markdown-h3">{children}</h3>,
                              h4: ({children}) => <h4 className="markdown-h4">{children}</h4>,
                              h5: ({children}) => <h5 className="markdown-h5">{children}</h5>,
                              h6: ({children}) => <h6 className="markdown-h6">{children}</h6>,
                            }}
                          >
                            {message.text}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        message.text
                      )}
                    </div>
                    {message.sender === 'assistant' && message.sqlQuery && (
                      <div className="technical-details">
                        <details>
                          <summary>Technical Details</summary>
                          <div className="technical-content">
                            <div className="sql-query">
                              <strong>SQL Query:</strong>
                              <pre>{message.sqlQuery}</pre>
                            </div>
                            {message.additionalContext && (
                              <div className="additional-context">
                                <strong>Additional Context:</strong>
                                <p>{message.additionalContext}</p>
                              </div>
                            )}
                            {message.results && message.results.length > 0 && (
                              <div className="results-count">
                                <strong>Results:</strong> {message.results.length} rows returned
                              </div>
                            )}
                          </div>
                        </details>
                      </div>
                    )}
                  </>
                )}
                <div className="message-timestamp">{message.timestamp}</div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSendMessage} className="chat-input-form">
          <div className="input-wrapper">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              className="chat-input"
              rows="1"
              maxLength="1000"
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={!inputText.trim() || isLoading}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22,2 15,22 11,13 2,9 22,2"></polygon>
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
