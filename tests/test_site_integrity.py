"""Check rendered correspondence and data routes without a browser dependency."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build
import dashboard
import legibility
import validate

class SiteIntegrity(unittest.TestCase):
    def test_every_original_block_and_heading_survives_exactly(self):
        for post in build.load_posts():
            for block in legibility.split_blocks(post['html']):
                with self.subTest(source=post['source'], text=block['text'][:40]):
                    self.assertIn(block['html'],post['parallel_html'])
    def test_table_provenance_matches_source_bytes(self):
        data=dashboard.load_dashboard(build.ROOT,build.load_posts())
        for table in data['tables']:
            self.assertEqual(table['source_sha256'],sha256((build.ROOT/table['source']).read_bytes()).hexdigest())
    def test_all_generated_routes_assets_and_anchors_validate(self):
        validate.validate_html(build.ROOT)
    def test_every_chart_is_covered_by_passive_asset_profile(self):
        data=dashboard.load_dashboard(build.ROOT,build.load_posts())
        for panel in dashboard.chart_definitions(data):
            svg=dashboard.line_svg(panel['title'],panel['x_label'],panel['y_label'],panel['rows'])
            validate.validate_svg(svg,'assets/charts/dashboard-'+panel['id']+'.svg')
