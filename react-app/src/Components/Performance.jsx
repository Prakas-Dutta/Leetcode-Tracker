// src/Components/Performance.jsx
import { useState, useEffect } from "react";
import { getPerformance } from "../services/problemService";
import "../Styles/Performance.css";

function Performance() {
  const [performanceData, setPerformanceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPerformance()
      .then((data) => setPerformanceData(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const maxCount = Math.max(...performanceData.map((d) => d.no_of_problems), 1);
  const sortedData = [...performanceData].sort(
    (a, b) => b.no_of_problems - a.no_of_problems
  );

  if (loading) {
    return (
      <div className="performance-card performance-status">
        <div className="spinner-border" role="status" />
        <p>Loading performance data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="performance-card performance-status performance-error">
        <p>⚠️ Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="performance-card">
      <h1 className="performance-title">Pattern Performance</h1>

      {sortedData.length === 0 ? (
        <p className="performance-empty">No problem is solved yet!!!</p>
      ) : (
        <table className="performance-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Pattern</th>
              <th>Solved</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map((data, index) => (
              <tr key={data.approach ?? index}>
                <td className="performance-rank">{index + 1}</td>
                <td className="performance-pattern">{data.approach}</td>
                <td className="performance-count">{data.no_of_problems}</td>
                <td className="performance-bar-cell">
                  <div className="performance-bar-track">
                    <div
                      className="performance-bar-fill"
                      style={{
                        width: `${(data.no_of_problems / maxCount) * 100}%`,
                      }}
                    />
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Performance;