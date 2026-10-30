"""Readable SVG labels do not broaden the existing frozen-chart policy."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import dashboard
import validate

class DashboardSvgTests(unittest.TestCase):
    def svg(self):
        return dashboard.line_svg('Measured text', 'Targets', 'Loss', [{'x':0,'y':2}, {'x':3,'y':1}])
    def test_generated_labeled_chart_is_passive(self):
        validate.validate_svg(self.svg(), 'assets/charts/dashboard-cfr-v5.svg')
    def test_old_chart_profile_still_rejects_text(self):
        with self.assertRaises(validate.ValidationError):
            validate.validate_svg(self.svg(), 'assets/charts/checkpoint-perplexity.svg')
    def test_new_chart_profile_rejects_active_or_unbounded_text(self):
        for mutation in ['<text onclick="alert(1)"', '<text href="https://example.com"', '<text font-size="1000000"', '<text font-family="url(https://example.com)"']:
            with self.subTest(mutation=mutation), self.assertRaises(validate.ValidationError):
                validate.validate_svg(self.svg().replace('<text', mutation, 1), 'assets/charts/dashboard-cfr-v5.svg')
        for markup in ['<script/>','<foreignObject/>','<image href="https://example.com"/>','<text><a>bad</a></text>']:
            with self.subTest(markup=markup), self.assertRaises(validate.ValidationError):
                validate.validate_svg(self.svg().replace('</svg>', markup+'</svg>'), 'assets/charts/dashboard-cfr-v5.svg')
