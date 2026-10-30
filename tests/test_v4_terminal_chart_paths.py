"""Terminal chart names retain the existing restricted passive SVG profile."""
import unittest
from scripts.validate import validate_svg,ValidationError

NAMES=('v4-terminal-cfr-perplexity.svg','v4-terminal-overhead.svg')
SAFE='<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path d="M0 0 L10 10"/></svg>'

class TerminalChartPaths(unittest.TestCase):
 def test_only_two_exact_chart_names_in_the_existing_directories(self):
  for name in NAMES:
   for prefix in ('assets/charts/','docs/assets/charts/'):
    try:validate_svg(SAFE,prefix+name)
    except ValidationError as error:self.fail(str(error))
   for path in ('assets/'+name,'assets/charts/sub/'+name,'docs/assets/charts/'+name.upper()):
    with self.subTest(path=path),self.assertRaises(ValidationError):validate_svg(SAFE,path)
  with self.assertRaises(ValidationError):validate_svg(SAFE,'assets/charts/v4-terminal-throughput.svg')

 def test_allowed_names_do_not_expand_active_or_external_content(self):
  for name in NAMES:
   for prefix in ('assets/charts/','docs/assets/charts/'):
    for payload in ('<script>alert(1)</script>','<image href="https://example.com/chart.png"/>',
                    '<path d="M0 0" style="fill:red"/>','<g onclick="alert(1)"/>',
                    '<use href="https://example.com/chart.svg#x"/>'):
     with self.subTest(path=prefix+name,payload=payload),self.assertRaises(ValidationError):
      validate_svg(SAFE.replace('<path d="M0 0 L10 10"/>',payload),prefix+name)

if __name__=='__main__':unittest.main()
