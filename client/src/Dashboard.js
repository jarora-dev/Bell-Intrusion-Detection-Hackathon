import React, { useState } from "react";

function Dashboard({
  threatLevel,
  totalBlocked,
  totalReceived,
  falsePositives,
  falseNegatives,
}) {
  const [threatLevelState, setThreatLevel] = useState(threatLevel);
  const [totalBlockedState, setTotalBlocked] = useState(totalBlocked);
  const [totalReceivedState, setTotalReceived] = useState(totalReceived);
  const [falsePositivesState, setFalsePositives] = useState(falsePositives);
  const [falseNegativesState, setFalseNegatives] = useState(falseNegatives);

  return (
    <>
      <div className="dashboard">
        {/* Threat Level and Blocked/Received Ratio */}
        <div className="main-indicators">
          <div
            className="threat-level"
            style={{
              backgroundColor: threatLevelColors[threatLevelState],
              flex: 1,
              fontSize: "1.5rem",
            }}
          >
            Current Threat Level: {threatLevel}
          </div>
          <div className="blocked-ratio" style={{ flex: 1 }}>
            <span className="big-number">{totalBlockedState}/</span>
            <span className="big-number">{totalReceivedState}</span>
            <div>Requests Blocked</div>
          </div>
        </div>

        {/* Other indicators */}
      </div>

      <div className="other-indicators">
        <div className="false-positives">
          False Positives: {falsePositivesState}
        </div>
        <div className="false-negatives">
          False Negatives: {falseNegativesState}
        </div>
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
