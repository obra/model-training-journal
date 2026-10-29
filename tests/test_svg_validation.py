"""The four reviewed passive chart assets; synthetic private fixtures only."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(os.environ.get(
    "SVG_VALIDATOR_SOURCE", str(Path(__file__).resolve().parents[1] / "scripts/validate.py")))
SPEC = importlib.util.spec_from_file_location("svg_validator_fixture", SOURCE)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

CHARTS = ("checkpoint-perplexity.svg", "broader-panel.svg",
          "training-throughput.svg", "checkpoint-overhead.svg")
SVG = '''<svg xmlns="http://www.w3.org/2000/svg"
 xmlns:xlink="http://www.w3.org/1999/xlink" width="80pt" height="30pt"
 viewBox="0 0 80 30" version="1.1" role="img" aria-labelledby="chart-title chart-desc">
 <title id="chart-title">Measured checkpoints</title>
 <desc id="chart-desc">Synthetic chart fixture.</desc>
 <defs><path id="glyph" d="M 0 0 L 10 0 L 10 10 Z" transform="scale(0.015625)"/>
 <clipPath id="clip"><rect x="0" y="0" width="80" height="30"/></clipPath></defs>
 <g clip-path="url(#clip)" transform="translate(1 2) scale(1 -1)" fill="#123456"
 stroke="#000000" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="miter"
 stroke-miterlimit="4" stroke-dasharray="3.7,1.6" stroke-dashoffset="0"
 fill-opacity="0.9" stroke-opacity="0.8" opacity="1">
 <use xlink:href="#glyph" x="10" y="20"/></g></svg>'''


class SVGValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "assets/charts").mkdir(parents=True)
        (self.root / "docs/assets/charts").mkdir(parents=True)
        (self.root / "docs/.nojekyll").touch()
        (self.root / "docs/index.html").write_text(
            '<img src="/model-training-journal/assets/charts/checkpoint-perplexity.svg" '
            'alt="Measured checkpoint chart">', encoding="utf-8")
        self.write(SVG)

    def write(self, text, name=CHARTS[0]):
        for prefix in ("assets/charts", "docs/assets/charts"):
            (self.root / prefix / name).write_text(text, encoding="utf-8")

    def rejected(self, text):
        self.write(text)
        with self.assertRaises(validator.ValidationError):
            validator.candidate(self.root)

    def accepted(self):
        try:
            return validator.validate(self.root)
        except validator.ValidationError as exc:
            self.fail(f"Reviewed passive chart fixture was rejected: {exc}")

    def test_four_named_external_charts_allow_glyph_paths_and_local_clips(self):
        for name in CHARTS:
            self.write(SVG, name)
        hashes = self.accepted()
        for name in CHARTS:
            self.assertIn("assets/charts/" + name, hashes)
            self.assertEqual(hashes["assets/charts/" + name],
                             hashes["docs/assets/charts/" + name])

    def test_standard_xml_declaration_and_unprefixed_local_href_are_allowed(self):
        self.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n' +
                   SVG.replace('xlink:href="#glyph"', 'href="#glyph"'))
        self.accepted()

    def test_unknown_chart_names_paths_and_case_are_rejected(self):
        for name in ("assets/charts/other.svg", "assets/checkpoint-perplexity.svg",
                     "docs/checkpoint-perplexity.svg", "content/checkpoint-perplexity.svg",
                     "assets/charts/nested/checkpoint-perplexity.svg"):
            with self.subTest(name=name):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(SVG, encoding="utf-8")
                with self.assertRaises(validator.ValidationError):
                    validator.candidate(self.root)
                path.unlink()
        path = self.root / "assets/charts" / CHARTS[0]
        path.unlink()
        path.with_suffix(".SVG").write_text(SVG, encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.candidate(self.root)

    def test_active_tags_events_styles_and_unknown_attributes_are_rejected(self):
        for markup in ('<script>alert(1)</script>', '<style>path{fill:red}</style>',
                       '<image href="https://example.org/image.png"/>', '<a href="#glyph"/>',
                       '<foreignObject><p>HTML</p></foreignObject>', '<animate/>',
                       '<animateTransform/>', '<set/>', '<text>Text outside the path profile</text>',
                       '<metadata>Unreviewed metadata</metadata>', '<svg/>'):
            with self.subTest(markup=markup):
                self.rejected(SVG.replace('</svg>', markup + '</svg>'))
        for attr in ('onload="alert(1)"', 'style="fill:red"', 'filter="url(#clip)"',
                     'xml:base="https://example.org/"', 'data-extra="unreviewed"'):
            with self.subTest(attr=attr):
                self.rejected(SVG.replace('version="1.1"', 'version="1.1" ' + attr))

    def test_external_data_and_disguised_resource_references_are_rejected(self):
        for href in ('https://example.org/x.svg#glyph', '//example.org/x.svg#glyph',
                     'data:image/svg+xml,ignored', 'javascript:alert(1)',
                     '&#x68;ttps://example.org/x.svg#glyph', ' #glyph', '#missing'):
            with self.subTest(href=href):
                self.rejected(SVG.replace('xlink:href="#glyph"', 'xlink:href="' + href + '"'))
        for attr in ('fill="url(#glyph)"', 'fill="url(https://example.org/paint)"',
                     'clip-path="url(https://example.org/x.svg#clip)"',
                     'clip-path="url(data:text/plain,ignored)"', 'clip-path="url(#missing)"'):
            with self.subTest(attr=attr):
                before = 'clip-path="url(#clip)"' if attr.startswith('clip-path') else 'fill="#123456"'
                self.rejected(SVG.replace(before, attr))

    def test_doctypes_entities_and_nonstandard_processing_instructions_are_rejected(self):
        for prolog in ('<!DOCTYPE svg>',
                       '<!DOCTYPE svg SYSTEM "https://example.org/external.dtd">',
                       '<!DOCTYPE svg [<!ENTITY chart "expanded">]>',
                       '<!ENTITY chart "expanded">',
                       '<?xml-stylesheet href="https://example.org/style.css"?>',
                       '<?chart anything?>'):
            with self.subTest(prolog=prolog):
                self.rejected(prolog + SVG)
        self.rejected(SVG.replace('</svg>', '<?xml version="1.0"?></svg>'))

    def test_unknown_namespaces_duplicate_ids_and_reference_ambiguities_are_rejected(self):
        for text in (SVG.replace('http://www.w3.org/2000/svg', 'https://example.org/not-svg'),
                     SVG.replace('version="1.1"', 'version="1.1" xmlns:other="https://example.org/ns"'),
                     SVG.replace('id="chart-title"', 'id="glyph"'),
                     SVG.replace('xlink:href="#glyph"', 'xlink:href="#glyph" href="#glyph"'),
                     SVG.replace('xlink:href="#glyph"', 'id="loop" xlink:href="#loop"'),
                     SVG.replace('aria-labelledby="chart-title chart-desc"',
                                 'aria-labelledby="chart-title missing"'),
                     SVG.replace('url(#clip)', 'url(#glyph)')):
            with self.subTest(text=text[:70]):
                self.rejected(text)

    def test_geometry_is_bounded_numeric_and_cannot_hide_paint_urls(self):
        for before, after in [('width="80pt"', 'width="NaN"'),
                              ('height="30pt"', 'height="-1pt"'),
                              ('viewBox="0 0 80 30"', 'viewBox="0 0 80"'),
                              ('opacity="1"', 'opacity="2"'),
                              ('scale(0.015625)', 'scale(url(#glyph))'),
                              ('d="M 0 0 L 10 0 L 10 10 Z"', 'd="url(#glyph)"')]:
            with self.subTest(after=after):
                self.rejected(SVG.replace(before, after))
        self.rejected(SVG.replace('</svg>', '<g/>' * 25001 + '</svg>'))
        self.rejected(SVG.replace('</svg>', '<g>' * 70 + '</g>' * 70 + '</svg>'))

    def test_svg_still_requires_utf8_size_limit_and_private_term_review(self):
        self.accepted()
        source = self.root / "assets/charts" / CHARTS[0]
        for data in (b'\xff', b'\x00', b'x' * 1_000_001):
            with self.subTest(size=len(data)):
                source.write_bytes(data)
                with self.assertRaises(validator.ValidationError):
                    validator.candidate(self.root)
        self.write(SVG.replace('Synthetic chart fixture.', 'fixture-private-host'))
        with self.assertRaisesRegex(validator.ValidationError, 'private review term'):
            validator.candidate(self.root, ['fixture-private-host'])

    def test_generated_chart_copy_must_match_and_have_its_source(self):
        generated = self.root / "docs/assets/charts" / CHARTS[0]
        generated.write_text(SVG.replace('Measured checkpoints', 'Changed copy'), encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(self.root)
        self.write(SVG)
        (self.root / "assets/charts" / CHARTS[0]).unlink()
        with self.assertRaises(validator.ValidationError):
            validator.validate(self.root)

    def test_external_asset_exception_does_not_allow_inline_svg_or_active_html(self):
        for markup in ('<svg xmlns="http://www.w3.org/2000/svg"></svg>',
                       '<script>alert(1)</script>', '<style>p{color:red}</style>',
                       '<p style="color:red">Inline CSS</p>'):
            with self.subTest(markup=markup):
                (self.root / "docs/index.html").write_text(markup, encoding="utf-8")
                with self.assertRaises(validator.ValidationError):
                    validator.validate(self.root)


if __name__ == "__main__":
    unittest.main()
