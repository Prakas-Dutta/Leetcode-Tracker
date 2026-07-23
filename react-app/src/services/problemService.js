// src/services/problemService.js
import BASE_URL from "./api";

export async function getProblems() {
  const res = await fetch(`${BASE_URL}/problem_list/`);
  console.log(res)
  if (!res.ok) throw new Error("Failed to fetch problems");
  return res.json();
}

export async function addProblem(problem) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(problem),
  });
  if (!res.ok) throw new Error("Failed to add problem");
  return res.json();
}

// export async function updateProblem(id, updates) {
//   const res = await fetch(`${BASE_URL}/problems/${id}`, {
//     method: "PUT",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(updates),
//   });
//   if (!res.ok) throw new Error("Failed to update problem");
//   return res.json();
// }

// export async function deleteProblem(id) {
//   const res = await fetch(`${BASE_URL}/problems/${id}`, {
//     method: "DELETE",
//   });
//   if (!res.ok) throw new Error("Failed to delete problem");
// }