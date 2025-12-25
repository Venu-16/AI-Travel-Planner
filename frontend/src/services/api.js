const API_URL = process.env.REACT_APP_API_URL || "";

function getToken() {
  return localStorage.getItem("token");
}

async function post(path, body) {
  if (API_URL) {
    const res = await fetch(`${API_URL}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(getToken() ? { Authorization: `Bearer ${getToken()}` } : {}),
      },
      body: JSON.stringify(body),
    });
    return res.json();
  }

  // Fallback to local mock behaviour
  return mockPost(path, body);
}

function mockPost(path, body) {
  if (path === "/auth/register") {
    const users = JSON.parse(localStorage.getItem("mock_users") || "[]");
    if (users.find((u) => u.email === body.email)) {
      return { error: "User exists" };
    }
    users.push({ email: body.email, password: body.password });
    localStorage.setItem("mock_users", JSON.stringify(users));
    const token = `mock-token-${body.email}`;
    localStorage.setItem("token", token);
    return { token };
  }

  if (path === "/auth/login") {
    const users = JSON.parse(localStorage.getItem("mock_users") || "[]");
    const u = users.find((x) => x.email === body.email && x.password === body.password);
    if (!u) return { error: "Invalid credentials" };
    const token = `mock-token-${body.email}`;
    localStorage.setItem("token", token);
    return { token };
  }

  if (path === "/generate") {
    // simple mock itinerary
    const { destination, days } = body;
    const d = Number(days) || 2;
    let text = "";
    for (let i = 1; i <= d; i++) {
      text += `Day ${i}: ${destination} - Sample activities (morning/afternoon/evening)\n`;
    }
    return { itinerary: text };
  }

  return { error: "Unknown mock path" };
}

export async function register({ email, password }) {
  const r = await post("/auth/register", { email, password });
  return r;
}

export async function login({ email, password }) {
  const r = await post("/auth/login", { email, password });
  return r;
}

export async function generateItinerary({ destination, days }) {
  // Try real backend first
  try {
    if (API_URL) {
      const res = await post("/generate", { destination, days });
      return res.itinerary || JSON.stringify(res);
    }
    const mock = await post("/generate", { destination, days });
    return mock.itinerary;
  } catch (e) {
    const mock = await post("/generate", { destination, days });
    return mock.itinerary;
  }
}

export function logout() {
  localStorage.removeItem("token");
}

export function getCurrentToken() {
  return getToken();
}
