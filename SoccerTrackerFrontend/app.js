function showPage(pageId, button) {
  const pages = document.querySelectorAll(".page");
  const buttons = document.querySelectorAll(".nav-btn");

  pages.forEach(page => page.classList.remove("active"));
  buttons.forEach(btn => btn.classList.remove("active"));

  document.getElementById(pageId).classList.add("active");
  button.classList.add("active");
}
