import React from "react";

function Dashboard({
  threatLevel,
  totalBlocked,
  totalReceived,
  falsePositives,
  falseNegatives,
}) {
  return (
    <>
      <div className="dashboard">
        {/* Threat Level and Blocked/Received Ratio */}
        <div className="main-indicators">
          <div
            className="threat-level"
            style={{
              backgroundColor: threatLevelColors[threatLevel],
              flex: 1,
              fontSize: "1.5rem",
            }}
          >
            Current Threat Level: {threatLevel}
          </div>
          <div className="blocked-ratio" style={{ flex: 1 }}>
            <span className="big-number">{totalBlocked}/</span>
            <span className="big-number">{totalReceived}</span>
            <div>Requests Blocked</div>
          </div>
        </div>

        {/* Other indicators */}
      </div>

      <div className="other-indicators">
        <div className="false-positives">False Positives: {falsePositives}</div>
        <div className="false-negatives">False Negatives: {falseNegatives}</div>
      </div>
    </>
  );
}

const threatLevelColors = {
  Low: "green",
  Medium: "orange",
  High: "red",
};

export default Dashboard;
