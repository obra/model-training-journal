"""Compile public evidence once for the dashboard, charts, tables and home cards."""
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import json
import math
import re

BASE = '/model-training-journal'
STAGES = {
    'science_104521471': ('science', 'Scientific prose'),
    'filtered_96012838': ('filtered', 'Filtered continuation'),
    'admitted_143m_continuation': ('expansion', 'Wiki / Stack expansion'),
    'admitted_v3_stage1': ('v3-stage1', 'V3 · first stage'),
    'admitted_v3_stage2': ('v3-stage2', 'V3 · second stage'),
    'admitted_v4_tranche1': ('v4-first', 'V4 · first slice'),
}
PROGRESS_METRICS = {
    'phase_valid_labels': 'Completed usable predictions in this slice',
    'phase_charged_valid_labels': 'Charged predictions in this slice',
    'phase_processed_ids': 'Completed input IDs in this slice',
    'phase_charged_processed_ids': 'Charged input IDs in this slice',
    'phase_updates': 'Completed training steps in this slice',
    'phase_charged_microbatches': 'Charged small batches in this slice',
    'model_lineage_valid_labels': 'Predictions retained in the model lineage',
    'model_lineage_processed_ids': 'Input IDs retained in the model lineage',
    'model_lineage_updates': 'Steps retained in the model lineage',
    'physical_valid_labels': 'All physical campaign predictions',
    'physical_processed_ids': 'All physical campaign input IDs',
    'physical_updates': 'All physical campaign steps',
    'charged_cap_valid_labels': 'Predictions charged against the campaign cap',
    'failed_reserved_valid_labels': 'Earlier failed reservations still charged',
    'guard_elapsed_seconds': 'Elapsed guard time · seconds',
    'interval_seconds': 'Length of each observation interval · seconds',
    'interval_charged_valid_labels_per_wall_second': 'Charged predictions per interval second',
    'interval_completed_valid_labels_per_wall_second': 'Completed predictions per interval second',
    'startup_inclusive_charged_labels_per_guard_second': 'Charged predictions per guard second, including startup',
}
TIMING_METRICS = {
    'training_loop_elapsed_seconds': 'Training-loop time · seconds',
    'worker_elapsed_seconds': 'Worker elapsed time · seconds',
    'guard_wall_seconds': 'Guard elapsed time · seconds',
    'checkpoint_hook_seconds': 'Model-saving work · seconds',
    'evaluation_hook_seconds': 'Evaluation work · seconds',
    'training_seconds_excluding_measured_hooks': 'Loop time excluding measured saves and checks · seconds',
    'valid_labels_per_loop_second': 'Usable predictions per loop second',
    'valid_labels_per_worker_second': 'Usable predictions per worker second',
    'valid_labels_per_guard_wall_second': 'Usable predictions per guard second',
    'processed_ids_per_loop_second': 'Processed input IDs per loop second',
    'checkpoint_plus_evaluation_fraction_of_loop': 'Saving and evaluation share of loop time',
    'phase_valid_labels': 'Completed usable predictions',
    'phase_processed_ids': 'Completed input IDs',
}
CHART_IDS = ([f'cfr-{value[0]}' for value in STAGES.values()] + ['cfr-v4-second', 'cfr-v5', 'broader', 'v4-boundary-overhead'] +
             ['progress-' + key.replace('_', '-') for key in PROGRESS_METRICS])
DASHBOARD_CHART_NAMES = frozenset('dashboard-' + key + '.svg' for key in CHART_IDS)


def numeric_cell(text):
    """Parse only explicit scalars or fractions, never versions, targets or ranges."""
    clean = text.strip().replace(',', '')
    match = re.fullmatch(r'([+-]?\d+(?:\.\d+)?)(?:/(\d+(?:\.\d+)?))?(?: (?:seconds|labels|tokens|steps|bytes|GiB))?', clean)
    if not match: return None
    value = float(match[1]); denominator = float(match[2]) if match[2] else None
    if not math.isfinite(value) or (denominator is not None and (denominator <= 0 or value < 0 or value > denominator)):
        return None
    return {'value': value, 'denominator': denominator, 'display': text}


