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
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to add problem");
  }

  return data;
}

export async function updateProblem(updates) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  });
  if (!res.ok) throw new Error("Failed to update problem");
  return res.json();
}

export async function deleteProblem(id, approach) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ leetcode_id: id, approach: approach }),
  });
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to delete problem");
  }

  return data;
}

export async function getPerformance() {
  const res = await fetch(`${BASE_URL}/completed_list/`);
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch performance data");
  }

  return data;
}

export async function chatbotSuggestions() {
  const res = await fetch(`${BASE_URL}/suggestions/`);
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch chatbot suggestions");
  }

  return data;
}

export async function getTitle(id, setProblemTitle, setLoading) {
  if(id == null || id === "") {
    setProblemTitle("");
    setLoading(false);
    return;
  }
  const res = await fetch(`${BASE_URL}/${id}/`);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch problem title");
  }
  setProblemTitle(data.title);
  setLoading(false);
}

export async function getValidApproaches(id, setValidApproaches) {
  if(id == null || id === "") {
    setValidApproaches([]);
    return;
  }
  const res = await fetch(`${BASE_URL}/valid_approaches/${id}/`);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch valid approaches");
  }
  setValidApproaches(data);
}
