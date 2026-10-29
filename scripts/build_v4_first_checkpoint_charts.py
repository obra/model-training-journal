#!/usr/bin/env python3
"""Reproduce four passive SVG charts from public sanitized JSON; no network behavior."""
from pathlib import Path
import hashlib,io,json,os,re,xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'assets/v4-first-checkpoint-569/checkpoint-history.json';OUT=ROOT/'assets/charts'
SVG='http://www.w3.org/2000/svg';XLINK='http://www.w3.org/1999/xlink'
TAGS={'svg','g','defs','path','rect','line','polyline','polygon','use','clipPath','title','desc'}
PRESENTATION={'fill','stroke','stroke-width','stroke-linejoin','stroke-linecap','stroke-miterlimit','stroke-dasharray','stroke-dashoffset','opacity','fill-opacity','stroke-opacity'}
ATTRS={'width','height','viewBox','version','id','d','transform','x','y','x1','x2','y1','y2','rx','ry','points','clip-path','clip-rule','fill-rule','href','role','aria-labelledby',*PRESENTATION}
ET.register_namespace('',SVG);ET.register_namespace('xlink',XLINK)
plt.rcParams.update({'svg.fonttype':'path','svg.hashsalt':'checkpoint-chart-history-20261029-v1','font.family':'DejaVu Sans','font.size':10,'axes.titlesize':13,'axes.labelsize':10,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#536273','axes.labelcolor':'#243447','text.color':'#172b3a','xtick.color':'#394d5b','ytick.color':'#394d5b','figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white','path.simplify':False})
STAGES=[('science_104521471','Science 104.52M','#5267a8'),('filtered_96012838','Filtered 96.01M','#a16a21'),('admitted_143m_continuation','Admitted 143.22M','#40857b'),('admitted_v3_stage1','Stage1 130.07M','#704a9b'),('admitted_v3_stage2','Stage2 130.11M','#c04b43'),('admitted_v4_tranche1','V4 first checkpoint','#187eaa')]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def sanitize(raw,title,description):
 raw=re.sub(br'<!DOCTYPE[^>]*>',b'',raw,flags=re.S);root=ET.fromstring(raw)
 for parent in list(root.iter()):
  for child in list(parent):
   if child.tag.split('}')[-1] in {'metadata','style'}:parent.remove(child)
 root.set('role','img');root.set('aria-labelledby','chart-title chart-description');root.set('stroke-linejoin','round');root.set('stroke-linecap','butt')
 for position,tag,identity,value in [(0,'title','chart-title',title),(1,'desc','chart-description',description)]:
  node=ET.Element('{'+SVG+'}'+tag,{'id':identity});node.text=value;root.insert(position,node)
 for node in root.iter():
  assert node.tag.startswith('{'+SVG+'}') and node.tag.split('}')[-1] in TAGS,node.tag
  style=node.attrib.pop('style',None)
  if style:
   for declaration in style.split(';'):
    if not declaration.strip():continue
    key,value=declaration.split(':',1);key=key.strip();value=value.strip();assert key in PRESENTATION,(key,value);assert not re.search(r'url\s*\(|(?:https?|data):',value,re.I);node.set(key,value)
  for key,value in node.attrib.items():
   local=key.split('}')[-1];assert local in ATTRS and not local.lower().startswith('on'),(node.tag,key)
   if key.startswith('{'):assert key=='{'+XLINK+'}href'
   if local not in {'href','clip-path'}:assert not re.search(r'url\s*\(|(?:https?|data):',value,re.I),(key,value)
 ids={n.get('id'):n for n in root.iter() if n.get('id')};assert len(ids)==sum(n.get('id') is not None for n in root.iter())
 for node in root.iter():
  for key,value in node.attrib.items():
   local=key.split('}')[-1]
   if local=='href':assert node.tag=='{'+SVG+'}use' and re.fullmatch(r'#[A-Za-z_][\w.-]*',value) and value[1:] in ids and ids[value[1:]].tag=='{'+SVG+'}path'
   if local=='clip-path':
    match=re.fullmatch(r'url\(#([A-Za-z_][\w.-]*)\)',value);assert match and match.group(1) in ids and ids[match.group(1)].tag=='{'+SVG+'}clipPath'
 result=ET.tostring(root,encoding='utf-8',xml_declaration=True);assert len(result)<1_000_000 and b'DOCTYPE' not in result and b'<style' not in result and b' style=' not in result
 return result,{'tags':sorted({n.tag.split('}')[-1] for n in root.iter()}),'attributes':sorted({k.split('}')[-1] for n in root.iter() for k in n.attrib}),'nodes':sum(1 for _ in root.iter())}
def save(fig,name,title,caption,counts):
 preview=os.environ.get('CHART_PREVIEW_DIR')
 if preview:
  target=Path(preview);target.mkdir(parents=True,exist_ok=True);fig.savefig(target/name.replace('.svg','.png'),dpi=120)
 buffer=io.BytesIO();fig.savefig(buffer,format='svg',metadata={'Date':None,'Creator':None});plt.close(fig);raw,profile=sanitize(buffer.getvalue(),title,caption);(OUT/name).write_bytes(raw)
 return {'file':'assets/charts/'+name,'sha256':sha(raw),'bytes':len(raw),'title':title,'caption':caption,'counts':counts,'passive_svg_profile':profile}
def grid(ax):ax.grid(axis='y',color='#d9e1e7',linewidth=.6);ax.set_axisbelow(True)
def build():
 raw=SOURCE.read_bytes();data=json.loads(raw);OUT.mkdir(parents=True,exist_ok=True);figures=[]
 narrow=[r for r in data['evaluation_points'] if r['evaluation_population']=='narrow_cfr_7057' and r['evaluation_status']=='evaluated'];assert len(narrow)==34 and {r['scored_labels'] for r in narrow}=={7057};assert len({(r['evaluation_manifest_sha256'],r['evaluator_sha256'],r['tokenizer_sha256']) for r in narrow})==1
 fig,axes=plt.subplots(1,2,figsize=(13,5.4),sharey=True);fig.subplots_adjust(left=.065,right=.98,top=.81,bottom=.23,wspace=.23);omitted={k:0 for k in ['model_lineage_valid_labels','phase_valid_labels']};baselines_plotted=0
 for stage,label,color in STAGES:
  rows=[r for r in narrow if r['stage']==stage]
  for ax,field in [(axes[0],'model_lineage_valid_labels'),(axes[1],'phase_valid_labels')]:
   points=sorted([r for r in rows if r[field] is not None and r['perplexity'] is not None],key=lambda r:r[field]);omitted[field]+=len(rows)-len(points);ax.plot([r[field]/1e6 for r in points],[r['perplexity'] for r in points],color=color,linewidth=1.5,label=label)
   for r in points:
    baseline='baseline' in r['role'];ax.scatter(r[field]/1e6,r['perplexity'],s=46 if baseline else 24,facecolor='white' if baseline else color,edgecolor=color,linewidth=1.5 if baseline else .7,zorder=4)
    if field=='model_lineage_valid_labels' and baseline:baselines_plotted+=1
 axes[0].set_title('Cumulative model-lineage clock');axes[0].set_xlabel('Model-lineage valid labels (millions)');axes[0].set_ylabel('Perplexity on 7,057 CFR labels');axes[1].set_title('Phase-local clocks reset at each stage');axes[1].set_xlabel('Valid labels within each phase (millions)')
 for ax in axes:grid(ax)
 handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.955),ncol=3,frameon=False,fontsize=8);fig.suptitle('CFR checkpoint perplexity across the training lineage',y=.995,fontsize=16,fontweight='bold');fig.text(.065,.11,'Hollow circles: baseline observations of existing checkpoints. Repeated baselines remain separate; no averaging.',fontsize=9);fig.text(.065,.065,'Unknown x values omitted: five cumulative points, one phase-local baseline. Observation times are not checkpoint times.',fontsize=9)
 latest=sorted([r for r in narrow if r['stage']=='admitted_v3_stage2' and r['phase_updates'] not in [None,0]],key=lambda r:r['phase_updates']);assert len(latest)==6 and [r['phase_updates'] for r in latest]==[664,1327,1990,2653,3316,3979] and latest[2]['perplexity']>latest[1]['perplexity'] and latest[-1]['perplexity']>latest[-2]['perplexity']
 fig.text(.065,.025,'V4: one new saved checkpoint at18.604M labels, PPL39.4730 versus repeated parent39.7762. Stage remains in progress.',fontsize=9,color='#187eaa')
 inset=axes[1].inset_axes([.42,.42,.54,.43]);v4=[r for r in narrow if r['stage']=='admitted_v4_tranche1'];inset.plot([r['phase_valid_labels']/1e6 for r in v4],[r['perplexity'] for r in v4],color='#187eaa',marker='o');inset.scatter(0,v4[0]['perplexity'],facecolor='white',edgecolor='#187eaa',zorder=5);inset.set_title('V4 detail: same7,057-label CFR set',fontsize=8);inset.set_xlabel('Phase labels (M)',fontsize=8);inset.set_ylabel('PPL',fontsize=8);inset.tick_params(labelsize=8);inset.set_ylim(39.35,39.9);grid(inset)
 caption='Narrow CFR development evaluation only:7,057 scored labels per report under one unchanged contract. Left:cumulative model-lineage valid labels in millions. Right:phase-local valid labels. Hollow markers retain baseline observations without averaging repeated checkpoints. Of 34 evaluated rows, the cumulative panel plots 29 and omits five unknown x values; the phase-local panel plots 33 and omits one early baseline. Missing values are never plotted at zero. Broad-panel and fixed32 results are separate. Stage2 completed six scheduled checkpoints. Terminal PPL39.776214231484126 slightly regressed from39.64829262191972 at checkpoint3316, below parent43.77612727431155. The checkpoint1990 regression remains visible. V4 adds a repeated parent baseline and one unique saved checkpoint569:39.776214231484126 to39.4729645509789 at18604156 phase labels. Inset shows this pair. V4 capture observation:2026-10-29T21:58:47.291635+00:00; exact checkpoint creation time unavailable.'
 figures.append(save(fig,'v4-569-checkpoint-perplexity.svg','CFR checkpoint perplexity by cumulative and phase-local valid labels',caption,{'evaluated_rows':len(narrow),'plotted_cumulative_rows':len(narrow)-omitted['model_lineage_valid_labels'],'plotted_phase_local_rows':len(narrow)-omitted['phase_valid_labels'],'omitted_unknown_cumulative_x':omitted['model_lineage_valid_labels'],'omitted_unknown_phase_x':omitted['phase_valid_labels'],'baseline_observations_total':sum('baseline' in r['role'] for r in narrow),'baseline_markers_per_panel':baselines_plotted,'unique_checkpoint_identities':len({r['checkpoint_sha256'] for r in narrow}),'v4_new_saved_checkpoints':1,'v4_inset_points':2}))
 broad=[r for r in data['evaluation_points'] if r['evaluation_population']=='broad_panel_130209'];assert len(broad)==3 and all(r['scored_labels']==130209 for r in broad);broad.sort(key=lambda r:r['model_lineage_updates']);fig,axes=plt.subplots(1,2,figsize=(12.5,5.2));fig.subplots_adjust(left=.075,right=.98,top=.80,bottom=.21,wspace=.24);colors=['#7b8799','#25887f','#c04b43'];values=[r['perplexity'] for r in broad];bars=axes[0].bar(['Parent baseline','Science terminal','Stage2 terminal'],values,color=colors,width=.6);axes[0].bar_label(bars,labels=[f'{x:.2f}' for x in values],padding=4);axes[0].set_ylim(0,max(values)*1.2);axes[0].set_title('Frozen earlier aggregate evaluations');axes[0].set_ylabel('Perplexity on 130,209 labels')
 slices=data['broad_panel_per_source'];source_order=['arxiv','stackexchange','wikimedia'];x=np.arange(3);width=.24;source_den={}
 for j,r in enumerate(broad):
  ss={s['source_family']:s for s in slices if s['point_id']==r['point_id']};assert set(ss)==set(source_order);vals=[ss[k]['perplexity'] for k in source_order];source_den={k:ss[k]['scored_tokens'] for k in source_order};bars=axes[1].bar(x+(j-1)*width,vals,width,color=colors[j],label=['Parent baseline','Science terminal','Stage2 terminal'][j]);axes[1].bar_label(bars,labels=[f'{v:.1f}' for v in vals],padding=3,fontsize=8)
 axes[1].set_xticks(x,['arXiv','StackExchange','Wikimedia']);axes[1].set_ylim(0,610);axes[1].set_title('Separate source slices of the same panel');axes[1].legend(frameon=False,fontsize=9)
 for ax in axes:grid(ax)
 fig.suptitle('Broader development panel: separate evaluation contract',y=.98,fontsize=16,fontweight='bold');fig.text(.075,.095,'Frozen previous-parent results; no V4 checkpoint569 mixed-source evaluation has run.',fontsize=9);fig.text(.075,.045,'Source denominators: arXiv 45,516; StackExchange 38,590; Wikimedia 46,103.',fontsize=9)
 figures.append(save(fig,'v4-569-broader-lm.svg','Three frozen earlier broader-panel evaluations; V4 not evaluated','Mixed-source development panel:130,209 scored labels at three checkpoints, with nine separate source slices. Science-terminal PPL62.10324143003107 at133411556 retained labels versus previous-parent-terminal14.631154356930713 at632823676 spans multiple phases; not an isolated phase effect. Source denominators:arXiv45516, StackExchange38590, Wikimedia46103. Separate from CFR; no reasoning or sealed-holdout claim.',{'aggregate_points':3,'source_slice_points':9,'aggregate_scored_labels':130209,'source_denominators':source_den}))
 timings=data['completed_run_timings']+data['intermediate_run_timings'];assert len(timings)==6 and timings[-1]['status']=='in_progress_intermediate';names=['Science\n104.52M','Filtered\n96.01M','Admitted\n143.22M','Stage1\n130.07M','Stage2\n130.11M','V4\n569 partial'];x=np.arange(6);fig,ax=plt.subplots(figsize=(11.5,5.3));fig.subplots_adjust(left=.095,right=.98,top=.82,bottom=.24);missing=[];drawn=0
 for j,(key,label,color) in enumerate([('valid_labels_per_guard_wall_second','Guard wall (approximate)','#637aa8'),('valid_labels_per_worker_second','Worker elapsed','#329283'),('valid_labels_per_loop_second','Training loop','#c58a36'),('valid_labels_per_training_excluding_hooks_second','Excluding measured hooks','#9767a6')]):
  first=True
  for i,r in enumerate(timings):
   value=r.get(key)
   if key=='valid_labels_per_training_excluding_hooks_second' and value is None and r.get('training_seconds_excluding_measured_hooks') is not None:value=r['phase_valid_labels']/r['training_seconds_excluding_measured_hooks']
   if value is None:missing.append({'stage':r['stage'],'denominator':label});continue
   drawn+=1;bar=ax.bar(x[i]+(j-1.5)*.19,value/1000,.17,color=color,label=label if first else None);first=False;ax.bar_label(bar,labels=[f'{value/1000:.2f}'],padding=3,fontsize=8)
 ax.set_xticks(x,names);ax.set_ylabel('Phase-local valid labels / second (thousands)');ax.set_title('Completed runs and an intermediate V4 boundary',fontsize=16,fontweight='bold',pad=23);ax.legend(loc='upper center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False,fontsize=8);grid(ax);ax.set_ylim(0,ax.get_ylim()[1]*1.12);fig.text(.095,.105,'V4 through569: loop5,358 labels/s; excluding measured hooks5,548 labels/s. Intermediate, model load excluded.',fontsize=9);fig.text(.095,.055,'Missing denominators omitted; startup-inclusive live wall rates are a separate CSV series. No GPU-kernel rate claim.',fontsize=9)
 figures.append(save(fig,'v4-569-throughput.svg','Measured valid-label throughput: five completed runs and intermediate V4','Five completed runs and one intermediate V4 boundary through569. V4 loop rate5358.397046451784 labels/s includes measured hooks; training excluding those hooks5547.727102367691 labels/s. Model load excluded from both. Missing guard and worker denominators omitted; live startup-inclusive wall rates are separately downloadable. No GPU-kernel throughput claim.',{'completed_runs':5,'intermediate_runs':1,'actual_bars':drawn,'omitted_missing_denominators':missing}))
 fig,ax=plt.subplots(figsize=(11.5,5.2));fig.subplots_adjust(left=.085,right=.98,top=.81,bottom=.22);cp=[];ev=[]
 for r in timings:
  assert all(r[k] is not None for k in ['training_loop_elapsed_seconds','checkpoint_hook_seconds','evaluation_hook_seconds']);cp.append(100*r['checkpoint_hook_seconds']/r['training_loop_elapsed_seconds']);ev.append(100*r['evaluation_hook_seconds']/r['training_loop_elapsed_seconds']);assert abs((cp[-1]+ev[-1])/100-r['checkpoint_plus_evaluation_fraction_of_loop'])<1e-12
 ax.bar(x,cp,.6,color='#637aa8',label='Checkpoint hooks');ax.bar(x,ev,.6,bottom=cp,color='#329283',label='Evaluation hooks')
 for i,total in enumerate(np.array(cp)+np.array(ev)):ax.text(i,total+.18,f'{total:.3f}%',ha='center',fontsize=10)
 ax.axhline(10,color='#ad5149',linewidth=1.2,linestyle='--',label='10% reference ceiling');ax.set_xticks(x,names);ax.set_ylabel('Measured hook seconds / loop seconds (%)');ax.set_ylim(0,10.8);grid(ax);fig.legend(*ax.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,.91),ncol=3,frameon=False,fontsize=9);fig.suptitle('Checkpoint and evaluation overhead',y=.98,fontsize=16,fontweight='bold');fig.text(.085,.095,'V4:115.92s checkpoint +2.57s evaluation /3,471.96s loop =3.413%. Intermediate through569.',fontsize=9);fig.text(.085,.045,'V4 evaluation includes baseline plus checkpoint; model load excluded. Reserved charges are not measured overhead.',fontsize=9)
 figures.append(save(fig,'v4-569-overhead.svg','Measured checkpoint and evaluation fractions of training-loop elapsed time','Five completed runs plus intermediate V4 through checkpoint569. V4 measured checkpoint115.91997592698317s plus evaluation2.569439060986042s divided by3471.9629468889907 loop seconds:3.412749986117801%. V4 evaluation includes baseline and checkpoint; full-boundary hooks included and model load excluded. This is not final-run overhead. The10% line is an engineering reference. Reserved charges are not measured overhead.',{'completed_runs':5,'intermediate_runs':1,'actual_hook_components':12,'reference_ceiling_percent':10,'missing_hook_values':0}))
 metadata={'schema':'sanitized_reproducible_static_charts_v1','input':{'file':'assets/v4-first-checkpoint-569/checkpoint-history.json','sha256':sha(raw),'bytes':len(raw),'frozen_utc':data['frozen_utc']},'builder':{'file':'scripts/build_v4_first_checkpoint_charts.py','sha256':sha(Path(__file__).read_bytes())},'runtime_versions':{'matplotlib':matplotlib.__version__,'numpy':np.__version__},'determinism':{'svg_hashsalt':'checkpoint-chart-history-20261029-v1','svg_date_metadata':None,'fonttype':'path','xml_metadata_removed':True,'css_removed':True},'charts':figures,'publication_performed':False}
 (OUT/'v4-569-chart-metadata.json').write_text(json.dumps(metadata,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(metadata,sort_keys=True))
if __name__=='__main__':build()