class Tables(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.tables, self.rows, self.row, self.cell = [], None, None, None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'table': self.rows = []
        elif tag == 'tr' and self.rows is not None: self.row = []
        elif tag in {'td', 'th'} and self.row is not None: self.cell = []

    def handle_data(self, text):
        if self.cell is not None: self.cell.append(text)

    def handle_endtag(self, tag):
        if tag in {'td', 'th'} and self.cell is not None:
            self.row.append(' '.join(' '.join(self.cell).split())); self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None
        elif tag == 'table' and self.rows is not None:
            self.tables.append(self.rows); self.rows = None


def load_dashboard(root, posts):
    config = json.loads((root / 'content/dashboard.json').read_text())
    if config['schema'] != 1: raise ValueError('Unsupported dashboard schema')
    sources = []
    def read(path):
        if not re.fullmatch(r'(?:assets|content)/[a-zA-Z0-9_./-]+\.json', path) or '..' in path.split('/'):
            raise ValueError('Dashboard source must be a public local JSON file')
        raw = (root / path).read_bytes()
        sources.append({'path': path, 'sha256': sha256(raw).hexdigest()})
        return json.loads(raw)
    history = read(config['history_source'])
    later = read(config['later_slices_source'])
    read('content/dashboard.json')
    terminal = config['terminal_v5']
    if terminal['status'] != 'completed' or terminal['scored_labels'] != 7057 or terminal['checkpoint_time_utc'] is not None:
        raise ValueError('Terminal evidence requires its explicit status and time semantics')
    for name in ('updates', 'valid_labels', 'processed_input_tokens', 'scored_labels'):
        if type(terminal[name]) is not int or terminal[name] <= 0: raise ValueError('Positive terminal counts required')
    for name in ('perplexity', 'mean_token_nll_nats', 'checkpoint_plus_evaluation_percent_of_loop'):
        if type(terminal[name]) not in (int, float) or not math.isfinite(terminal[name]) or terminal[name] < 0:
            raise ValueError('Finite measured terminal value required')
    later = deepcopy(later)
    later['source_snapshot_scope'] = later['scope']
    later['scope'] = 'Historical V4/V5 snapshot, augmented with separately verified V5 completion. Source snapshot time is not terminal verification time.'
    later['verified_at_utc'] = config['verified_at_utc']
    v5 = later['stages'][-1]
    v5['status'] = 'completed'
    v5['points'].append({'updates': terminal['updates'], 'valid_labels': terminal['valid_labels'],
                         'perplexity': terminal['perplexity'], 'mean_token_nll_nats': terminal['mean_token_nll_nats'],
                         'role': 'terminal_checkpoint', 'checkpoint_sha256': terminal['checkpoint_sha256'],
                         'verified_at_utc': terminal['verified_at_utc'], 'checkpoint_time_utc': None})
    later['stages'][0]['status'] = 'completed'
    tables = []
    for post in posts:
        for number, rows in enumerate(Tables(post['html']).tables, 1):
            tables.append({'id': post['slug'] + '-' + str(number), 'title': post['title'],
                           'date': str(post['date']), 'url': post['url'], 'headers': rows[0], 'rows': rows[1:],
                           'summary': post['summary'], 'source': post['source'],
                           'source_sha256': sha256((root / post['source']).read_bytes()).hexdigest()})
    task = history['historical_fixed32'][-1]
    summary = {
        'language': {'value': terminal['perplexity'], 'denominator': terminal['scored_labels'],
                     'status': 'evaluated', 'stage': 'V5 terminal', 'checkpoint_time_utc': None,
                     'source_url': terminal['source_url']},
        'training': {'value': terminal['valid_labels'], 'updates': terminal['updates'],
                     'status': terminal['status'], 'source_url': terminal['source_url']},
        'task': {'value': task['correct'], 'denominator': task['denominator'], 'format_valid': task['protocol_valid'],
                 'stage': task['stage'], 'status': task['evaluation_status'],
                 'source_url': BASE + '/2026/10/29/two-stages-terminal-evaluations/'},
    }
    for item in config['unrun']:
        if item['value'] is not None or item['status'] not in {'not_run', 'blocked_before_trial'}:
            raise ValueError('Unrun checks must have a null value and explicit status')
    return {'schema': 1, 'verified_at_utc': config['verified_at_utc'], 'sources': sources,
            'history': history, 'later_slices': later, 'terminal_v5': terminal,
            'tables': tables, 'unrun': config['unrun'], 'summary': summary}


def number(value):
    if value is None: return 'Not recorded'
    if type(value) is bool: return 'Yes' if value else 'No'
    if isinstance(value, (int, float)):
        if not math.isfinite(value): raise ValueError('Nonfinite dashboard number')
        return f'{value:,}'
    return str(value)


def render_summary(data):
    language, training, task = (data['summary'][k] for k in ('language', 'training', 'task'))
    return f'''<section class="dashboard-summary" aria-labelledby="dashboard-summary-title">
<div class="section-heading"><h2 id="dashboard-summary-title">What the measurements say</h2><a href="{BASE}/dashboard/">Full dashboard →</a></div>
<div class="metric-cards">
<article><p class="metric-kicker">Text prediction · V5 terminal</p><p class="metric-value">{language['value']:.4f}</p><p>Perplexity on the same <strong>{language['denominator']:,}</strong>-target CFR development check. Lower is better; this is not a reasoning score.</p><a href="{language['source_url']}">Read the evidence</a></article>
<article><p class="metric-kicker">Completed V5 slice</p><p class="metric-value">{training['value'] / 1e6:.2f}M</p><p><strong>{training['status'].capitalize()}</strong> usable training targets in {training['updates']:,} updates. More training is not itself a quality result.</p><a href="{training['source_url']}">{training['value']:,} exact targets</a></article>
<article><p class="metric-kicker">Last completed task check · earlier V3</p><p class="metric-value">{task['value']}/{task['denominator']}</p><p>Correct answers; <strong>{task['format_valid']}/{task['denominator']}</strong> met the output format. That failure prevents a clean reasoning test. No V5 task result.</p><a href="{task['source_url']}">Keep the test’s limits in view</a></article>
<article><p class="metric-kicker">Proposed grammar check</p><p class="metric-value metric-status">Not run</p><p>BLiMP has no score. A proposal is not a result, and grammar alone would not prove transferable logic.</p><a href="{BASE}/dashboard/#not-run">What remains unmeasured</a></article>
</div></section>'''


def line_svg(title, x_label, y_label, rows):
    values = [r for r in rows if r['x'] is not None and r['y'] is not None]
    if not values: raise ValueError('Cannot chart an entirely unmeasured series')
    if any(not math.isfinite(float(r[k])) for r in values for k in ('x', 'y')): raise ValueError('Nonfinite chart coordinate')
    width, height, left, right, top, bottom = 760, 300, 75, 25, 28, 62
    xmin, xmax = min(r['x'] for r in values), max(r['x'] for r in values)
    ymin, ymax = min(r['y'] for r in values), max(r['y'] for r in values)
    if xmax == xmin: xmax = xmin + 1
    span = ymax - ymin
    if span == 0: ymin, ymax = min(0, ymin), max(1, ymax * 1.1)
    else: ymin, ymax = max(0, ymin - span * .12), ymax + span * .12
    def xy(r):
        return left + (r['x'] - xmin) / (xmax - xmin) * (width-left-right), top + (ymax-r['y']) / (ymax-ymin) * (height-top-bottom)
    desc = f'{title}. {x_label}; {y_label}. Every recorded row is retained. Missing values are gaps, not zero. Exact values and timestamps are in the accompanying table. The vertical scale may not start at zero.'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-description">',
           f'<title id="chart-title">{escape(title)}</title><desc id="chart-description">{escape(desc)}</desc>',
           '<rect x="0" y="0" width="760" height="300" fill="#faf9f6"/>']
    for i in range(5):
        value = ymin + i*(ymax-ymin)/4
        y = xy({'x': xmin, 'y':value})[1]
        out.append(f'<path d="M {left} {y:.2f} L {width-right} {y:.2f}" stroke="#c9cec7" stroke-width="1" fill="none"/>')
        out.append(f'<text x="{left-10}" y="{y+4:.2f}" text-anchor="end" font-size="12" fill="#59615c">{escape(compact(value))}</text>')
    for i in range(5):
        value = xmin + i*(xmax-xmin)/4; x = xy({'x':value,'y':ymin})[0]
        out.append(f'<text x="{x:.2f}" y="{height-bottom+24}" text-anchor="middle" font-size="12" fill="#59615c">{escape(compact(value))}</text>')
    out.append(f'<text x="{width/2}" y="{height-10}" text-anchor="middle" font-size="13" fill="#232e2d">{escape(x_label)}</text>')
    out.append(f'<text x="{left}" y="17" font-size="13" fill="#232e2d">{escape(y_label)}</text>')
    segments, current = [], []
    for row in rows:
        if row['x'] is None or row['y'] is None:
            if current: segments.append(current); current = []
        else: current.append(row)
    if current: segments.append(current)
    for i, segment in enumerate(segments,1):
        points = [xy(row) for row in segment]
        route = ' '.join(('M' if n == 0 else 'L') + f' {x:.2f} {y:.2f}' for n,(x,y) in enumerate(points))
        out.append(f'<path id="series-line-{i}" d="{route}" stroke="#205e56" stroke-width="2.5" fill="none"/>')
        for row,(x,y) in zip(segment,points):
            fill = '#faf9f6' if 'parent' in row.get('role','') or 'baseline' in row.get('role','') else '#205e56'
            out.append(f'<rect x="{x-2.5:.2f}" y="{y-2.5:.2f}" width="5" height="5" fill="{fill}" stroke="#205e56" stroke-width="1"/>')
    out.append('</svg>')
    return '\n'.join(out)+'\n'


