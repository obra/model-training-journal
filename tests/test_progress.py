"""Check snapshot truthfulness, fixed-budget arithmetic and progressive enhancement."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build import DEADLINE_UTC, load_progress, remaining_at_snapshot, render_progress, utc_timestamp

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    return {
        "schema": 1, "model_parameters": 97_536_768, "initialization": "from scratch",
        "experiment_state": "A bounded diagnostic completed.",
        "latest_result": {"summary": "A measured result with stated limits.", "url": "/model-training-journal/current-plan/#latest-result"},
        "verified_at_utc": "2026-10-26T04:12:00Z", "deadline_utc": DEADLINE_UTC,
    }


class ProgressTests(unittest.TestCase):
    def load_fixture(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            path.write_text(json.dumps(data))
            return load_progress(path)

    def test_deadline_is_fixed_and_timestamps_require_utc(self):
        self.load_fixture(fixture())
        for key, value in (("deadline_utc", "2026-11-01T04:12:00Z"),
                           ("verified_at_utc", "2026-10-26T04:12:00"),
                           ("verified_at_utc", "2026-10-26T04:12:00+00:00"),
                           ("model_parameters", True)):
            data = fixture()
            data[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.load_fixture(data)

    def test_progress_text_is_escaped_and_result_url_cannot_execute(self):
        data = fixture()
        data["experiment_state"] = '</dd><script>alert("fixture")</script>'
        data["latest_result"]["summary"] = '<img src=x onerror="fixture">'
        html = render_progress(self.load_fixture(data))
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img", html)
        for bad_url in ("javascript:alert(1)", "https://example.org/", "/model-training-journal/../private/", '/model-training-journal/\" onclick=\"x'):
            data["latest_result"]["url"] = bad_url
            with self.subTest(url=bad_url), self.assertRaises(ValueError):
                self.load_fixture(data)

    def test_no_javascript_fallback_is_explicitly_a_snapshot(self):
        html = render_progress(fixture())
        self.assertIn("12d 0h 0m remaining at snapshot", html)
        self.assertIn("Status snapshot", html)
        self.assertIn("last verified", html)
        self.assertIn("Data do not refresh here", html)
        self.assertIn("Local clock unavailable", html)
        self.assertIn("26 Oct 2026, 04:12:00 UTC", html)
        self.assertIn("7 Nov 2026, 04:12 UTC", html)
        self.assertNotIn("%", html)
        self.assertEqual(remaining_at_snapshot(utc_timestamp(DEADLINE_UTC)), "Budget elapsed at snapshot")
        self.assertEqual(remaining_at_snapshot(utc_timestamp("2026-11-08T04:12:00Z")), "Budget elapsed at snapshot")

    def test_local_clock_boundaries_and_failure_restore_snapshot(self):
        program = r'''
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const api = require("./assets/progress.js");
const deadline = Date.parse("2026-11-07T04:12:00Z");
const verified = Date.parse("2026-10-26T04:12:00Z");
assert.equal(api.DEADLINE_UTC, "2026-11-07T04:12:00Z");
assert.equal(api.clockState(verified, verified).countdown, "12d 0h 0m remaining");
assert.equal(api.clockState(deadline - 1, verified).countdown, "Less than 1 min remaining");
assert.equal(api.clockState(deadline, verified).countdown, "Budget elapsed");
assert.equal(api.clockState(deadline + 86400000, verified).countdown, "Budget elapsed");
assert.equal(api.clockState(verified + 3599999, verified).stale, false);
assert.equal(api.clockState(verified + 3600000, verified).stale, true);
assert.equal(api.clockState(verified - 1, verified).countdown, null);
assert.equal(api.clockState(NaN, verified).countdown, null);
assert.equal(api.clockState(verified, NaN).countdown, null);

let now = verified + 3600000;
class LocalDate extends Date { static now() { return now; } }
const countdown = { textContent: "12d 0h 0m remaining at snapshot" };
const freshness = {
  textContent: "Local clock unavailable", attrs: {},
  setAttribute(key, value) { this.attrs[key] = value; },
  removeAttribute(key) { delete this.attrs[key]; }
};
const root = {
  dataset: { verifiedAt: "2026-10-26T04:12:00Z", deadline: api.DEADLINE_UTC },
  querySelector(selector) { return selector === "[data-countdown]" ? countdown : freshness; }
};
let timer, visibilityListener, requestCount = 0;
vm.runInNewContext(fs.readFileSync("assets/progress.js", "utf8"), {
  Date: LocalDate,
  document: { hidden: false, querySelector() { return root; }, addEventListener(event, listener) { assert.equal(event, "visibilitychange"); visibilityListener = listener; } },
  setInterval(callback, interval) { assert.equal(interval, 60000); timer = callback; },
  fetch() { requestCount++; throw new Error("Network access is forbidden"); }
});
assert.equal(countdown.textContent, "11d 23h 0m remaining");
assert.equal(freshness.attrs["data-stale"], "true");
now = deadline;
timer();
assert.equal(countdown.textContent, "Budget elapsed");
now = NaN;
timer();
assert.equal(countdown.textContent, "12d 0h 0m remaining at snapshot");
assert.match(freshness.textContent, /clock unavailable/);
assert.equal(freshness.attrs["data-stale"], undefined);
now = verified - 1;
visibilityListener();
assert.match(freshness.textContent, /precedes the snapshot/);
root.dataset.deadline = "2026-11-01T04:12:00Z";
now = verified;
timer();
assert.equal(countdown.textContent, "12d 0h 0m remaining at snapshot");
assert.match(freshness.textContent, /display unavailable/);
assert.equal(requestCount, 0);
console.log("Clock arithmetic, stale boundary, immutable deadline and no-network DOM updates passed.");
'''
        result = subprocess.run(["node", "-e", program], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
