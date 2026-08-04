// src/services/problemService.js
import BASE_URL from "./api";


export async function getProblemCount() {
  if (!sessionStorage.getItem("access_token")) {
    return 0;
  }
  const res = await fetch(`${BASE_URL}/problem_list/`, 
  {headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") }});
  if (!res.ok) throw new Error("Failed to fetch problems");
  return res.json();
}

export async function addProblem(problem) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") },
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
    headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") },
    body: JSON.stringify(updates),
  });
  if (!res.ok) throw new Error("Failed to update problem");
  return res.json();
}

export async function deleteProblem(id, approach) {
  const res = await fetch(`${BASE_URL}/completed_list/`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") },
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
    headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") }
  });
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch performance data");
  }

  return data;
}

export async function chatbotSuggestions() {
  const res = await fetch(`${BASE_URL}/suggestions/`, {
    headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") }
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
    headers: { "Content-Type": "application/json", token: sessionStorage.getItem("access_token") }
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
    headers: { "Content-Type": "application/json", "token": sessionStorage.getItem("access_token") }
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
  sessionStorage.setItem("access_token", data.token);
  if (!res.ok) {
    throw new Error(data.detail || "Failed to validate user");
  }
  return data.message;
}

export async function signupUser(username, leetcode_username, password) {
  const res = await fetch(`${BASE_URL}/signup/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username:username, leetcode_username:leetcode_username, password:password }),
  });
  const data = await res.json();
  return data;
}

export function logoutUser() {
  sessionStorage.removeItem("access_token");
}

export function authenticateUser(array) {
  if(array.length === 3) {
    var username = array[0];
    var leetcode_username = array[1];
    var password = array[2];
  }
  else if(array.length === 2) {
    var username = array[0];
    var password = array[1];
  }
  if(array.length === 3 && (!username || !leetcode_username || !password)) {
    throw new Error("Username, Leetcode username and password are required");
  }
  else if (!username || !password) {
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
  else if (username.indexOf("@") !== username.lastIndexOf("@")) {
    throw new Error("Username must contain only one '@'");
  }
  else
  {
    return true;
  }
}


export function isTokenExpired(token) {
  if (!token) return true;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp * 1000 < Date.now();
  } catch {
    return true;
  }
}