def compact(value):
    if abs(value) >= 1e6: return f'{value/1e6:.2f}M'
    if abs(value) >= 1e3: return f'{value/1e3:.1f}k'
    return f'{value:.2f}'.rstrip('0').rstrip('.')


def chart_definitions(data):
    result = []
    h = data['history']
    for stage,(short,title) in STAGES.items():
        points = [r for r in h['evaluation_points'] if r['stage'] == stage and r['evaluation_population'] == 'narrow_cfr_7057']
        result.append({'id': 'cfr-'+short, 'group':'language', 'title': title + ' · CFR text prediction',
                       'x_label':'Usable training targets within this stage', 'y_label':'Perplexity · lower is better',
                       'note':'Same 7,057-target narrow development panel. Starting models are repeat baselines, not new training. Unknown exposure coordinates are gaps. Exact checkpoint creation times are unavailable; observation times are not substitutes.',
                       'source':data['sources'][0]['path'],
                       'rows':[{'label':r['point_id']+' · '+r['role'], 'x':r['phase_valid_labels'], 'y':r['perplexity'],
                                'nll':r['mean_token_nll_nats'], 'denominator':r['scored_labels'], 'role':r['role'],
                                'observed_utc':r.get('observed_latest_utc'), 'checkpoint_time_utc':r['checkpoint_time_utc'],
                                'checkpoint_sha256':r['checkpoint_sha256']} for r in points]})
    for stage,short,title in zip(data['later_slices']['stages'],('v4-second','v5'),('V4 · second slice','V5 · completed slice')):
        result.append({'id':'cfr-'+short,'group':'language','title':title+' · CFR text prediction',
                       'x_label':'Usable training targets within this slice','y_label':'Perplexity · lower is better',
                       'note':'Same 7,057-target development panel. This slice is completed. Hollow starting point repeats the parent; saved checkpoints are separate from live counters. The V5 terminal score is rounded as reported. No reasoning result follows.',
                       'source':'content/dashboard.json' if short=='v5' else data['sources'][1]['path'],
                       'rows':[{'label':'Update '+str(p['updates'])+' · '+p['role'],'x':p['valid_labels'],'y':p['perplexity'],
                                'nll':p.get('mean_token_nll_nats'),'denominator':7057,'role':p['role'],
                                'observed_utc':p.get('verified_at_utc'),
                                'snapshot_utc':data['later_slices']['observation_utc'] if 'verified_at_utc' not in p else None,
                                'checkpoint_time_utc':None} for p in stage['points']]})
    broad=[r for r in h['evaluation_points'] if r['evaluation_population']=='broad_panel_130209']
    result.append({'id':'broader','group':'language','title':'Broader text · a different development panel',
                   'x_label':'Retained model-lineage targets','y_label':'Perplexity · lower is better',
                   'note':'130,209 targets across arXiv, Stack Exchange and Wikimedia. These historical checkpoints span several phases. This is not the CFR population and has not been rerun on V5.',
                   'source':data['sources'][0]['path'],
                   'rows':[{'label':r['stage'],'x':r['model_lineage_valid_labels'],'y':r['perplexity'],
                            'nll':r['mean_token_nll_nats'],'denominator':r['scored_labels'],
                            'observed_utc':r.get('observed_latest_utc'),'checkpoint_time_utc':None} for r in broad]})
    result.append({'id':'v4-boundary-overhead','group':'performance','title':'V4 first slice · cumulative save-and-check share',
                   'x_label':'Completed training update','y_label':'Percent of training-loop time',
                   'note':'Cumulative, overlapping boundaries: do not add them. Includes full checkpoint and evaluation work; excludes model loading. Stage completion was verified separately from this timing schema.',
                   'source':data['sources'][0]['path'],
                   'rows':[{'label':'Through update '+str(r['through_phase_update']),'x':r['through_phase_update'],
                            'y':r['checkpoint_plus_evaluation_fraction_of_loop']*100,'observed_utc':r['observed_utc'],
                            'checkpoint_time_utc':None} for r in h['intermediate_run_timings']]})
    observations=h['v4_progress_observations']
    start=datetime.fromisoformat(observations[0]['observed_utc'])
    for key,title in PROGRESS_METRICS.items():
        result.append({'id':'progress-'+key.replace('_','-'),'group':'progress','title':'V4 first slice · '+title,
                       'x_label':'Minutes since first recorded observation','y_label':title,
                       'note':'Historical observer series, not live data. Every observation is retained. Completed work, charged work, retained model history and physical work have different scopes. Interval rates include all elapsed overhead; they are not GPU-kernel rates. Missing first intervals remain missing.',
                       'source':data['sources'][0]['path'],
                       'rows':[{'label':r['observed_utc'],'x':(datetime.fromisoformat(r['observed_utc'])-start).total_seconds()/60,
                                'y':r[key],'observed_utc':r['observed_utc'],'checkpoint_time_utc':None} for r in observations]})
    if {p['id'] for p in result} != set(CHART_IDS): raise ValueError('Chart inventory and reviewed asset names differ')
    return result


