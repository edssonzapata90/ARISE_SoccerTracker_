const API =
"http://127.0.0.1:8000";

function showPage(
page,
button
){

document
.querySelectorAll(".page")
.forEach(
p=>p.classList.remove(
"active"
)
);

document
.getElementById(
page
)
.classList.add(
"active"
);

document
.querySelectorAll(
".nav-btn"
)
.forEach(
b=>b.classList.remove(
"active"
)
);

button.classList.add(
"active"
);

if(
page==="home"
)
refreshHome();

if(
page==="stats"
)
loadStats();

if(
page==="sessions"
)
loadSessions();

if(
page==="profile"
)
loadProfile();

}

async function testBackend(){

try{

let r=
await fetch(
`${API}/`
);

let d=
await r.json();

document
.getElementById(
"backend-status"
)
.innerText=
d.message;

}

catch{

document
.getElementById(
"backend-status"
)
.innerText=
"Backend connection failed.";

}

}

async function loadPlayers(){

let box=
document.getElementById(
"players-box"
);

try{

let r=
await fetch(
`${API}/players`
);

let players=
await r.json();

box.innerHTML="";

players.forEach(
p=>{

box.innerHTML+=`

<div class='card'>

<h3>

${p.name}

</h3>

<p>

Position:
${p.position}

</p>

<p>

Foot:
${p.dominant_foot}

</p>

</div>

`;

});

}

catch{

box.innerHTML=

"<div class='card'>Could not load players.</div>";

}

}

async function loadStats(){

let box=
document.getElementById(
"stats-box"
);

try{

let r=
await fetch(
`${API}/sensor-data`
);

let data=
await r.json();

let touches=0;

let dribbles=0;

let sprints=0;

data.forEach(
x=>{

touches+=
x.touch_detected||0;

dribbles+=
x.dribble_detected||0;

sprints+=
x.sprint_detected||0;

}
);

box.innerHTML=

`

<div class='card stat'>

Touches

<strong>

${touches}

</strong>

</div>

<div class='card stat'>

Dribbles

<strong>

${dribbles}

</strong>

</div>

<div class='card stat'>

Sprints

<strong>

${sprints}

</strong>

</div>

`;

}

catch{

box.innerHTML=

"<div class='card'>Could not load stats.</div>";

}

}

async function loadSessions(){

let box=
document.getElementById(
"sessions-box"
);

try{

let r=
await fetch(
`${API}/sessions`
);

let s=
await r.json();

box.innerHTML="";

s.forEach(
x=>{

box.innerHTML+=`

<div class='card'>

<h3>

${x.session_name}

</h3>

<p>

Session:

${x.id}

</p>

</div>

`;

});

}

catch{

box.innerHTML=

"<div class='card'>Could not load sessions.</div>";

}

}

async function loadProfile(){

let box=
document.getElementById(
"profile-box"
);

try{

let r=
await fetch(
`${API}/players`
);

let p=
await r.json();

let player=
p[0];

box.innerHTML=

`

<div class='card'>

<h3>

${player.name}

</h3>

<p>

${player.position}

</p>

<p>

${player.dominant_foot}

</p>

</div>

`;

}

catch{

box.innerHTML=

"<div class='card'>Could not load profile.</div>";

}

}

function refreshHome(){

testBackend();

loadPlayers();

}

refreshHome();

refreshHome();
