// src/components/ProblemCount.jsx
import { useState, useEffect } from "react";
import { getProblems } from "../services/problemService";

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

  if (count === null) return <p>Loading...</p>;

  return (
    <span className="badge rounded-pill bg-primary fs-6">
      Problem Solved {count}
    </span>
  );
}

export default ProblemCount;
