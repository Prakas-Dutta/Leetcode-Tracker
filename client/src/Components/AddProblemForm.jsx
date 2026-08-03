// src/components/AddProblemForm.jsx
import { useState, useEffect } from "react";
import { addProblem } from "../services/problemService";
import approaches from "./Approaches";
import "../Styles/AddProblemForm.css";
import { getTitle } from "../services/problemService";

function AddProblemForm({ onProblemAdded }) {
  const [id, setId] = useState("");
  const [loading, setLoading] = useState(true);
  const [approach, setApproach] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [problemTitle, setProblemTitle] = useState("");


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
  useEffect(() => {
    getTitle(id, setProblemTitle, setLoading);
  }, [id]);
  return (
    <div className="add-problem-card">
      <h1 className="add-problem-title">Add a New Problem</h1>
      <form onSubmit={handleSubmit} className="add-problem-form">
        <input
          className="add-problem-input"
          value={id}
          onChange={(e) => {setId(e.target.value)}}
          placeholder="Problem ID"
          type="number"
        />
        <label className="add-problem-label" htmlFor="approach">
        {loading ? "Problem Title" : problemTitle ? `Problem Title: ${problemTitle}` : "Problem Title: Not Found"}
        </label>
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