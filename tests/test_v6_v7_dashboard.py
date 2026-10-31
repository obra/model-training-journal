"""Keep catch-up scores distinct from history, work counts and unused budget."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import dashboard


class CatchupContracts(unittest.TestCase):
    def data(self):
        return json.loads((ROOT / 'assets/v6-v7-cfr-checkpoints.json').read_text())

    def test_twelve_points_preserve_terminal_and_regressions(self):
        self.assertTrue(hasattr(dashboard, 'validate_catchup'))
        data = self.data()
        dashboard.validate_catchup(data)
        v6, v7 = data['stages']
        self.assertEqual([len(s['points']) for s in data['stages']], [6, 6])
        self.assertEqual(v6['points'][-1]['perplexity'], 34.188756272700275)
        self.assertEqual(v7['points'][-1]['perplexity'], 33.882335618048806)
        self.assertGreater(v6['points'][1]['perplexity'], v6['points'][0]['perplexity'])
        self.assertGreater(v7['points'][-1]['perplexity'], v7['points'][-2]['perplexity'])
        self.assertEqual(v7['points'][-1]['valid_labels'], 45021370)
        self.assertEqual(v7['points'][-1]['model_lineage_valid_labels'], 1070817348)
        self.assertEqual(v7['points'][-1]['physical_valid_labels'], 1073475742)
        self.assertEqual(data['evaluation_budget']['new_nonrefundable_charge_seconds'], 3600)
        self.assertAlmostEqual(data['evaluation_budget']['score_guard_seconds'], 131.66023921966553)

    def test_mixed_panel_missing_terminal_and_nonfinite_scores_fail(self):
        self.assertTrue(hasattr(dashboard, 'validate_catchup'))
        for change in ('denominator', 'terminal', 'nonfinite', 'population'):
            data = deepcopy(self.data())
            if change == 'denominator': data['scoring_contract']['scored_labels'] = 130209
            elif change == 'terminal': data['stages'][1]['points'].pop()
            elif change == 'nonfinite': data['stages'][0]['points'][0]['perplexity'] = float('nan')
            else: data['scoring_contract']['population'] = 'reasoning'
            with self.subTest(change=change), self.assertRaises(ValueError):
                dashboard.validate_catchup(data)

    def test_stage_panels_and_latest_summary_use_new_source(self):
        self.assertIn('cfr-v6', dashboard.CHART_IDS)
        self.assertIn('cfr-v7', dashboard.CHART_IDS)
        import build
        data = dashboard.load_dashboard(ROOT, build.load_posts())
        self.assertEqual(data['summary']['language']['stage'], 'V7 terminal')
        self.assertEqual(data['summary']['training']['value'], 45021370)
        self.assertEqual(data['terminal_v5']['perplexity'], 34.2885)
        panels = dashboard.chart_definitions(data)
        for stage in ('v6', 'v7'):
            panel = next(p for p in panels if p['id'] == 'cfr-' + stage)
            self.assertEqual(len(panel['rows']), 6)
            self.assertTrue(all(r['denominator'] == 7057 for r in panel['rows']))
            self.assertTrue(all(r['checkpoint_time_utc'] is None for r in panel['rows']))
            self.assertEqual(panel['source'], 'assets/v6-v7-cfr-checkpoints.json')


if __name__ == '__main__':
    unittest.main()
