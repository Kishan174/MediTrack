window.addEventListener("load", () => {
  document.getElementById("pageLoader")?.classList.add("hide");
});

const root = document.documentElement;
const savedTheme = localStorage.getItem("meditrack-theme");
if (savedTheme) root.dataset.theme = savedTheme;

document.getElementById("themeToggle")?.addEventListener("click", () => {
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("meditrack-theme", root.dataset.theme);
});

document.getElementById("menuToggle")?.addEventListener("click", () => {
  document.querySelector(".sidebar")?.classList.toggle("open");
});

document.querySelectorAll(".counter").forEach((counter) => {
  const target = Number(counter.dataset.target || 0);
  let current = 0;
  const step = Math.max(1, Math.ceil(target / 38));
  const tick = () => {
    current = Math.min(target, current + step);
    counter.textContent = current;
    if (current < target) requestAnimationFrame(tick);
  };
  tick();
});

const searchInput = document.querySelector("[data-suggest-url]");
const suggestions = document.getElementById("suggestions");
if (searchInput && suggestions) {
  searchInput.addEventListener("input", async () => {
    const q = searchInput.value.trim();
    if (q.length < 2) {
      suggestions.style.display = "none";
      return;
    }
    const response = await fetch(`${searchInput.dataset.suggestUrl}?q=${encodeURIComponent(q)}`);
    const rows = await response.json();
    suggestions.innerHTML = rows.map((row) => `<a href="/patients/${row.id}"><strong>${row.name}</strong><small class="d-block text-muted">${row.contact}</small></a>`).join("");
    suggestions.style.display = rows.length ? "block" : "none";
  });
}

async function loadDashboardCharts() {
  if (!window.MEDITRACK_ANALYTICS_URL || !window.Chart) return;
  const response = await fetch(window.MEDITRACK_ANALYTICS_URL);
  const data = await response.json();
  const palette = ["#2563eb", "#0fb9b1", "#16a34a", "#ef4444", "#8b5cf6"];
  const appointmentCanvas = document.getElementById("appointmentChart");
  const patientCanvas = document.getElementById("patientChart");
  if (appointmentCanvas) {
    new Chart(appointmentCanvas, {
      type: "bar",
      data: { labels: data.appointments.labels, datasets: [{ data: data.appointments.data, backgroundColor: palette, borderRadius: 8 }] },
      options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
    });
  }
  if (patientCanvas) {
    new Chart(patientCanvas, {
      type: "doughnut",
      data: { labels: data.patients.labels, datasets: [{ data: data.patients.data, backgroundColor: palette, borderWidth: 0 }] },
      options: { plugins: { legend: { position: "bottom" } }, cutout: "68%" }
    });
  }
}
loadDashboardCharts();
