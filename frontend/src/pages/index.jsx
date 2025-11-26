/**
 * Landing page for Polix.
 */
import { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import "../pages/index.css";

const Index = () => {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (message) => {
    try {
      // Call backend query endpoint
      const response = await fetch("http://localhost:8000/query/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: message,
          top_k: 5,
        }),
      });

      if (!response.ok) {
        throw new Error("Query failed");
      }

      const data = await response.json();
      return {
        message: data.answer || "Response received",
        data: data,
      };
    } catch (error) {
      console.error("Error querying backend:", error);
      return {
        message: "Sorry, I encountered an error. Please try again.",
        error: error.message,
      };
    }
  };

  return (
    <div className="index-page">
      <div className="page-header">
        <h1>Welcome to Polix</h1>
        <p>AI-Powered Compliance Audit System</p>
      </div>

      <div className="page-content">
        <div className="chat-section">
          <ChatWindow onSendMessage={handleSendMessage} />
        </div>

        <div className="info-section">
          <div className="info-card">
            <h3>Features</h3>
            <ul>
              <li>📋 Policy Analysis</li>
              <li>🔍 Compliance Auditing</li>
              <li>📊 Automated Reporting</li>
              <li>🤖 Agent-Based Workflows</li>
            </ul>
          </div>

          <div className="info-card">
            <h3>Getting Started</h3>
            <ol>
              <li>Upload policy documents</li>
              <li>Ask questions about compliance</li>
              <li>Run automated audits</li>
              <li>Review detailed reports</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;

