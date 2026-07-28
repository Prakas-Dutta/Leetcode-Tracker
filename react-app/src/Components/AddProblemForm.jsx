// src/components/AddProblemForm.jsx
import { useState } from "react";
import { addProblem } from "../services/problemService";
import "../Styles/AddProblemForm.css";

function AddProblemForm({ onProblemAdded }) {
  const [id, setId] = useState("");
  const [loading, setLoading] = useState(true);
  const [approach, setApproach] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const approaches = [
    "Two Pointers",
    "Sliding Window (Fixed Size)",
    "Sliding Window (Variable Size)",
    "Prefix Sum",
    "Prefix Sum + HashMap",
    "Kadane's Algorithm",
    "Monotonic Stack",
    "Monotonic Deque",
    "Fast & Slow Pointers",
    "Binary Search on Array",
    "Sorting-Based Approach",
    "Cyclic Sort",
    "In-place Array Manipulation",
    "Hashing / Frequency Map",
    "Greedy",
    "Divide and Conquer",
    "Dynamic Programming on Arrays",
    "Matrix Traversal Patterns",
    "Union-Find (Disjoint Set)",
    "Bit Manipulation",
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!id || !approach) return;

    setSubmitting(true);
    try {
      await addProblem({ leetcode_id: id, approach: approach });
      alert("Problem added successfully!");
      setId("");
      setApproach("");
      if (onProblemAdded) onProblemAdded();
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="add-problem-card">
      <h1 className="add-problem-title">Add a New Problem</h1>
      <form onSubmit={handleSubmit} className="add-problem-form">
        <input
          className="add-problem-input"
          value={id}
          onChange={(e) => {setId(e.target.value), setLoading(false)}}
          placeholder="Problem ID"
          type="number"
        />
        <input
          className="add-problem-input"
          value={loading ? "Loading..." : ""}
          placeholder="Problem Title"
          type="string"
        />
        <select
          className="add-problem-select"
          value={approach}
          onChange={(e) => setApproach(e.target.value)}
        >
          <option value="" disabled>
            Select a pattern
          </option>
          {approaches.map((p, i) => (
            <option key={i} value={p}>
              {p}
            </option>
          ))}
        </select>

        <button
          type="submit"
          className="add-problem-btn"
          disabled={submitting}
        >
          {submitting ? "Adding..." : "Add Problem"}
        </button>
      </form>
    </div>
  );
}

export default AddProblemForm;