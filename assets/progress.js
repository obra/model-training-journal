/* Only the reader's local clock changes this display. Snapshot data never refresh. */
(() => {
  "use strict";
  const DEADLINE_UTC = "2026-10-31T04:12:00Z";
  const DEADLINE_MS = Date.parse(DEADLINE_UTC);
  const STALE_AFTER_MS = 60 * 60 * 1000;

  function remainingText(milliseconds) {
    if (milliseconds <= 0) return "Budget elapsed";
    if (milliseconds < 60_000) return "Less than 1 min remaining";
    const totalMinutes = Math.floor(milliseconds / 60_000);
    const days = Math.floor(totalMinutes / 1440);
    const hours = Math.floor((totalMinutes % 1440) / 60);
    const minutes = totalMinutes % 60;
    return `${days}d ${hours}h ${minutes}m remaining`;
  }

  function clockState(now, verified) {
    if (!Number.isFinite(now) || !Number.isFinite(verified) || !Number.isFinite(DEADLINE_MS)) {
      return { countdown: null, stale: null, label: "Local clock unavailable; showing snapshot values." };
    }
    if (now < verified) {
      return { countdown: null, stale: null, label: "Local clock precedes the snapshot; showing snapshot values." };
    }
    const stale = now - verified >= STALE_AFTER_MS;
    return {
      countdown: remainingText(Math.max(0, DEADLINE_MS - now)),
      stale,
      label: stale
        ? "Snapshot stale · at least 60 min old. Countdown uses this device’s clock."
        : "Snapshot under 60 min old. Countdown uses this device’s clock."
    };
  }

  // Expose pure calculations to the local test runner; no browser global is added.
  if (typeof module === "object" && module.exports) {
    module.exports = { DEADLINE_UTC, clockState, remainingText };
  }
  if (typeof document === "undefined") return;

  const root = document.querySelector("[data-progress]");
  if (!root) return;
  const countdown = root.querySelector("[data-countdown]");
  const freshness = root.querySelector("[data-freshness]");
  if (!countdown || !freshness) return;
  const snapshotCountdown = countdown.textContent;
  const verified = Date.parse(root.dataset.verifiedAt);

  function update() {
    let state;
    try {
      state = root.dataset.deadline === DEADLINE_UTC
        ? clockState(Date.now(), verified)
        : { countdown: null, stale: null, label: "Clock display unavailable; showing snapshot values." };
    } catch (_) {
      state = { countdown: null, stale: null, label: "Local clock unavailable; showing snapshot values." };
    }
    countdown.textContent = state.countdown === null ? snapshotCountdown : state.countdown;
    // Only freshness transitions announce a status change, not every clock minute.
    if (freshness.textContent !== state.label) freshness.textContent = state.label;
    if (state.stale === null) freshness.removeAttribute("data-stale");
    else freshness.setAttribute("data-stale", String(state.stale));
  }

  update();
  setInterval(update, 60_000);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) update();
  });
})();
