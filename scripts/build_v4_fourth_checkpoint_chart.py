#!/usr/bin/env python3
"""Reproduce the frozen five-point CFR chart using the existing passive SVG helper.

Use scripts/chart-requirements.txt in the existing plotting environment; no network or installs.
"""
from pathlib import Path
import hashlib
import io
import json
import os

from build_v4_first_checkpoint_charts import plt, sanitize, grid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/v4-fourth-checkpoint-2273/cfr-checkpoints.json'
NAME = 'v4-2273-cfr-perplexity.svg'
TITLE = 'Fourth V4 checkpoint: narrow CFR development perplexity'
DESCRIPTION = (
    'Five observations on the same 7,057-label CFR development set. '
    'Stage-local completed valid labels and perplexities: repeated parent baseline 0, '
    '39.776214231484126; checkpoint 569 at 18,604,156, 39.4729645509789; '
    'checkpoint 1,137 at 37,175,835, 38.51235059861212; checkpoint 1,705 '
    'at 55,747,334, 38.54555845078176; checkpoint 2,273 at 74,319,147, '
    '38.17367341486999. The small regression at checkpoint 1,705 is preserved. '
    'Hollow circle is the repeated parent baseline, not a new checkpoint. '
    'The y-axis is restricted to show small changes. Repeated development '
    'evaluation is not sealed holdout or evidence of transferable logic.'
)


def build():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    rows = data['points']
    assert data['schema'] == 'sanitized_v4_cfr_checkpoints_v1'
    assert [r['phase_updates'] for r in rows] == [0, 569, 1137, 1705, 2273]
    assert [r['phase_valid_labels'] for r in rows] == [0, 18604156, 37175835, 55747334, 74319147]
    assert {r['scored_labels'] for r in rows} == {7057}
    assert len({(r['evaluation_manifest_sha256'], r['evaluator_sha256'],
                 r['tokenizer_sha256']) for r in rows}) == 1
    assert len({r['checkpoint_sha256'] for r in rows}) == 5
    assert rows[3]['perplexity'] > rows[2]['perplexity']
    x = [r['phase_valid_labels'] / 1e6 for r in rows]
    y = [r['perplexity'] for r in rows]
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    fig.subplots_adjust(left=.14, right=.96, bottom=.24, top=.80)
    color = '#187eaa'
    ax.plot(x, y, color=color, linewidth=2)
    ax.scatter(x[1:], y[1:], s=65, color=color, zorder=4)
    ax.scatter(x[0], y[0], s=80, facecolor='white', edgecolor=color,
               linewidth=2, zorder=5)
    for row, label, offset, align in zip(
            rows, ['Parent', 'CP569', 'CP1137', 'CP1705', 'CP2273'],
            [(8, 10), (0, 14), (-5, -39), (0, 16), (-5, -39)],
            ['left', 'center', 'center', 'center', 'right']):
        ax.annotate(f"{label}\n{row['perplexity']:.4f}",
                    (row['phase_valid_labels'] / 1e6, row['perplexity']),
                    xytext=offset, textcoords='offset points', ha=align,
                    fontsize=11)
    ax.set_xlim(-3, 79)
    ax.set_ylim(37.7, 40.15)
    ax.set_xticks(x, ['0', '18.60', '37.18', '55.75', '74.32'])
    ax.set_yticks([38.0, 38.5, 39.0, 39.5, 40.0])
    ax.set_xlabel('Completed valid labels within this stage (millions)', labelpad=10)
    ax.set_ylabel('CFR perplexity (restricted axis)', labelpad=8)
    grid(ax)
    fig.suptitle('Fourth checkpoint on the next corpus slice',
                 y=.96, fontsize=14, fontweight='bold')
    fig.text(.14, .865, 'Same 7,057-label CFR development set', fontsize=11)
    fig.text(.14, .115, 'Hollow circle: repeated parent. Four saved checkpoints.', fontsize=10)
    fig.text(.14, .070, 'Small CP1705 regression retained; broader and logic scores have not run here.', fontsize=9)
    fig.text(.14, .030, 'Repeated development result; transferable logic remains unestablished.', fontsize=9)
    preview = os.environ.get('CHART_PREVIEW_DIR')
    if preview:
        target = Path(preview)
        target.mkdir(parents=True, exist_ok=True)
        fig.savefig(target / NAME.replace('.svg', '.png'), dpi=150)
    output = io.BytesIO()
    fig.savefig(output, format='svg', metadata={'Date': None, 'Creator': None})
    plt.close(fig)
    svg, profile = sanitize(output.getvalue(), TITLE, DESCRIPTION)
    destination = ROOT / 'assets/charts' / NAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(svg)
    metadata = {
        'schema': 'sanitized_reproducible_static_chart_v1',
        'input_file': SOURCE.relative_to(ROOT).as_posix(),
        'input_sha256': hashlib.sha256(raw).hexdigest(),
        'builder_file': Path(__file__).relative_to(ROOT).as_posix(),
        'builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'file': destination.relative_to(ROOT).as_posix(),
        'bytes': len(svg), 'sha256': hashlib.sha256(svg).hexdigest(),
        'title': TITLE, 'description': DESCRIPTION,
        'counts': {'observations': 5, 'repeated_parent_baselines': 1,
                   'new_saved_checkpoints': 4, 'scored_labels_per_observation': 7057,
                   'checkpoint1705_regression_preserved': True},
        'passive_svg_profile': profile,
    }
    (destination.parent / 'v4-2273-chart-metadata.json').write_text(
        json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, sort_keys=True))


if __name__ == '__main__':
    build()
