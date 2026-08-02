// src/services/problemService.js
import BASE_URL from "./api";

const access_token = localStorage.getItem("access_token");

export async function getProblemCount() {
  const res = await fetch(`${BASE_URL}/problem_list/`, 
  {headers: { "Content-Type": "application/json", token: access_token }});
  console.log(res)
  if (!res.ok) throw new Error("Failed to fetch problems");
  return res.json();
}

export async function addProblem(problem) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", token: access_token },
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
    headers: { "Content-Type": "application/json", token: access_token },
    body: JSON.stringify(updates),
  });
  if (!res.ok) throw new Error("Failed to update problem");
  return res.json();
}

export async function deleteProblem(id, approach) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json", token: access_token },
    body: JSON.stringify({ leetcode_id: id, approach: approach }),
  });
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to delete problem");
  }

  return data;
}

export async function getPerformance() {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    headers: { "Content-Type": "application/json", token: access_token }
  });
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch performance data");
  }

  return data;
}

export async function chatbotSuggestions() {
  const res = await fetch(`${BASE_URL}/suggestions/`, {
    headers: { "Content-Type": "application/json", token: access_token }
  });
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
  const res = await fetch(`${BASE_URL}/${id}/`, {
    headers: { "Content-Type": "application/json", token: access_token }
  });
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
  const res = await fetch(`${BASE_URL}/valid_approaches/${id}/`, {
    headers: { "Content-Type": "application/json", "token": access_token }
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch valid approaches");
  }
  setValidApproaches(data);
}

export async function loginUser(username, password) {
  const res = await fetch(`${BASE_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username:username, password:password }),
  });
  const data = await res.json();
  localStorage.setItem("access_token", data.token);
  if (!res.ok) {
    throw new Error(data.detail || "Failed to validate user");
  }
  return data.message;
}

export async function signupUser(username, password) {
  const res = await fetch(`${BASE_URL}/signup/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username:username, password:password }),
  });
  const data = await res.json();
  return data;
}

export function authenticateUser(username, password) {
  if (!username || !password) {
    throw new Error("Username and password are required");
  }
  else if (username.includes(" ") || password.includes(" ")) {
    throw new Error("Username and password cannot contain spaces");
  }
  else if (username.length < 3 || password.length < 3) {
    throw new Error("Username and password must be at least 3 characters long");
  }
  else if (!username.includes("@")) {
    throw new Error("Username must contain '@'");
  }
  else if (!username.includes(".com")) {
    throw new Error("Username must contain '.com'");
  }
  else if (username.indexOf("@") > username.indexOf(".com")) {
    throw new Error("Username must contain '@' before '.com'");
  }
  else if (username.indexOf("@") !== username.lastIndexOf("@")) {
    throw new Error("Username must contain only one '@'");
  }
  else
  {
    return true;
  }
}
