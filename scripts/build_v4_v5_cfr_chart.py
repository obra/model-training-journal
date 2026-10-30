#!/usr/bin/env python3
"""Reproduce a passive, stage-local CFR chart from published aggregate JSON."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/v4-v5-cfr-checkpoints.json'
OUTPUT = ROOT / 'assets/charts/v4-v5-cfr-perplexity.svg'
WIDTH, HEIGHT = 820, 390
LEFT, RIGHT, TOP, BOTTOM = 58, 25, 28, 50
Y_MIN, Y_MAX = 34.0, 38.2
X_MAX = 125_320_085


def point(row):
    x = LEFT + row['valid_labels'] / X_MAX * (WIDTH - LEFT - RIGHT)
    y = TOP + (Y_MAX - row['perplexity']) / (Y_MAX - Y_MIN) * (HEIGHT - TOP - BOTTOM)
    return x, y


def build():
    data = json.loads(SOURCE.read_text())
    assert data['schema'] == 'sanitized_v4_v5_cfr_checkpoints_v1'
    assert data['panel'] == 'fixed_cfr_development_7057_labels'
    stages = data['stages']
    assert [stage['id'] for stage in stages] == ['v4_second_slice_completed', 'v5_running_slice']
    assert [[p['updates'] for p in stage['points']] for stage in stages] == [
        [0, 569, 1137, 1705, 2273, 2841, 3408],
        [0, 639, 1278, 1917, 2556, 3195],
    ]
    for stage in stages:
        rows = stage['points']
        assert rows[0]['role'] == 'repeated_parent' and rows[0]['valid_labels'] == 0
        assert all(0 <= p['valid_labels'] <= X_MAX and Y_MIN <= p['perplexity'] <= Y_MAX for p in rows)
        assert all(a['valid_labels'] < b['valid_labels'] for a, b in zip(rows, rows[1:]))
    assert stages[0]['points'][-1]['perplexity'] == stages[1]['points'][0]['perplexity']

    title = 'CFR development perplexity across two separate corpus slices'
    description = ('Blue: completed second V4 slice, parent 37.7860 to terminal 35.9212, '
                   'with a regression at checkpoint 2841. Green: running V5 slice, '
                   'repeated parent 35.9212 to checkpoint 3195 at 34.5556. '
                   'Horizontal positions are valid labels within each separate slice, '
                   'not cumulative training. Same 7057-label development panel; '
                   'lower is better. No reasoning or sealed-holdout result.')
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
             f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="chart-title chart-description">',
             f'<title id="chart-title">{escape(title)}</title>',
             f'<desc id="chart-description">{escape(description)}</desc>',
             f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>']
    for value in (34, 35, 36, 37, 38):
        y = point({'valid_labels': 0, 'perplexity': value})[1]
        parts.append(f'<path d="M {LEFT} {y:.2f} L {WIDTH-RIGHT} {y:.2f}" '
                     'fill="none" stroke="#dce5e9" stroke-width="1"/>')
    parts.append(f'<path d="M {LEFT} {TOP} L {LEFT} {HEIGHT-BOTTOM} L {WIDTH-RIGHT} {HEIGHT-BOTTOM}" '
                 'fill="none" stroke="#60717e" stroke-width="1.5"/>')
    for stage, color in zip(stages, ('#246c9a', '#168274')):
        positions = [point(row) for row in stage['points']]
        route = ' '.join((('M' if i == 0 else 'L') + f' {x:.2f} {y:.2f}')
                         for i, (x, y) in enumerate(positions))
        parts.append(f'<path d="{route}" fill="none" stroke="{color}" stroke-width="3"/>')
        for index, (x, y) in enumerate(positions):
            size = 8 if index else 10
            fill = color if index else '#ffffff'
            parts.append(f'<rect x="{x-size/2:.2f}" y="{y-size/2:.2f}" width="{size}" '
                         f'height="{size}" fill="{fill}" stroke="{color}" stroke-width="2"/>')
    parts.append('</svg>')
    OUTPUT.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    print(OUTPUT.relative_to(ROOT))


if __name__ == '__main__':
    build()
