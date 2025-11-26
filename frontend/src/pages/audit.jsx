/**
 * Audit results page.
 */
import { useState, useEffect } from "react";
import ComplianceScoreCard from "../components/ComplianceScoreCard";
import AgentTimeline from "../components/AgentTimeline";
import "../pages/audit.css";

const Audit = () => {
  const [auditData, setAuditData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [policyDocument, setPolicyDocument] = useState("");

  const handleRunAudit = async () => {
    if (!query.trim()) {
      alert("Please enter an audit query");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/agent/audit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          policy_document: policyDocument || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error("Audit failed");
      }

      const data = await response.json();
      setAuditData(data);
    } catch (error) {
      console.error("Error running audit:", error);
      alert("Failed to run audit. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="audit-page">
      <div className="page-header">
        <h1>Compliance Audit</h1>
        <p>Run automated compliance audits using AI agents</p>
      </div>

      <div className="audit-content">
        <div className="audit-controls">
          <div className="control-group">
            <label htmlFor="audit-query">Audit Query</label>
            <textarea
              id="audit-query"
              className="control-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your audit query here..."
              rows={4}
            />
          </div>

          <div className="control-group">
            <label htmlFor="policy-document">Policy Document (Optional)</label>
            <textarea
              id="policy-document"
              className="control-input"
              value={policyDocument}
              onChange={(e) => setPolicyDocument(e.target.value)}
              placeholder="Paste policy document text here..."
              rows={6}
            />
          </div>

          <button
            className="run-audit-button"
            onClick={handleRunAudit}
            disabled={loading || !query.trim()}
          >
            {loading ? "Running Audit..." : "Run Audit"}
          </button>
        </div>

        {auditData && (
          <div className="audit-results">
            <div className="results-header">
              <h2>Audit Results</h2>
              <p>Workflow ID: {auditData.workflow_id}</p>
            </div>

            <div className="results-grid">
              <div className="results-section">
                <ComplianceScoreCard
                  score={auditData.compliance_score || 0}
                  title="Overall Compliance Score"
                />
              </div>

              <div className="results-section">
                <AgentTimeline steps={auditData.steps || []} />
              </div>
            </div>

            {auditData.final_report && (
              <div className="results-section report-section">
                <h3>Final Report</h3>
                <div className="report-content">
                  <pre>{auditData.final_report}</pre>
                </div>
              </div>
            )}
          </div>
        )}

        {!auditData && !loading && (
          <div className="audit-placeholder">
            <p>Enter an audit query and click "Run Audit" to start.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Audit;

