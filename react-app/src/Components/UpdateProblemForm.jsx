// src/components/UpdateProblemForm.jsx
import { useState } from "react";
import { updateProblem } from "../services/problemService";
import approaches from "./Approaches";
import "../Styles/UpdateProblemForm.css";
import { useEffect } from "react";
import { getValidApproaches } from "../services/problemService";

function UpdateProblemForm({ onProblemAdded }) {
  const [id, setId] = useState("");
  const [updatedApproach, setUpdatedApproach] = useState("");
  const [approach, setApproach] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [validApproaches, setValidApproaches] = useState([]);


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!id || !approach || !updatedApproach) return;

    setSubmitting(true);
    try {
      await updateProblem({
        leetcode_id: id,
        approach: approach,
        updated_approach: updatedApproach,
      });
      alert("Problem updated successfully!");
      setId("");
      setApproach("");
      setUpdatedApproach("");
      if (onProblemAdded) onProblemAdded();
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };
  useEffect(() => {
    getValidApproaches(id, setValidApproaches);
  }, [id]);

  return (
    <div className="update-problem-card">
      <h1 className="update-problem-title">Update a Problem</h1>
      <form onSubmit={handleSubmit} className="update-problem-form">
        <input
          className="update-problem-input"
          value={id}
          onChange={(e) => setId(e.target.value)}
          placeholder="Problem ID"
          type="number"
        />

        <label className="update-problem-label">Current Approach</label>
        <select
          className="update-problem-select"
          value={approach}
          onChange={(e) => setApproach(e.target.value)}
        >
          <option value="" disabled>
            Select a pattern
          </option>
          {validApproaches.map((p, i) => (
            <option key={i} value={p}>
              {p}
            </option>
          ))}
        </select>

        <label className="update-problem-label">New Approach</label>
        <select
          className="update-problem-select"
          value={updatedApproach}
          onChange={(e) => setUpdatedApproach(e.target.value)}
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

        <button type="submit" className="update-problem-btn" disabled={submitting}>
          {submitting ? "Updating..." : "Update Problem"}
        </button>
      </form>
    </div>
  );
}

export default UpdateProblemForm;