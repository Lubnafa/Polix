/**
 * ComplianceScoreCard component for displaying compliance scores.
 */
import "./ComplianceScoreCard.css";

const ComplianceScoreCard = ({ score, maxScore = 100, title = "Compliance Score" }) => {
  const percentage = (score / maxScore) * 100;
  
  const getScoreColor = () => {
    if (percentage >= 80) return "#10b981"; // green
    if (percentage >= 60) return "#f59e0b"; // yellow
    return "#ef4444"; // red
  };

  const getScoreLabel = () => {
    if (percentage >= 80) return "Compliant";
    if (percentage >= 60) return "Partial";
    return "Non-Compliant";
  };

  return (
    <div className="compliance-score-card">
      <div className="score-header">
        <h3 className="score-title">{title}</h3>
        <span className={`score-label score-label-${getScoreLabel().toLowerCase().replace("-", "")}`}>
          {getScoreLabel()}
        </span>
      </div>
      
      <div className="score-display">
        <div className="score-circle" style={{ "--percentage": percentage, "--color": getScoreColor() }}>
          <svg className="score-svg" viewBox="0 0 100 100">
            <circle
              className="score-background"
              cx="50"
              cy="50"
              r="45"
            />
            <circle
              className="score-progress"
              cx="50"
              cy="50"
              r="45"
              style={{
                strokeDasharray: `${percentage * 2.827} 282.7`,
              }}
            />
          </svg>
          <div className="score-text">
            <span className="score-value">{score.toFixed(0)}</span>
            <span className="score-max">/{maxScore}</span>
          </div>
        </div>
      </div>
      
      <div className="score-details">
        <div className="score-bar">
          <div
            className="score-bar-fill"
            style={{
              width: `${percentage}%`,
              backgroundColor: getScoreColor(),
            }}
          />
        </div>
        <p className="score-percentage">{percentage.toFixed(1)}%</p>
      </div>
    </div>
  );
};

export default ComplianceScoreCard;

