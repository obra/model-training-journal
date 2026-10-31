"""Reader-facing correspondence, stale-copy refusal, and original preservation."""
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


class TranslationTests(unittest.TestCase):
    def test_every_published_post_gets_a_complete_companion(self):
        import build
        posts = build.load_posts()
        self.assertEqual(len(posts), 48)
        for post in posts:
            with self.subTest(post=post['slug']):
                self.assertIn('parallel_html', post)
                self.assertGreater(post['parallel_html'].count('class="translation-pair"'), 0)

    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('legibility'), 'Translation renderer is missing')
        return importlib.import_module('legibility')

    def fixture(self, directory):
        source = Path(directory) / 'post.md'
        source.write_text('Original source\n')
        html = '<h2 id="test">A heading</h2>\n<p>Zero <strong>0/32</strong> &amp; unknown.</p>\n<ul><li>One</li><li>Two</li></ul>'
        texts = ['Zero 0/32 & unknown.', 'One Two']
        data = {'schema': 1, 'source': 'content/posts/post.md',
                'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'blocks': [{'id': f'passage-{i:03d}', 'source_kind': tag,
                            'source_text_sha256': hashlib.sha256(text.encode()).hexdigest(),
                            'text': translation}
                           for i, (tag, text, translation) in enumerate(zip(
                               ['p', 'ul'], texts, ['Zero correct; unknown is not zero.', 'The list has one and two.']), 1)]}
        return source, html, data

    def test_pairs_preserve_original_markup_and_reading_order(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as d:
            source, html, data = self.fixture(d)
            result = m.render_translations(html, data, source.read_bytes(), 'content/posts/post.md')
        self.assertIn('<h2 id="test">A heading</h2>', result)
        self.assertIn('<p>Zero <strong>0/32</strong> &amp; unknown.</p>', result)
        self.assertIn('<ul><li>One</li><li>Two</li></ul>', result)
        self.assertLess(result.index('Zero <strong>'), result.index('Zero correct'))
        self.assertLess(result.index('Zero correct'), result.index('<ul>'))
        self.assertEqual(result.count('class="translation-pair"'), 2)
        self.assertIn('href="#original-passage-001"', result)

    def test_missing_extra_reordered_or_stale_copy_fails(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as d:
            source, html, data = self.fixture(d)
            for change in ('missing', 'extra', 'reorder', 'source', 'block'):
                altered = json.loads(json.dumps(data)); body = html; raw = source.read_bytes()
                if change == 'missing': altered['blocks'].pop()
                if change == 'extra': altered['blocks'].append(altered['blocks'][0])
                if change == 'reorder': altered['blocks'].reverse()
                if change == 'source': raw += b'Changed'
                if change == 'block': body = body.replace('unknown.', 'known.')
                with self.subTest(change=change), self.assertRaises(ValueError):
                    m.render_translations(body, altered, raw, 'content/posts/post.md')

    def test_plain_copy_is_escaped_and_empty_copy_rejected(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as d:
            source, html, data = self.fixture(d)
            data['blocks'][0]['text'] = '<script>alert(1)</script>'
            result = m.render_translations(html, data, source.read_bytes(), 'content/posts/post.md')
            self.assertNotIn('<script>', result)
            self.assertIn('&lt;script&gt;', result)
            data['blocks'][0]['text'] = '  '
            with self.assertRaises(ValueError): m.render_translations(html, data, source.read_bytes(), 'content/posts/post.md')

    def test_nested_tables_and_void_images_are_one_complete_block(self):
        m = self.module()
        markup = '<p>First<br />next</p><div class="table-scroll"><table><tr><td>3</td></tr></table></div><figure><img src="x" alt="X"><figcaption>Caption</figcaption></figure>'
        blocks = m.split_blocks(markup)
        self.assertEqual([b['kind'] for b in blocks], ['p', 'div', 'figure'])
        self.assertEqual(''.join(b['html'] for b in blocks), markup)
        self.assertEqual(blocks[0]['text'], 'First next')
        self.assertEqual(blocks[2]['text'], 'Caption')


if __name__ == '__main__': unittest.main()
