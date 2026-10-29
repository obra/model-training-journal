"""The second-checkpoint chart uses the same narrow passive SVG contract."""
import unittest
from scripts.validate import validate_svg, ValidationError

NAME = 'v4-1137-cfr-perplexity.svg'
SAFE = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path d="M0 0 L10 10"/></svg>'


class SecondCheckpointChartPathTests(unittest.TestCase):
    def test_only_explicit_source_and_generated_paths_are_added(self):
        for prefix in ('assets/charts/', 'docs/assets/charts/'):
            validate_svg(SAFE, prefix + NAME)
        for path in ('assets/charts/v4-1138-cfr-perplexity.svg',
                     'assets/charts/v4-1137-overhead.svg',
                     'assets/' + NAME, 'assets/charts/sub/' + NAME,
                     'docs/assets/charts/' + NAME.upper()):
            with self.subTest(path=path), self.assertRaises(ValidationError):
                validate_svg(SAFE, path)

    def test_new_name_does_not_expand_the_passive_profile(self):
        for prefix in ('assets/charts/', 'docs/assets/charts/'):
            for payload in ('<script>alert(1)</script>',
                            '<image href="https://example.com/chart.png"/>',
                            '<path d="M0 0" style="fill:red"/>',
                            '<g onclick="alert(1)"/>',
                            '<use href="https://example.com/chart.svg#x"/>'):
                with self.subTest(path=prefix + NAME, payload=payload), self.assertRaises(ValidationError):
                    validate_svg(SAFE.replace('<path d="M0 0 L10 10"/>', payload), prefix + NAME)


if __name__ == '__main__':
    unittest.main()
