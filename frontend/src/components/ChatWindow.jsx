/**
 * ChatWindow component for interacting with Polix.
 */
import { useState, useRef, useEffect } from "react";
import "./ChatWindow.css";

const ChatWindow = ({ onSendMessage }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "system",
      content: "Welcome to Polix! I can help you with compliance audits and policy analysis.",
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      // Call the onSendMessage callback if provided
      if (onSendMessage) {
        const response = await onSendMessage(inputValue);
        
        const botMessage = {
          id: Date.now() + 1,
          type: "assistant",
          content: response.message || response.answer || "I received your message.",
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, botMessage]);
      } else {
        // Default response if no callback provided
        setTimeout(() => {
          const botMessage = {
            id: Date.now() + 1,
            type: "assistant",
            content: "Thank you for your message. This is a placeholder response.",
            timestamp: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, botMessage]);
          setIsLoading(false);
        }, 1000);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = {
        id: Date.now() + 1,
        type: "error",
        content: "Sorry, an error occurred. Please try again.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`chat-message chat-message-${message.type}`}
          >
            <div className="message-content">{message.content}</div>
            <div className="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="chat-message chat-message-system">
            <div className="message-content">
              <span className="loading-dots">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <textarea
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          rows={3}
          disabled={isLoading}
        />
        <button
          className="chat-send-button"
          onClick={handleSend}
          disabled={!inputValue.trim() || isLoading}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;

