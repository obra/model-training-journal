"""Hash-bound editorial companions. No network, inference, or silent fallback."""
from hashlib import sha256
from html import escape, unescape
from html.parser import HTMLParser
import re

HEADINGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Blocks(HTMLParser):
    """Keep original slices byte-for-byte instead of reserializing HTML."""
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0]
        for match in re.finditer('\n', source): self.offsets.append(match.end())
        self.stack = []
        self.blocks = []
        self.fragments = []
        self.start = None
        self.kind = None
        self.feed(source)
        self.close()
        if self.stack: raise ValueError('Unclosed original article block')

    def absolute_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def finish(self, end):
        self.blocks.append({'kind': self.kind, 'html': self.source[self.start:end],
                            'text': ' '.join(' '.join(self.fragments).split())})
        self.start = None
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        if not self.stack:
            self.start, self.kind, self.fragments = self.absolute_offset(), tag, []
        if tag not in VOID: self.stack.append(tag)
        elif not self.stack: self.finish(self.absolute_offset() + len(self.get_starttag_text()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID: self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f'Unbalanced original article markup: {tag}')
        self.stack.pop()
        if not self.stack:
            self.finish(self.source.index('>', self.absolute_offset()) + 1)

    def handle_data(self, data):
        if self.stack: self.fragments.append(data)
        elif data.strip(): raise ValueError('Unwrapped article text needs explicit pairing')

    def handle_entityref(self, name): self.handle_data(unescape('&' + name + ';'))
    def handle_charref(self, name): self.handle_data(unescape('&#' + name + ';'))


def split_blocks(html):
    return Blocks(html).blocks


def render_translations(html, data, source_bytes, source_name):
    if set(data) != {'schema', 'source', 'source_sha256', 'blocks'} or data['schema'] != 1:
        raise ValueError(f'{source_name}: unexpected translation schema')
    if data['source'] != source_name or data['source_sha256'] != sha256(source_bytes).hexdigest():
        raise ValueError(f'{source_name}: translation source changed; editorial review required')
    blocks = split_blocks(html)
    paired = [b for b in blocks if b['kind'] not in HEADINGS]
    if len(data['blocks']) != len(paired):
        raise ValueError(f'{source_name}: every substantive block needs exactly one translation')
    for i, (original, translation) in enumerate(zip(paired, data['blocks']), 1):
        if (set(translation) != {'id', 'source_kind', 'source_text_sha256', 'text'} or
                translation['id'] != f'passage-{i:03d}' or
                translation['source_kind'] != original['kind'] or
                translation['source_text_sha256'] != sha256(original['text'].encode()).hexdigest()):
            raise ValueError(f'{source_name}: stale or reordered translation at passage {i}')
        if not isinstance(translation['text'], str) or not translation['text'].strip():
            raise ValueError(f'{source_name}: empty translation at passage {i}')
    result, i = [], 0
    for block in blocks:
        if block['kind'] in HEADINGS:
            result.append(block['html'])
            continue
        translation = data['blocks'][i]
        i += 1
        identity = translation['id']
        paragraphs = ''.join(f'<p>{escape(p.strip())}</p>' for p in translation['text'].split('\n\n') if p.strip())
        result.append(f'''<div class="translation-pair" id="{identity}">
<div class="original-passage" id="original-{identity}"><p class="passage-label"><a href="#plain-{identity}">Original · {i}<span class="visually-hidden"> — jump to plain-language version</span></a></p>{block['html']}</div>
<aside class="plain-passage" id="plain-{identity}" aria-label="Plain-language version of passage {i}"><p class="passage-label"><a href="#original-{identity}">In plain language · {i}<span class="visually-hidden"> — back to original</span></a></p>{paragraphs}</aside>
</div>''')
    return '\n'.join(result)
