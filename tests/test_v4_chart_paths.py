"""The four frozen V4 chart names retain the existing passive SVG boundary."""
import unittest
from scripts.validate import validate_svg, ValidationError

NAMES = ('v4-569-checkpoint-perplexity.svg', 'v4-569-broader-lm.svg',
         'v4-569-throughput.svg', 'v4-569-overhead.svg')
SAFE = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path d="M0 0 L10 10"/></svg>'


class V4ChartPathTests(unittest.TestCase):
    def test_four_explicit_source_and_generated_paths(self):
        for prefix in ('assets/charts/', 'docs/assets/charts/'):
            for name in NAMES:
                with self.subTest(path=prefix + name):
                    validate_svg(SAFE, prefix + name)

    def test_other_names_and_directories_rejected(self):
        for path in ('assets/charts/v4-570-overhead.svg', 'assets/other/v4-569-overhead.svg',
                     'assets/v4-first-checkpoint-569/v4-569-overhead.svg',
                     'docs/assets/charts/sub/v4-569-overhead.svg'):
            with self.subTest(path=path), self.assertRaises(ValidationError):
                validate_svg(SAFE, path)

    def test_new_paths_do_not_allow_active_or_external_content(self):
        payloads = ('<script>alert(1)</script>', '<image href="https://example.com/x.png"/>',
                    '<g onclick="alert(1)"><path d="M0 0"/></g>',
                    '<use href="https://example.com/x.svg#x"/>')
        for name in NAMES:
            for payload in payloads:
                with self.subTest(name=name, payload=payload), self.assertRaises(ValidationError):
                    validate_svg(SAFE.replace('<path d="M0 0 L10 10"/>', payload), 'assets/charts/' + name)


if __name__ == '__main__':
    unittest.main()
