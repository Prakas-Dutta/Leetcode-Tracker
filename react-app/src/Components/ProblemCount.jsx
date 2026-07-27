// src/components/ProblemCount.jsx
import { useState, useEffect } from "react";
import { getProblems } from "../services/problemService";
import "../Styles/ProblemCount.css";
import { Outlet } from "react-router-dom";

function ProblemCount() {
  const [count, setCount] = useState(null);

  useEffect(() => {
    async function fetchCount() {
      try {
        const data = await getProblems();
        setCount(data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchCount();
  }, []);

  return (
    <>
    <div className="d-flex justify-content-end">
    <span className={`badge rounded-pill problem-count-badge ${count !== null ? "loaded" : ""}`}>
      <span className="problem-count-icon">🔥</span>
      <span className="problem-count-label">Problems Solved</span>
      <span className="problem-count-value">
        {count === null ? (
          <span className="spinner-border spinner-border-sm" role="status" />
        ) : (
          count
        )}
      </span>
    </span>
      </div>
      <Outlet />
      </>
  );
}

export default ProblemCount;