def data_table(title, headers, rows):
    return '<div class="table-scroll" tabindex="0" role="region" aria-label="'+escape(title,quote=True)+'"><table><caption>'+escape(title)+'</caption><thead><tr>'+''.join('<th scope="col">'+escape(str(h))+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+escape(number(c))+('</th>' if i==0 else '</td>') for i,c in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div>'


def chart_table(panel):
    headers = ['Observation', panel['x_label'], panel['y_label']]
    fields = ['label', 'x', 'y']
    if panel['group'] == 'language':
        headers += ['NLL (nats/target)', 'Scored targets', 'Observed / verified UTC', 'Source snapshot UTC', 'Exact save time', 'Checkpoint SHA-256']
        fields += ['nll', 'denominator', 'observed_utc', 'snapshot_utc', 'checkpoint_time_utc', 'checkpoint_sha256']
    else:
        headers += ['Observed UTC']; fields += ['observed_utc']
    return data_table(panel['title']+' · every recorded observation', headers,
                      [[r.get(key) for key in fields] for r in panel['rows']])


def bars(title, labels, cells):
    parsed = [numeric_cell(c) for c in cells]
    measured = [c for c in parsed if c is not None]
    if not measured: return ''
    denominators = {c['denominator'] for c in measured}
    if len(denominators) > 1:
        return '<p class="chart-caveat">Different denominators: read the exact fractions in the table; no pooled rate.</p>'
    maximum = max([c['denominator'] or c['value'] for c in measured] + [1])
    if any(c['value'] < 0 for c in measured): return ''
    rows = []
    for label, cell, raw in zip(labels, parsed, cells):
        bar = ('<meter aria-hidden="true" min="0" max="'+str(maximum)+'" value="'+str(cell['value'])+'"></meter>') if cell else '<span class="chart-missing">No bar</span>'
        rows.append('<div class="bar-row"><span>'+escape(label)+'</span>'+bar+'<strong>'+escape(raw)+'</strong></div>')
    return '<div class="bar-chart"><p class="bar-title">'+escape(title)+'</p>'+''.join(rows)+'<p class="bar-scale">Scale: 0–'+escape(number(maximum))+'. Exact reported values; missing or nonnumeric cells have no bar.</p></div>'


def historical_table(item):
    headers,rows=item['headers'],item['rows']
    # Comparisons have experiments in columns. Other tables have observations in rows.
    rowwise = headers[0] in {'Measurement','Training diagnostic','Development measurement','Frozen quantity','Training measurement','Per-mode result, 64 cases','New frozen diagnostic','Fresh 48-case diagnostic','Fixed-64 measure','Original accepted-state score','Original accepted-state score, each mode','Changed factor','CPU budget calculation'}
    charts=''
    if rowwise:
        charts=''.join(bars(row[0],headers[1:],row[1:]) for row in rows)
    elif headers[0] not in {'Proposed criterion','Software or device','Component','Selected failure'}:
        for col in range(1,len(headers)):
            charts+=bars(headers[col],[r[0] for r in rows],[r[col] for r in rows])
    return f'<details class="historical-table" id="table-{escape(item["id"],quote=True)}"><summary>{escape(item["title"])} · table {item["id"].rsplit("-",1)[-1]}</summary><p>{escape(item["summary"])}</p><p class="chart-caveat">Dated snapshot, {item["date"]}. Read each metric separately: training fit, proxy passes, strict success, plans, and data candidates are not interchangeable. Bars start at zero and compare only values within their own metric. Different populations are not a learning curve.</p>{charts}{data_table(item["title"],headers,rows)}<p><a href="{item["url"]}">Read the source and its plain-language companion</a></p></details>'


def detailed_histories(data):
    h = data['history']; parts = []
    lookup = {r['point_id']: r for r in h['evaluation_points']}
    parts.append('<section class="dashboard-group" id="source-panels"><h2>Text sources and repeated observations</h2><p>The broader panel’s source families have different denominators. Each family stays in its own chart; none is a new V5 result.</p>')
    for family in sorted({r['source_family'] for r in h['broad_panel_per_source']}):
        rows = [r for r in h['broad_panel_per_source'] if r['source_family'] == family]
        labels = [STAGES[lookup[r['point_id']]['stage']][1] for r in rows]
        parts.append('<details><summary>'+escape(family)+' · broader-panel subset</summary>'+bars('Perplexity · '+family, labels, [number(r['perplexity']) for r in rows])+data_table(family+' · exact source-panel results', ['Checkpoint phase','Targets','NLL (nats/target)','Perplexity','Total NLL (nats)'], [[label,r['scored_tokens'],r['mean_token_nll_nats'],r['perplexity'],r['total_nll_nats']] for label,r in zip(labels,rows)])+'</details>')
    rows = h['stage2_observations']
    parts.append('<details><summary>V3 second stage · repeated observations, not new saves</summary><p>These are 22 observations of saved-model evidence, not 22 new checkpoints. Missing counters and incomplete matching resume-state files remain explicit.</p>'+bars('Observed perplexity · same 7,057-target panel', [r['observed_utc'] for r in rows], [number(r['perplexity']) for r in rows])+data_table('Repeated V3 stage-two observations', ['Observed UTC','PPL','NLL','Targets','Phase updates','Physical labels','Complete resume state','New unique save claimed','Checkpoint SHA-256'], [[r['observed_utc'],r['perplexity'],r['mean_token_nll_nats'],r['scored_labels'],r['phase_updates'],r['physical_valid_labels'],r['complete_matching_sidecar_present'],r['is_new_unique_checkpoint_claim'],r['checkpoint_sha256']] for r in rows])+'</details></section>')
    return ''.join(parts)


def render_dashboard(data):
    panels=chart_definitions(data)
    parts=[f'<article class="page dashboard"><header class="article-header"><p class="eyebrow">An evidence map, not a leaderboard</p><h1>What is getting better?<br>What is still unknown?</h1><p class="dek">Text prediction, task outcomes, training work and cost tell different stories. Keep them separate.</p><p>Reviewed snapshot: <time datetime="{data["verified_at_utc"]}">{data["verified_at_utc"]}</time>. This page rebuilds from reviewed public data; it does not poll the training machine.</p></header>',render_summary(data),
           f'<nav class="dashboard-nav" aria-label="Dashboard sections"><a href="#language">Language prediction</a><a href="#tasks">Task and format checks</a><a href="#performance">Time and cost</a><a href="#progress">Training histories</a><a href="#historical">Earlier comparisons</a><a href="#not-run">Not run</a><a href="#sources">Data and method</a></nav>',
           '<aside class="note"><strong>How to read these charts</strong><p>Lower loss or perplexity means better prediction on that exact text check, not better reasoning. A checkpoint is a saved model. A target is a prediction the rules count. A blank is missing or unrun, not zero. Repeated parent checks add no new training. Some chart axes are narrowed to reveal small changes; read the labeled scale.</p></aside>',
           '<p class="correction"><strong>Ledger correction:</strong> the 17:14 UTC V5 snapshot had 3,601 completed updates and 117,734,731 valid labels, not the earlier zero-based counts of 3,600 and 117,702,026. Saved-checkpoint scores are unchanged. V5 has since completed.</p>']
    def panel_html(p):
        table=(f'<details><summary>Exact values and timestamps · {len(p["rows"])} observations</summary>{chart_table(p)}</details>' if len(p['rows'])<=50 else f'<p><a href="{BASE}/dashboard/data/{p["id"]}/">Read all {len(p["rows"])} observations as an accessible table</a></p>')
        return f'<section class="dashboard-panel" id="{p["id"]}"><h3>{escape(p["title"])}</h3><p>{escape(p["note"])}</p><figure><div class="chart-scroll" tabindex="0" role="region" aria-label="{escape(p["title"],quote=True)} chart"><img loading="lazy" width="760" height="300" src="{BASE}/assets/charts/dashboard-{p["id"]}.svg" alt="{escape(p["title"]+". "+p["y_label"]+". Exact values follow in the data table.",quote=True)}"></div><figcaption>{escape(p["x_label"])} · {escape(p["y_label"])}. Every measured point retained; unknown positions omitted from geometry, retained in the table. On narrow screens, scroll the chart sideways or use the exact table.</figcaption></figure>{table}</section>'
    for group,title in [('language','Language prediction'),('performance','Time and cost'),('progress','Training histories')]:
        parts.append(f'<section id="{group}" class="dashboard-group"><h2>{title}</h2>')
        if group=='progress': parts.append('<p>Open a measure to explore every recorded V4 first-slice observation. These historical counters are not today’s live status and never advance a saved model’s quality score.</p>')
        for p in panels:
            if p['group']!=group:continue
            body=panel_html(p)
            if group=='progress':body=f'<details><summary>{escape(p["title"])}</summary>{body}</details>'
            parts.append(body)
        if group=='performance':
            parts.append('<h3>Completed runs · each denominator stays separate</h3><p>These are end-to-end rates, not GPU-kernel speeds. Reserved evaluation charges are not measured elapsed times.</p>')
            labels=[STAGES[r['stage']][1] for r in data['history']['completed_run_timings']]
            for key,title2 in TIMING_METRICS.items():
                rows=data['history']['completed_run_timings']
                vals=[r.get(key) for r in rows]
                parts.append('<details><summary>'+escape(title2)+'</summary>'+bars(title2,labels,[number(v) for v in vals])+data_table(title2,['Run',title2],list(zip(labels,vals)))+'</details>')
            rows = data['history']['intermediate_run_timings']
            parts.append('<h3>V4 first-slice cumulative boundaries</h3><p>Each row covers all work up to that checkpoint, not an additional interval. These overlapping totals must not be added. Empty timing fields stay missing.</p>')
            for key,title2 in {**TIMING_METRICS, 'valid_labels_per_training_excluding_hooks_second': 'Usable predictions per second excluding measured hooks'}.items():
                if not any(r.get(key) is not None for r in rows): continue
                labels = ['Through update '+str(r['through_phase_update']) for r in rows]
                vals = [r.get(key) for r in rows]
                parts.append('<details><summary>'+escape(title2)+'</summary>'+bars(title2, labels, [number(v) for v in vals])+data_table('Cumulative V4 · '+title2,['Boundary',title2,'Observed UTC'],[[label,v,r['observed_utc']] for label,v,r in zip(labels,vals,rows)])+'</details>')
            timing=data['history']['completed_benchmark_timings']
            parts.append(data_table('Separate terminal evaluation costs · seconds',['Check','Scorer','Full restore/check hook','Guard','Reserved charge'],[[r['role'],r['scorer_elapsed_seconds'],r['full_hook_elapsed_seconds'],r['guard_conservative_elapsed_seconds'],r['charged_seconds']] for r in timing]))
            for key,title2 in [('scorer_elapsed_seconds','Scorer time · seconds'),('full_hook_elapsed_seconds','Restore and complete evaluation · seconds'),('guard_conservative_elapsed_seconds','Guard elapsed time · seconds'),('charged_seconds','Reserved evaluation budget · seconds'),('generated_tokens','Generated output tokens'),('generated_tokens_per_second','Generated tokens per scorer second')]:
                parts.append('<details><summary>'+title2+'</summary>'+bars(title2,[r['role'] for r in timing],[number(r.get(key)) for r in timing])+data_table(title2,['Check',title2,'Observed UTC'],[[r['role'],r.get(key),r['observed_utc']] for r in timing])+'</details>')
            terminal=data['terminal_v5']
            parts.append(data_table('Completed slice · V5', ['State','Updates','Usable training targets','Processed input tokens','Completion verified UTC'], [[terminal['status'],terminal['updates'],terminal['valid_labels'],terminal['processed_input_tokens'],terminal['verified_at_utc']]]))
            parts.append(f'<p>V5 terminal save-and-check overhead: <strong>{data["terminal_v5"]["checkpoint_plus_evaluation_percent_of_loop"]}%</strong> of loop time. No new whole-run seconds or GPU-only rate are inferred.</p>')
        parts.append('</section>')
    parts.append(detailed_histories(data))
    tasks=data['history']['historical_fixed32']
    parts.append('<section id="tasks" class="dashboard-group"><h2>Task and format checks</h2><p>The last completed fixed-32 check belongs to V3, not V5. Every answer failed the required output format. That makes these failures important, but prevents a clean measurement of reasoning capacity.</p>'+bars('Task-correct answers out of 32',[STAGES[r['stage']][1] for r in tasks],[f'{r["correct"]}/{r["denominator"]}' for r in tasks])+data_table('Historical fixed-32 development checks',['Earlier stage','Correct','Correct format','Observed UTC'],[[STAGES[r['stage']][1],f'{r["correct"]}/{r["denominator"]}',f'{r["protocol_valid"]}/{r["denominator"]}',r.get('observed_utc')] for r in tasks])+'</section>')
    parts.append('<section id="historical" class="dashboard-group"><h2>Earlier experiments and recorded quantities</h2><p>Every public post table is collected below directly from its Markdown source. Numeric comparisons get their own zero-based bars; software versions, ambiguous ranges, and proposed thresholds are not guessed into measurements. Dated proxy scores remain labeled by their source limitations. These tables include the earlier 97.5M-model experiments, data reviews, recovery, and planned budgets.</p>'+''.join(historical_table(t) for t in data['tables'])+'</section>')
    parts.append('<section id="not-run" class="dashboard-group"><h2>Not run is not zero</h2>'+''.join('<article class="unrun-card"><h3>'+escape(r['title'])+'</h3><strong>'+('Blocked before trial' if r['status']=='blocked_before_trial' else 'Not run')+'</strong><p>'+escape(r['note'])+'</p></article>' for r in data['unrun'])+'</section>')
    parts.append('<details><summary>Historical unrun checks · explicit missing results</summary>'+data_table('Unrun historical checks', ['Phase','Checkpoint identity','Check','Status','Planned targets or cases','Actually scored','Perplexity','Correct','Format valid'], [[r['stage'],r['point_id'],r['evaluation_population'],r['evaluation_status'],r['planned_population_denominator'],r['scored_labels'],r['perplexity'],r['correct'],r['protocol_valid']] for r in data['history']['unrun_evaluations']])+'</details>')
    parts.append(f'<section id="sources" class="dashboard-group"><h2>Data and method</h2><p>The homepage and this dashboard use one compiled data model. Source post charts stay frozen. This page keeps all 42 aggregate language-score rows, 22 repeated stage-two observations, 26 explicitly unrun records, 594 V4 observer rows, timing histories and all 41 post tables. Later V4/V5 saves are separate additions. Repeated observations do not create new checkpoint identities.</p><p><a href="{BASE}/assets/dashboard-data.json">Download the complete dashboard data (JSON)</a> · <a href="https://github.com/obra/model-training-journal/blob/main/scripts/dashboard-README.md">Schema and update guide</a></p><p>Exact model-save times are unavailable in these sources. Observation and completion-verification times are retained under their own names. Different populations, tokenizer/scorer contracts, training clocks and timing denominators are never pooled. No private logs, source passages, model weights or live telemetry are fetched.</p><ul>'+''.join('<li><a href="https://github.com/obra/model-training-journal/blob/main/'+s['path']+'">'+escape(s['path'])+'</a> · SHA-256 <code>'+s['sha256']+'</code></li>' for s in data['sources'])+'</ul></section></article>')
    return '\n'.join(parts)


def write_assets(root, data):
    for panel in chart_definitions(data):
        name='dashboard-'+panel['id']+'.svg'
        if name not in DASHBOARD_CHART_NAMES: raise ValueError('Unreviewed chart path')
        (root/'assets/charts'/name).write_text(line_svg(panel['title'],panel['x_label'],panel['y_label'],panel['rows']))
    (root/'assets/dashboard-data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
