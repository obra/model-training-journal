"""Dashboard uses evidence, not duplicated headline numbers or inferred zeros."""
import importlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


class DashboardTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('dashboard'), 'Shared dashboard model is missing')
        return importlib.import_module('dashboard')

    def model(self):
        import build
        return self.module().load_dashboard(ROOT, build.load_posts())

    def test_current_summary_uses_terminal_point_and_keeps_reasoning_separate(self):
        d = self.model()
        self.assertEqual(d['summary']['language']['value'], 33.882335618048806)
        self.assertEqual(d['summary']['language']['denominator'], 7057)
        self.assertEqual(d['summary']['training']['value'], 45021370)
        self.assertEqual(d['summary']['training']['status'], 'completed')
        self.assertEqual(d['summary']['task']['value'], 0)
        self.assertEqual(d['summary']['task']['denominator'], 32)
        self.assertEqual(d['summary']['task']['stage'], 'admitted_v3_stage2')
        self.assertIsNone(d['summary']['language']['checkpoint_time_utc'])

    def test_all_historical_rows_survive_without_pooled_panels(self):
        d = self.model()
        self.assertEqual(len(d['tables']), 44)
        self.assertEqual(len(d['history']['evaluation_points']), 42)
        self.assertEqual(len(d['history']['v4_progress_observations']), 594)
        self.assertEqual(len(d['history']['stage2_observations']), 22)
        self.assertEqual(len(d['history']['unrun_evaluations']), 26)
        self.assertEqual(len(d['later_slices']['stages'][-1]['points']), 7)
        self.assertTrue(all(row['perplexity'] is None for row in d['history']['unrun_evaluations']))
        self.assertTrue(all(row['value'] is None for row in d['unrun']))
        self.assertGreater(d['later_slices']['stages'][0]['points'][5]['perplexity'],
                           d['later_slices']['stages'][0]['points'][4]['perplexity'])

    def test_numeric_cells_do_not_turn_status_versions_or_ranges_into_values(self):
        m = self.module()
        for value in ['not run', '', '3.14.4', 'At least 80%', '0/0', '13–16']:
            with self.subTest(value=value): self.assertIsNone(m.numeric_cell(value))
        self.assertEqual(m.numeric_cell('0/32'), {'value': 0.0, 'denominator': 32.0, 'display': '0/32'})
        self.assertEqual(m.numeric_cell('125,320,085'), {'value': 125320085.0, 'denominator': None, 'display': '125,320,085'})

    def test_rendered_summary_and_dashboard_have_same_value_and_source(self):
        m = self.module(); d = self.model()
        summary, page = m.render_summary(d), m.render_dashboard(d)
        for html in (summary, page):
            self.assertIn('33.8823', html)
            self.assertIn('7,057', html)
            self.assertIn('0/32', html)
            self.assertIn('Not run', html)
        self.assertIn('Ledger correction', page)
        self.assertIn('<caption>', page)
        self.assertNotIn('<script', page)

    def test_line_chart_retains_null_gaps_and_has_readable_axis_labels(self):
        m = self.module()
        svg = m.line_svg('Test', 'Targets', 'Loss', [{'label':'a','x':0,'y':5}, {'label':'b','x':1,'y':None}, {'label':'c','x':2,'y':3}])
        self.assertIn('Targets', svg)
        self.assertIn('Loss', svg)
        self.assertIn('Missing values are gaps', svg)
        self.assertNotIn('nan', svg.lower())
        self.assertEqual(svg.count('id="series-line-'), 2)


if __name__ == '__main__': unittest.main()

class DashboardEvidenceContracts(unittest.TestCase):
    def test_missing_values_have_no_bar_but_real_zero_does(self):
        import dashboard
        html = dashboard.bars('Count', ['Missing', 'Measured zero'], ['Not recorded', '0'])
        self.assertEqual(html.count('<meter '), 1)
        self.assertIn('value="0.0"', html)
        self.assertIn('No bar', html)
        self.assertIn('Not recorded', html)
    def test_source_snapshot_is_not_fabricated_checkpoint_time(self):
        import dashboard, build
        panels=dashboard.chart_definitions(dashboard.load_dashboard(ROOT,build.load_posts()))
        p=next(p for p in panels if p['id']=='cfr-v5')
        self.assertTrue(all(r['checkpoint_time_utc'] is None for r in p['rows']))
        self.assertTrue(all(r['observed_utc'] is None and r['snapshot_utc']=='2026-10-30T17:14:12Z' for r in p['rows'][:-1]))
        self.assertEqual(p['rows'][-1]['observed_utc'],'2026-10-30T17:39:43Z')
    def test_table_values_keep_full_reported_precision(self):
        import dashboard
        self.assertEqual(dashboard.number(35.921232002527105),'35.921232002527105')
        self.assertEqual(dashboard.number(None),'Not recorded')
