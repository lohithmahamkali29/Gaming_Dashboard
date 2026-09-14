(function () {
  const startButton = document.getElementById('start-race');
  const leaderboard = document.getElementById('leaderboard');
  if (!startButton || !leaderboard) return;
  const render = (race) => {
    leaderboard.innerHTML = race.entries.length ? race.entries.map((entry) => `<div class="leader-row"><strong class="position">${entry.position}</strong><div><strong>${entry.driver_name}</strong><small>${entry.rig_name || ''}</small></div><span class="lap">L${entry.current_lap}/${race.total_laps}</span><span class="time">${entry.lap_time == null ? '--' : Number(entry.lap_time).toFixed(3)}s</span></div>`).join('') : '<div class="empty">Add race entries in the admin panel.</div>';
    document.getElementById('race-status').textContent = race.status;
  };
  startButton.addEventListener('click', async () => {
    await fetch(`/api/races/${window.RACE_ID}/start/`, {method: 'POST', headers: {'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)?.[1] || ''}});
    startButton.disabled = true;
  });
  setInterval(async () => {
    const response = await fetch(`/api/races/${window.RACE_ID}/telemetry/`);
    if (response.ok) render(await response.json());
  }, 2000);
})();
