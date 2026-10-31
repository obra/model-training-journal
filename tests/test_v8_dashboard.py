"""V8 is a new, worse development-panel result, not a fresh reasoning score."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import dashboard
import build


class V8DashboardContracts(unittest.TestCase):
    def test_identical_panel_parent_and_regression_remain_visible(self):
        v7 = json.loads((ROOT / 'assets/v6-v7-cfr-checkpoints.json').read_text())
        v8 = json.loads((ROOT / 'assets/v8-cfr-checkpoints.json').read_text())
        dashboard.validate_v8(v8, v7)
        data = dashboard.load_dashboard(ROOT, build.load_posts())
        self.assertEqual(data['summary']['language']['stage'], 'V8 terminal')
        self.assertEqual(data['summary']['language']['value'], 35.151670432677435)
        self.assertGreater(data['summary']['language']['value'], data['summary']['language']['prior_value'])
        panel = next(p for p in dashboard.chart_definitions(data) if p['id'] == 'cfr-v8')
        self.assertEqual([p['x'] for p in panel['rows']], [0, 5100685, 10201586])
        self.assertEqual([p['denominator'] for p in panel['rows']], [7057] * 3)
        self.assertEqual(panel['source'], 'assets/v8-cfr-checkpoints.json')

    def test_panel_or_parent_change_is_rejected(self):
        v7 = json.loads((ROOT / 'assets/v6-v7-cfr-checkpoints.json').read_text())
        original = json.loads((ROOT / 'assets/v8-cfr-checkpoints.json').read_text())
        for change in ('panel', 'parent', 'terminal', 'nan'):
            v8 = deepcopy(original)
            if change == 'panel': v8['scoring_contract']['scored_labels'] = 130209
            elif change == 'parent': v8['stage']['points'][0]['checkpoint_sha256'] = '0' * 64
            elif change == 'terminal': v8['stage']['points'].pop()
            else: v8['stage']['points'][-1]['perplexity'] = float('nan')
            with self.subTest(change=change), self.assertRaises(ValueError):
                dashboard.validate_v8(v8, v7)


if __name__ == '__main__':
    unittest.main()
