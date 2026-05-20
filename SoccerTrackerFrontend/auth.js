const API = "https://arise-soccertracker.onrender.com";

async function signup() {
  const body = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    position: document.getElementById("position").value,
    dominant_foot: document.getElementById("foot").value
  };

  try {
    const response = await fetch(`${API}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      alert("Signup failed.");
      return;
    }

    alert("Account created!");
    window.location.href = "login.html";

  } catch (error) {
    alert("Backend connection failed.");
    console.error(error);
  }
}

async function login() {
  const body = {
    email: document.getElementById("email").value,
    password: document.getElementById("password").value
  };

  try {
    const response = await fetch(`${API}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      alert("Invalid login.");
      return;
    }

    const data = await response.json();

    localStorage.setItem("player_id", data.player_id);
    localStorage.setItem("player_name", data.name);

    window.location.href = "index.html";

  } catch (error) {
    alert("Backend connection failed.");
    console.error(error);
  }
}
