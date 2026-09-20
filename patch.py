import io,sys,hashlib

P='index.html'
s=io.open(P,encoding='utf-8').read()

PAIRS=[
("function fetchRecord(n){if(!AN.url.startsWith('http')||!S)return;S.lbRec=undefined;rpc('leaderboard',{p_lvl:n,p_pid:PID}).then(d=>{if(S&&S.n===n)S.lbRec=d.record==null?null:d.record}).catch(()=>{})}",
 "function fetchRecord(n){if(!AN.url.startsWith('http')||!S)return;S.lbRec=undefined;S.lbMine=false;rpc('leaderboard',{p_lvl:n,p_pid:PID}).then(d=>{if(S&&S.n===n){S.lbRec=d.record==null?null:d.record;S.lbMine=!!(d.time_top||[]).some(r=>r.rank===1&&r.me)}}).catch(()=>{})}",1),

("  if(!S.cont&&SV.nick&&typeof S.lbRec==='number'&&secs<S.lbRec){prize=100;prizeTxt='Рекорд смены! Ты быстрее всех: +100'}",
 "  if(!S.cont&&SV.nick&&typeof S.lbRec==='number'&&secs<S.lbRec&&!S.lbMine){prize=100;prizeTxt='Рекорд смены! Ты быстрее всех: +100'}",1),

("  else if(pb&&secs<pb){prize=15;prizeTxt='Личный рекорд: +15'}",
 "  else if(S.lbMine&&typeof S.lbRec==='number'&&secs<S.lbRec){prize=15;prizeTxt='Свой же рекорд смены побит: +15'}\n  else if(pb&&secs<pb){prize=15;prizeTxt='Личный рекорд: +15'}",1),
]

for old,new,cnt in PAIRS:
    if s.count(old)!=cnt:
        print('MISS %d/%d: %s'%(s.count(old),cnt,old[:70]));sys.exit(1)
    s=s.replace(old,new,cnt)

io.open(P,'w',encoding='utf-8').write(s)

w=io.open('sw.js',encoding='utf-8').read().replace("const CACHE = 'smena-v3';","const CACHE = 'smena-v4';",1)
io.open('sw.js','w',encoding='utf-8').write(w)

print('OK',len(s),hashlib.sha256(s.encode()).hexdigest()[:16])
