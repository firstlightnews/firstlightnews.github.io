import json,glob,os,sys
src=sys.argv[1]; out='/home/claude/firstlightnews.github.io/data.json'
L=lambda p:json.load(open(p))
col=lambda c:{os.path.basename(p)[:-5]:L(p) for p in sorted(glob.glob(f'{src}/{c}/*.json'))}
arts=[dict(id=k,**v) for k,v in col('articles').items() if v.get('source')!='mr']
arts.sort(key=lambda a:str(a.get('published')),reverse=True)
# keep the last 3 days, plus each outlet's latest 3 so slow outlets are never empty
import datetime as _dt
_cut=(_dt.datetime.now(_dt.timezone.utc)-_dt.timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
_seen={}; _keep=[]
for a in arts:
    s=a.get('source'); _seen[s]=_seen.get(s,0)+1
    if str(a.get('published'))>=_cut or _seen[s]<=3: _keep.append(a)
arts=_keep
d={"weather":L(f'{src}/weather/today.json'),"digest":L(f'{src}/digest/today.json'),"status":L(f'{src}/meta/status.json'),
   "sports":col('sports'),"sportsnews":col('sportsnews'),"articles":arts[:300]}
assert len(d['digest']['items'])==10
ef='/home/claude/firstlightnews.github.io/edition.json'
try: ed=json.load(open(ef))
except Exception: ed={"no":0,"date":""}
day=d['digest']['date']
if ed.get('date')!=day: ed={"no":int(ed.get('no',0))+1,"date":day}
json.dump(ed,open(ef,'w'))
d['edition']=ed
json.dump(d,open(out,'w'),ensure_ascii=False,indent=1)
print('digest.date',d['digest']['date'],'articles',len(arts))
