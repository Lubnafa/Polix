/**
 * AgentTimeline component for displaying LangGraph agent steps.
 */
import { useEffect, useState } from "react";
import "./AgentTimeline.css";

const AgentTimeline = ({ steps = [] }) => {
  const [expandedStep, setExpandedStep] = useState(null);

  const getStepIcon = (agentName) => {
    const icons = {
      policy_agent: "📋",
      audit_agent: "🔍",
      report_agent: "📊",
      rag_retriever: "🔎",
      human_approval: "👤",
    };
    return icons[agentName] || "⚙️";
  };

  const getStepStatusColor = (status) => {
    const colors = {
      completed: "#10b981",
      running: "#3b82f6",
      error: "#ef4444",
      pending: "#f59e0b",
      skipped: "#94a3b8",
    };
    return colors[status] || "#64748b";
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return "";
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="agent-timeline">
      <div className="timeline-header">
        <h3>Agent Workflow Timeline</h3>
        <p>{steps.length} step(s) executed</p>
      </div>

      {steps.length === 0 ? (
        <div className="timeline-empty">
          <p>No workflow steps available yet.</p>
          <p className="empty-subtitle">Start an audit to see the timeline.</p>
        </div>
      ) : (
        <div className="timeline-steps">
          {steps.map((step, index) => (
            <div
              key={step.step_id || index}
              className={`timeline-step timeline-step-${step.status}`}
            >
              <div className="step-connector" />
              <div className="step-icon" style={{ backgroundColor: `${getStepStatusColor(step.status)}20` }}>
                <span style={{ color: getStepStatusColor(step.status) }}>
                  {getStepIcon(step.agent_name)}
                </span>
              </div>
              <div className="step-content">
                <div className="step-header">
                  <h4 className="step-title">{step.agent_name || "Unknown Agent"}</h4>
                  <span
                    className="step-status"
                    style={{ color: getStepStatusColor(step.status) }}
                  >
                    {step.status}
                  </span>
                </div>
                {step.timestamp && (
                  <p className="step-timestamp">{formatTimestamp(step.timestamp)}</p>
                )}
                {step.result && (
                  <div className="step-result">
                    <button
                      className="step-toggle"
                      onClick={() =>
                        setExpandedStep(expandedStep === index ? null : index)
                      }
                    >
                      {expandedStep === index ? "Hide" : "Show"} Details
                    </button>
                    {expandedStep === index && (
                      <div className="step-details">
                        <pre>{JSON.stringify(step.result, null, 2)}</pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AgentTimeline;

