#!/usr/bin/env python3
"""Reproduce the frozen three-point CFR chart using the existing passive SVG helper.

Run with the versions in scripts/chart-requirements.txt; no network or installs.
"""
from pathlib import Path
import hashlib
import io
import json
import os

from build_v4_first_checkpoint_charts import plt, sanitize, grid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/v4-second-checkpoint-1137/cfr-checkpoints.json'
NAME = 'v4-1137-cfr-perplexity.svg'
TITLE = 'Second V4 checkpoint: narrow CFR development perplexity'
DESCRIPTION = (
    'Three observations on the same 7,057-label CFR development set. '
    'Stage-local completed valid labels: parent baseline 0, checkpoint 569 '
    '18,604,156, checkpoint 1,137 37,175,835. Perplexities respectively '
    '39.776214231484126, 39.4729645509789, 38.51235059861212. '
    'Hollow circle is the repeated parent baseline, not a new checkpoint. '
    'The y-axis is restricted to show a small change. Repeated development '
    'evaluation is not sealed holdout or evidence of transferable logic.'
)


def build():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    rows = data['points']
    assert data['schema'] == 'sanitized_v4_cfr_checkpoints_v1'
    assert [r['phase_updates'] for r in rows] == [0, 569, 1137]
    assert [r['phase_valid_labels'] for r in rows] == [0, 18604156, 37175835]
    assert {r['scored_labels'] for r in rows} == {7057}
    assert len({(r['evaluation_manifest_sha256'], r['evaluator_sha256'],
                 r['tokenizer_sha256']) for r in rows}) == 1
    assert len({r['checkpoint_sha256'] for r in rows}) == 3
    x = [r['phase_valid_labels'] / 1e6 for r in rows]
    y = [r['perplexity'] for r in rows]
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    fig.subplots_adjust(left=.14, right=.96, bottom=.23, top=.80)
    color = '#187eaa'
    ax.plot(x, y, color=color, linewidth=2)
    ax.scatter(x[1:], y[1:], s=65, color=color, zorder=4)
    ax.scatter(x[0], y[0], s=80, facecolor='white', edgecolor=color,
               linewidth=2, zorder=5)
    for row, label, offset, align in zip(
            rows, ['Parent baseline', 'CP569', 'CP1137'],
            [(12, 12), (0, 14), (-8, 40)], ['left', 'center', 'right']):
        ax.annotate(f"{label}\n{row['perplexity']:.4f}",
                    (row['phase_valid_labels'] / 1e6, row['perplexity']),
                    xytext=offset, textcoords='offset points', ha=align,
                    fontsize=11)
    ax.set_xlim(-2, 40)
    ax.set_ylim(38.25, 40.16)
    ax.set_xticks(x, ['0', '18.60', '37.18'])
    ax.set_yticks([38.5, 39.0, 39.5, 40.0])
    ax.set_xlabel('Stage-local completed valid labels (millions)', labelpad=10)
    ax.set_ylabel('CFR perplexity (restricted axis)', labelpad=8)
    grid(ax)
    fig.suptitle('Second checkpoint on the next corpus slice',
                 y=.96, fontsize=14, fontweight='bold')
    fig.text(.14, .865, 'Same 7,057-label CFR development set', fontsize=11)
    fig.text(.14, .075, 'Hollow circle: repeated parent baseline. Two new saved checkpoints.',
             fontsize=9)
    fig.text(.14, .035, 'Narrow development result; broader and logic evaluations have not run here.',
             fontsize=9)
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
        'counts': {'observations': 3, 'repeated_parent_baselines': 1,
                   'new_saved_checkpoints': 2, 'scored_labels_per_observation': 7057},
        'passive_svg_profile': profile,
    }
    (destination.parent / 'v4-1137-chart-metadata.json').write_text(
        json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, sort_keys=True))


if __name__ == '__main__':
    build()
