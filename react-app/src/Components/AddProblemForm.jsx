// src/components/AddProblemForm.jsx
import { useState } from "react";
import { addProblem } from "../services/problemService";

function AddProblemForm({ onProblemAdded }) {
  const [id, setId] = useState("");
  const [approach, setApproach] = useState("");

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
    if (!id || !approach) return; // basic guard

    await addProblem({ leetcode_id: id, approach: approach });

    // reset form
    setId("");
    setApproach("");

    // notify parent if needed
    if (onProblemAdded) onProblemAdded();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={id}
        onChange={(e) => setId(e.target.value)}
        placeholder="Problem ID"
      />

      <select
        className="form-select w-75"
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

      <button type="submit">Add</button>
    </form>
  );
}

export default AddProblemForm;
