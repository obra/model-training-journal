#!/usr/bin/env python3
"""Reproduce two separate terminal V4 panels from sanitized aggregates, offline."""
from pathlib import Path
import hashlib,io,json,os
from build_v4_first_checkpoint_charts import plt,sanitize,grid

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/v4-terminal-tranche1'

def save(fig,name,title,description,source):
 preview=os.environ.get('CHART_PREVIEW_DIR')
 if preview:
  p=Path(preview);p.mkdir(parents=True,exist_ok=True);fig.savefig(p/name.replace('.svg','.png'),dpi=150)
 stream=io.BytesIO();fig.savefig(stream,format='svg',metadata={'Date':None,'Creator':None});plt.close(fig)
 raw,profile=sanitize(stream.getvalue(),title,description)
 target=ROOT/'assets/charts'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 return dict(file=target.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),
  title=title,description=description,input_file=source.relative_to(ROOT).as_posix(),
  input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),passive_svg_profile=profile)

def build():
 source=DATA/'cfr-checkpoints.json';data=json.loads(source.read_bytes());rows=data['points']
 assert [r['phase_updates'] for r in rows]==[0,569,1137,1705,2273,2841,3409]
 assert {r['scored_labels'] for r in rows}=={7057}
 assert len({(r['evaluation_manifest_sha256'],r['evaluator_sha256'],r['tokenizer_sha256']) for r in rows})==1
 assert len({r['checkpoint_sha256'] for r in rows})==7
 assert rows[3]['perplexity']>rows[2]['perplexity'] and rows[-1]['perplexity']>rows[-2]['perplexity']
 x=[r['phase_valid_labels']/1e6 for r in rows];y=[r['perplexity'] for r in rows]
 fig,ax=plt.subplots(figsize=(8,5.8));fig.subplots_adjust(left=.13,right=.97,bottom=.24,top=.80)
 color='#187eaa';ax.plot(x,y,color=color,linewidth=2);ax.scatter(x[1:],y[1:],s=48,color=color,zorder=4)
 ax.scatter(x[0],y[0],s=70,facecolor='white',edgecolor=color,linewidth=2,zorder=5)
 labels=['Parent','CP569','CP1137','CP1705','CP2273','CP2841','Terminal 3409']
 offsets=[(8,8),(0,15),(-2,-35),(0,15),(0,15),(-3,18),(-3,14)]
 aligns=['left','center','center','center','center','center','right']
 for r,label,offset,align in zip(rows,labels,offsets,aligns):
  ax.annotate(f"{label}\n{r['perplexity']:.4f}",(r['phase_valid_labels']/1e6,r['perplexity']),
   xytext=offset,textcoords='offset points',ha=align,fontsize=9)
 ax.set_xlim(-3,116);ax.set_ylim(36.9,40.2);ax.set_xticks(x,['0','18.60','37.18','55.75','74.32','92.89','111.46'])
 ax.set_xlabel('Completed valid labels within the first V4 slice (millions)',labelpad=10)
 ax.set_ylabel('CFR perplexity (restricted axis)',labelpad=8);grid(ax)
 fig.suptitle('Completed slice: terminal is not the best observed checkpoint',y=.96,fontsize=14,fontweight='bold')
 fig.text(.13,.86,'Same 7,057-label CFR development set; lower is better.',fontsize=11)
 fig.text(.13,.115,'Hollow marker: repeated parent. Both CP1705 and terminal regressions retained.',fontsize=9)
 fig.text(.13,.070,'Repeated development evaluation; no sealed-holdout or transferable-logic claim.',fontsize=9)
 figures=[save(fig,'v4-terminal-cfr-perplexity.svg','Completed V4 slice: narrow CFR development perplexity',
  'Seven observations on the same 7057-label CFR development panel. Parent 39.776214231484126; CP569: 39.4729645509789; CP1137: 38.51235059861212; CP1705: 38.54555845078176; CP2273: 38.17367341486999; CP2841: 37.315892535997385; terminal3409: 37.7860145783434. Regressions retained. Restricted y-axis; no broader or reasoning inference.',source)]
 source=DATA/'cumulative-overhead.json';timings=json.loads(source.read_bytes())['points']
 assert [r['through_phase_update'] for r in timings]==[569,1137,1705,2273,2841,3409]
 fractions=[r['checkpoint_plus_evaluation_fraction_of_loop']*100 for r in timings]
 assert abs(fractions[-1]-3.400852925025956)<1e-12
 fig,ax=plt.subplots(figsize=(8,5.3));fig.subplots_adjust(left=.13,right=.96,bottom=.24,top=.78)
 ax.plot(range(6),fractions,marker='o',color='#a16a21',linewidth=2)
 ax.axhline(10,color='#8a5050',linestyle='--',linewidth=1);ax.text(5,10.25,'Existing 10% limit',ha='right',fontsize=9)
 ax.annotate('Terminal 3.40085%',(5,fractions[-1]),xytext=(-5,14),textcoords='offset points',ha='right',fontsize=11)
 ax.set_xticks(range(6),['569','1137','1705','2273','2841','3409']);ax.set_ylim(0,11)
 ax.set_xlabel('Saved boundary: completed update within the first slice',labelpad=10)
 ax.set_ylabel('Cumulative checkpoint + evaluation hooks / loop (%)');grid(ax)
 fig.suptitle('Separate timing panel: cumulative measured hook overhead',y=.96,fontsize=14,fontweight='bold')
 fig.text(.13,.84,'Overlapping cumulative totals; do not add boundaries together.',fontsize=10)
 fig.text(.13,.115,'Full boundary hooks included; model load excluded. Axis starts at zero.',fontsize=9)
 fig.text(.13,.070,'No guard-wall, worker-startup or GPU-kernel timing claim.',fontsize=9)
 figures.append(save(fig,'v4-terminal-overhead.svg','V4 cumulative measured boundary-hook fraction',
  'Six cumulative boundary measurements, approximately 3.4 percent of loop time; terminal 3.400852925025956 percent. The existing limit is 10 percent. Full checkpoint/evaluation hooks included, model load excluded. Overlapping totals are not per-interval durations. No guard-wall or GPU-kernel claim.',source))
 metadata=dict(schema='sanitized_reproducible_static_chart_v1',builder_file=Path(__file__).relative_to(ROOT).as_posix(),
  builder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),figures=figures,
  observation_count=7,new_saved_checkpoints=6,regressions_preserved=[1705,3409],separate_panels=True)
 (ROOT/'assets/charts/v4-terminal-chart-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
 print(json.dumps(metadata,sort_keys=True))

if __name__=='__main__':build()
