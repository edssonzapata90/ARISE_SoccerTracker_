const API = "https://arise-soccertracker.onrender.com";

function showPage(pageId, button) {
  const pages = document.querySelectorAll(".page");
  const buttons = document.querySelectorAll(".nav-btn");

  pages.forEach(page => {
    page.classList.remove("active");
  });

  buttons.forEach(btn => {
    btn.classList.remove("active");
  });

  document.getElementById(pageId).classList.add("active");
  button.classList.add("active");

  if (pageId === "home") {
    refreshHome();
  }

  if (pageId === "stats") {
    loadStats();
  }

  if (pageId === "sessions") {
    loadSessions();
  }

  if (pageId === "profile") {
    loadProfile();
  }
}

async function testBackend() {
  try {
    const response = await fetch(`${API}/`);
    const data = await response.json();

    document.getElementById("backend-status").innerText = data.message;
  } catch (error) {
    document.getElementById("backend-status").innerText =
      "Backend connection failed.";
    console.error(error);
  }
}

async function loadPlayers() {
  try {
    const response = await fetch(`${API}/players`);
    const players = await response.json();

    const box = document.getElementById("players-box");

    if (!players || players.length === 0) {
      box.innerHTML = "<p>No players found yet.</p>";
      return;
    }

    let html = "";

    players.forEach(player => {
      html += `
        <div class="card">
          <h3>${player.name}</h3>
          <p><strong>Position:</strong> ${player.position}</p>
          <p><strong>Dominant Foot:</strong> ${player.dominant_foot}</p>
        </div>
      `;
    });

    box.innerHTML = html;
  } catch (error) {
    document.getElementById("players-box").innerHTML =
      "<p>Could not load players.</p>";
    console.error(error);
  }
}

async function loadStats() {
  try {
    const response = await fetch(`${API}/sensor-data`);
    const data = await response.json();

    const box = document.getElementById("stats-box");

    if (!data || data.length === 0) {
      box.innerHTML = "<p>No sensor data found yet.</p>";
      return;
    }

    let totalTouches = 0;
    let totalDribbles = 0;
    let totalSprints = 0;

    data.forEach(item => {
      totalTouches += item.touch_detected || 0;
      totalDribbles += item.dribble_detected || 0;
      totalSprints += item.sprint_detected || 0;
    });

    box.innerHTML = `
      <div class="card stat">
        <span>Total Touches</span>
        <strong>${totalTouches}</strong>
      </div>

      <div class="card stat">
        <span>Total Dribbles</span>
        <strong>${totalDribbles}</strong>
      </div>

      <div class="card stat">
        <span>Total Sprints</span>
        <strong>${totalSprints}</strong>
      </div>
    `;
  } catch (error) {
    document.getElementById("stats-box").innerHTML =
      "<p>Could not load stats.</p>";
    console.error(error);
  }
}

async function loadSessions() {
  try {
    const response = await fetch(`${API}/sessions`);
    const sessions = await response.json();

    const box = document.getElementById("sessions-box");

    if (!sessions || sessions.length === 0) {
      box.innerHTML = "<p>No sessions found yet.</p>";
      return;
    }

    let html = "";

    sessions.forEach(session => {
      html += `
        <div class="card">
          <h3>${session.session_name}</h3>
          <p><strong>Session ID:</strong> ${session.id}</p>
          <p><strong>Player ID:</strong> ${session.player_id}</p>
        </div>
      `;
    });

    box.innerHTML = html;
  } catch (error) {
    document.getElementById("sessions-box").innerHTML =
      "<p>Could not load sessions.</p>";
    console.error(error);
  }
}

async function loadProfile() {
  try {
    const response = await fetch(`${API}/players`);
    const players = await response.json();

    const box = document.getElementById("profile-box");

    if (!players || players.length === 0) {
      box.innerHTML = "<p>No player profile found yet.</p>";
      return;
    }

    const player = players[0];

    box.innerHTML = `
      <div class="card">
        <p><strong>Name:</strong> ${player.name}</p>
        <p><strong>Position:</strong> ${player.position}</p>
        <p><strong>Dominant Foot:</strong> ${player.dominant_foot}</p>
      </div>
    `;
  } catch (error) {
    document.getElementById("profile-box").innerHTML =
      "<p>Could not load profile.</p>";
    console.error(error);
  }
}

function refreshHome() {
  testBackend();
  loadPlayers();
}

refreshHome();
