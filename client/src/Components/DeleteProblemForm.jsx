// src/components/DeleteProblemForm.jsx
import { useState, useEffect } from "react";
import { deleteProblem } from "../services/problemService";
import approaches from "./Approaches";
import "../Styles/DeleteProblemForm.css";
import {getValidApproaches} from "../services/problemService";

function DeleteProblemForm() {
  const [id, setId] = useState("");
  const [approach, setApproach] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [validApproach, setValidApproach] = useState([]);


  const handleDelete = async (e) => {
    e.preventDefault();
    if (!id || !approach) return;

    setSubmitting(true);
    try {
      await deleteProblem(id, approach);
      alert("Problem deleted successfully!");
      setId("");
      setApproach("");
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };
  useEffect(() => {
    getValidApproaches(id, setValidApproach);
  }, [id]);
  return (
    <div className="delete-problem-card">
      <h1 className="delete-problem-title">Delete a Problem</h1>
      <form onSubmit={handleDelete} className="delete-problem-form">
        <input
          className="delete-problem-input"
          value={id}
          onChange={(e) => setId(e.target.value)}
          placeholder="Problem ID"
          type="number"
        />

        <select
          className="delete-problem-select"
          value={approach}
          onChange={(e) => setApproach(e.target.value)}
        >
          <option value="" disabled>
            Select a pattern
          </option>
          {validApproach.map((p, i) => (
            <option key={i} value={p}>
              {p}
            </option>
          ))}
        </select>

        <button
          type="submit"
          className="delete-problem-btn"
          disabled={submitting}
        >
          {submitting ? "Deleting..." : "Delete Problem"}
        </button>
      </form>
    </div>
  );
}

export default DeleteProblemForm;