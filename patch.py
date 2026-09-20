PAIRS = [["  let cols=n<=2?2:n<=12?3:4;if(hard)cols=Math.min(5,cols+1);\n  let bench=n>30?4:5;if(hard)bench-=1;if(boss||n<=4)bench=5;", "  let cols=n<=2?2:n<=10?3:4;if(hard)cols=Math.min(5,cols+1);\n  let bench=n<=2?5:4;if(hard)bench=3;\n  const ramp=Math.min(1,Math.max(0,(n-2)/28)),tough=hard||boss;\n  const diff=n<=2?{block:0,two:0,cap:0}:{block:tough?.34:.14+.2*ramp,two:tough?.3:.12+.18*ramp,cap:bench-(tough?0:(n<=6?2:1)),minB:tough?2:1};", 1], ["const spec=Object.assign({n,boss,hard,cols,bench},pic);", "const spec=Object.assign({n,boss,hard,cols,bench,diff},pic);", 1], ["function genShooters(spec,rng){\n  const {W,H}=spec,g=spec.cells.slice(),lanes=getLanes(W,H),rem={};let total=0;\n  for(const c of g)if(c){rem[c]=(rem[c]||0)+1;total++}\n  const seq=[];let guard=0;\n  while(total>0&&guard++<5000){\n    const cand=[];let sum=0;\n    for(const c in rem){if(rem[c]<=0)continue;const h=lapSim(g.slice(),W,H,lanes,c,1e9);if(h>0){const w=h*h;cand.push([c,h,w]);sum+=w}}\n    let r=rng()*sum,pick=cand[0];for(const x of cand){r-=x[2];if(r<=0){pick=x;break}}\n    const [c,h]=pick;let A=Math.min(h,rem[c]);\n    if(A>=10&&rem[c]-A>=3)A=Math.floor(A/5)*5;\n    lapSim(g,W,H,lanes,c,A);rem[c]-=A;total-=A;seq.push({c,a:A,ord:seq.length});\n  }\n  const K=spec.cols,cols=Array.from({length:K},()=>[]);\n  if(spec.n<=4)seq.forEach((s,i)=>cols[i%K].push(s));\n  else for(const s of seq){const mn=Math.min(...cols.map(c=>c.length));const ok=cols.filter(c=>c.length<=mn+1);ok[Math.floor(rng()*ok.length)].push(s)}\n  return cols;\n}\n", "function genShooters(spec,rng){\n  /* Builds a reference playthrough and deals its launch order into columns (every column is a\n     subsequence of it), so a solution always exists. Harder levels add \"blockers\" (shooters whose\n     colour is still hidden: they must be parked on the bench) and \"two-lap\" shooters (more ammo than\n     one lap can use). The reference never uses more than D.cap bench seats. */\n  const {W,H}=spec,lanes=getLanes(W,H),D=spec.diff||{block:0,two:0,cap:0};\n  const nice=(r,u)=>{if(u<=12)return u;const m=Math.min(20,u);return 5*(1+Math.floor(r()*Math.max(1,Math.floor(m/5))))};\n  let seq=null;\n  for(let att=0;att<60&&!seq;att++){\n    const g=spec.cells.slice(),un={};let left=0;\n    for(const c of g)if(c){un[c]=(un[c]||0)+1;left++}\n    const out=[],bench=[],hard=att<40;let guard=0;\n    while(left>0&&guard++<6000){\n      let did=false;\n      for(let i=0;i<bench.length;i++){const b=bench[i];const h=lapSim(g.slice(),W,H,lanes,b.c,b.a);if(h>0){lapSim(g,W,H,lanes,b.c,b.a);b.a-=h;left-=h;if(b.a<=0)bench.splice(i,1);did=true;break}}\n      if(did)continue;\n      const cand=[];let sum=0;\n      for(const c in un){if(un[c]<=0)continue;const h=lapSim(g.slice(),W,H,lanes,c,1e9);if(h>0){const w=h*h;cand.push([c,h,w]);sum+=w}}\n      const hidden=Object.keys(un).filter(c=>un[c]>0&&!cand.some(x=>x[0]===c));\n      if(hard&&hidden.length&&bench.length<D.cap&&rng()<D.block){\n        const c=hidden[Math.floor(rng()*hidden.length)],A=Math.min(un[c],nice(rng,un[c]));\n        un[c]-=A;out.push({c,a:A,ord:out.length,blk:1});bench.push({c,a:A});continue;\n      }\n      if(!cand.length)break;\n      let r=rng()*sum,pick=cand[0];for(const x of cand){r-=x[2];if(r<=0){pick=x;break}}\n      const [c,h]=pick;let A=Math.min(h,un[c]);\n      if(A>=10&&un[c]-A>=3)A=Math.floor(A/5)*5;\n      if(hard&&un[c]-A>0&&bench.length<D.cap&&rng()<D.two)A+=Math.min(un[c]-A,2+Math.floor(rng()*6));\n      const hits=lapSim(g,W,H,lanes,c,A);\n      un[c]-=A;left-=hits;out.push({c,a:A,ord:out.length});\n      if(A>hits)bench.push({c,a:A-hits});\n    }\n    if(left===0&&(!hard||out.filter(o=>o.blk).length>=(D.minB||0)))seq=out;\n  }\n  const K=spec.cols,cols=Array.from({length:K},()=>[]);\n  if(spec.n<=2)seq.forEach((s,i)=>cols[i%K].push(s));\n  else for(const s of seq){const mn=Math.min(...cols.map(c=>c.length));const ok=cols.filter(c=>c.length<=mn+1);ok[Math.floor(rng()*ok.length)].push(s)}\n  return cols;\n}\n", 1], ["let SV={unl:1,stars:{},coins:200,snd:true,gal:[],tut:{}};", "let SV={unl:1,stars:{},coins:200,snd:true,gal:[],tut:{},inv:{hint:3,hammer:1,slot:1}};", 1], ["  deny(){tone(180,.12,'square',.05,140)}", "  beat(){tone(72,.12,'sine',.28,48);tone(72,.1,'sine',.2,48,.17)},\n  deny(){tone(180,.12,'square',.05,140)}", 1], ["aimAll:n<=8,", "aimAll:n<=1,hbT:0,", 1], ["auto:n<=2,", "auto:n<=1,", 1], ["speed:Math.max(12,Math.min(24,P/3.3))", "speed:Math.max(14,Math.min(26,P/3))", 1], ["  ['#ovWin','#ovLose','#ovPause'].forEach(s=>$(s).hidden=true);", "  ['#ovWin','#ovLose','#ovPause','#ovAd'].forEach(s=>$(s).hidden=true);", 1], ["  setHammer(false);updCoins();resize();placeAll(true);", "  setHammer(false);updCoins();updBoost();resize();placeAll(true);", 1], ["S.aimAll=S.n<=8||S.hintAimT>0;", "S.aimAll=S.n<=1||S.hintAimT>0;\n  if(S.state==='play'){const free=S.bench.filter(x=>!x).length;if(free<=1&&S.bench.some(Boolean)){S.hbT-=dt;if(S.hbT<=0){S.hbT=free===0?.55:.85;sfx.beat()}}else S.hbT=0}", 1], ["if(!S.aimAll&&!a.zero)return;", "if(!S.aimAll)return;", 2], ["if(cx>=0&&cy>=0&&cx<S.W&&cy<S.H&&doHammer(cx,cy)){SV.coins-=100;S.boost=true;save();updCoins();setHammer(false)}", "if(cx>=0&&cy>=0&&cx<S.W&&cy<S.H&&doHammer(cx,cy)){pay('hammer',$('#bHammer'));S.boost=true;setHammer(false)}", 1], ["$('#bHint').onclick=e=>{ac();if(!S||S.state!=='play')return;const b=e.currentTarget;if(SV.coins<40)return deny(b,'Не хватает монет. Их дают за смены и лихорадку');const m=bestMove();if(!m)return;SV.coins-=40;S.boost=true;S.hint=m.id;S.hintT=4;S.hintAimT=6;save();updCoins();sfx.click()};\n$('#bHammer').onclick=e=>{ac();if(!S||S.state!=='play')return;const b=e.currentTarget;if(S.hammer){setHammer(false);return}if(SV.coins<100)return deny(b,'Не хватает монет. Их дают за смены и лихорадку');setHammer(true);sfx.click();toast('Тапни по картине: молот снесет квадрат 3×3',2600)};\n$('#bSlot').onclick=e=>{ac();if(!S||S.state!=='play')return;const b=e.currentTarget;if(S.bench.length>=7)return deny(b,'Больше мест не поместится');if(SV.coins<150)return deny(b,'Не хватает монет. Их дают за смены и лихорадку');SV.coins-=150;S.boost=true;S.bench.push(null);save();updCoins();layout();sfx.click()};", "const PRICE={hint:60,hammer:150,slot:200};\nfunction updBoost(){if(!SV.inv)SV.inv={hint:0,hammer:0,slot:0};for(const [k,id] of [['hint','#bHint'],['hammer','#bHammer'],['slot','#bSlot']]){const p=document.querySelector(id+' .price');if(p)p.textContent=SV.inv[k]>0?'×'+SV.inv[k]:PRICE[k]}}\nfunction pay(kind,btn){if(SV.inv[kind]>0){SV.inv[kind]--;save();updBoost();return true}if(SV.coins<PRICE[kind]){deny(btn,'Не хватает монет. Их дают за смены, звезды и лихорадку');return false}SV.coins-=PRICE[kind];save();updCoins();updBoost();return true}\n$('#bHint').onclick=e=>{ac();if(!S||S.state!=='play')return;const b=e.currentTarget;const m=bestMove();if(!m)return;if(!pay('hint',b))return;S.boost=true;S.hint=m.id;S.hintT=4;S.hintAimT=6;sfx.click()};\n$('#bHammer').onclick=e=>{ac();if(!S||S.state!=='play')return;const b=e.currentTarget;if(S.hammer){setHammer(false);return}if(SV.inv.hammer<=0&&SV.coins<PRICE.hammer)return deny(b,'Не хватает монет. Их дают за смены, звезды и лихорадку');setHammer(true);sfx.click();toast('Тапни по картине: молот снесет квадрат 3×3',2600)};\n$('#bSlot').onclick=e=>{ac();if(!S||S.state!=='play')return;const b=e.currentTarget;if(S.bench.length>=7)return deny(b,'Больше мест не поместится');if(!pay('slot',b))return;S.boost=true;S.bench.push(null);layout();sfx.click()};", 1], ["function showLose(){toastEl.classList.add('hide');\n  const free=!S.cont;\n  $('#loseCont').textContent=free?'+1 место и дальше (бесплатно)':'+1 место и дальше · 150';\n  $('#ovLose').hidden=false;\n}\n$('#loseCont').onclick=()=>{\n  if(S.cont){if(SV.coins<150){deny($('#loseCont'),'Не хватает монет');return}SV.coins-=150;save();updCoins()}\n  S.cont=true;S.bench.push(S.over);S.over=null;S.state='play';layout();$('#ovLose').hidden=true;\n};", "function showLose(){toastEl.classList.add('hide');\n  const free=S.n<=3&&!S.cont;\n  $('#loseAd').hidden=free;\n  $('#loseCont').textContent=free?'+1 место и дальше (бесплатно)':'+1 место за 150 монет';\n  $('#ovLose').hidden=false;\n}\nfunction contRun(){S.cont=true;S.bench.push(S.over);S.over=null;S.state='play';layout();$('#ovLose').hidden=true}\n$('#loseCont').onclick=()=>{\n  const free=S.n<=3&&!S.cont;\n  if(!free){if(SV.coins<150){deny($('#loseCont'),'Не хватает монет');return}SV.coins-=150;save();updCoins()}\n  contRun();\n};\n$('#loseAd').onclick=()=>{$('#ovLose').hidden=true;$('#ovAd').hidden=false;let t=3;$('#adT').textContent=t;const iv=setInterval(()=>{t--;$('#adT').textContent=t;if(t<=0){clearInterval(iv);$('#ovAd').hidden=true;contRun()}},1000)};", 1], ["<div class=\"row col\"><button class=\"btn primary\" id=\"loseCont\">+1 место и дальше</button><button class=\"btn ghost\" id=\"loseRetry\">Начать смену заново</button></div>", "<div class=\"row col\"><button class=\"btn primary\" id=\"loseAd\">Смотреть рекламу: +1 место</button><button class=\"btn ghost\" id=\"loseCont\">+1 место за 150 монет</button><button class=\"btn ghost\" id=\"loseRetry\">Начать смену заново</button></div>", 1], ["    <div class=\"ov\" id=\"ovPause\" hidden>", "    <div class=\"ov\" id=\"ovAd\" hidden><div class=\"card\"><div class=\"eyebrow\">Реклама · демо</div><h2 id=\"adT\">3</h2><p>Здесь будет ролик рекламодателя. В демо просто подожди пару секунд, место добавится само.</p></div></div>\n\n    <div class=\"ov\" id=\"ovPause\" hidden>", 1], ["once('t2','Стрелок бьет только крайний кубик в ряду. Сначала снимай внешний слой, потом доберешься до сердца',6000)", "once('t2','Внутренние кубики закрыты. Смотри, какой цвет сейчас снаружи картины, и запускай стрелков этого цвета',6000)", 1], ["once('t3','Конвейер держит несколько стрелков сразу. Запускай пачкой и лови лихорадку',5000)", "once('t3','Бывает, нужный стрелок стоит за лишним. Отправь лишнего на скамейку, он пригодится, когда откроется его цвет. Только не забей скамейку',7000)", 1], ["<br>Над стрелком видно, что будет: <span class=\"tag\" style=\"background:#2fcb82\">собьет 12</span> отлично, <span class=\"tag\" style=\"background:#9a93c4\">нет целей</span> запускать рано.", "<br>«Подсказка» покажет прогноз над стрелками: <span class=\"tag\" style=\"background:#2fcb82\">собьет 12</span> отлично, <span class=\"tag\" style=\"background:#9a93c4\">нет целей</span> пока рано.", 1], ["SV.coins+=coins;SV.stars[S.n]=", "if(S.spec.boss){SV.inv.hint++;SV.inv.hammer++}\n  SV.coins+=coins;SV.stars[S.n]=", 1], ["const sc=(h===sh.a?1000:0)+h*3-(h===0?2000:0)-sh.ord*.01;", "const sc=(h===sh.a?1000:0)+h*3-(h===0?2000:0)-(h===0&&S.bench.includes(sh)?3000:0)-sh.ord*.01;", 1], ["function isSpriteLevel(n){const boss=n%10===0;return n!==1&&(boss||n%4!==3)}", "function isSpriteLevel(n){const boss=n%10===0,hard=!boss&&n%5===0;return n!==1&&(boss||hard||n%4!==3)}", 1], ["if(S.state==='lose'&&S.loseT>0){S.loseT-=dt;if(S.loseT<=0)showLose()}", "if(S.state==='lose'&&S.loseT>0){S.loseT-=dt;if(S.loseT<=0)showLose()}\n  if(S.state==='play'&&!S.belt.length&&!S.wait.length&&!S.proj.length&&!S.bench.includes(null)){const q=[...S.cols.map(c=>c[0]),...S.bench].filter(Boolean);if(q.length&&q.every(sh=>S.aim[sh.id]===0)){S.over=null;S.state='lose';S.loseT=.4;sfx.lose();vib([60,40,60])}}", 1], ["/* ================= game state ================= */", "/* ================= analytics =================\n   Anonymous gameplay events (random player id, no personal data) -> Supabase table \"events\".\n   The key is the public insert-only key; reading happens only through the stats function. */\nconst AN={url:'https://vajpghoztikbcnvfkxtp.supabase.co',key:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhanBnaG96dGlrYmNudmZreHRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk4ODYyMDIsImV4cCI6MjEwNTQ2MjIwMn0.3OIKjC14WBKZmvftmptfNbhd2wtKXxCR5r3x1Lxk3TI'};\nconst PID=(()=>{try{let p=localStorage.getItem('smena-pid');if(!p){p=(crypto.randomUUID?crypto.randomUUID():Date.now().toString(36)+Math.random().toString(36).slice(2));localStorage.setItem('smena-pid',p);localStorage.setItem('smena-first',String(Date.now()))}return p}catch(e){return 'anon-'+Math.random().toString(36).slice(2)}})();\nconst SID=Math.random().toString(36).slice(2,10);\nconst PLAT=location.protocol==='file:'?'apk':((matchMedia('(display-mode: standalone)').matches||matchMedia('(display-mode: fullscreen)').matches||navigator.standalone)?'pwa':'web');\nconst DAY=(()=>{try{return Math.floor((Date.now()-Number(localStorage.getItem('smena-first')||Date.now()))/864e5)}catch(e){return 0}})();\nlet AQ=[];try{AQ=JSON.parse(localStorage.getItem('smena-aq')||'[]')||[]}catch(e){AQ=[]}\nfunction aqSave(){try{localStorage.setItem('smena-aq',JSON.stringify(AQ))}catch(e){}}\nfunction track(ev,d){\n  if(!AN.url.startsWith('http'))return;\n  d=d||{};AQ.push({pid:PID,sid:SID,ev,lvl:d.lvl||null,plat:PLAT,ts:new Date().toISOString(),data:d});\n  if(AQ.length>300)AQ=AQ.slice(-300);aqSave();\n  clearTimeout(track.t);track.t=setTimeout(flush,/win|lose|quit/.test(ev)?300:2500);\n}\nfunction flush(keep){\n  if(!AQ.length||flush.busy||!AN.url.startsWith('http'))return;\n  const batch=AQ.slice(0,60);flush.busy=true;\n  fetch(AN.url+'/rest/v1/events',{method:'POST',keepalive:!!keep,headers:{apikey:AN.key,...(AN.key.startsWith('ey')?{Authorization:'Bearer '+AN.key}:{}),'Content-Type':'application/json',Prefer:'return=minimal'},body:JSON.stringify(batch)})\n    .then(r=>{if(r.ok){AQ=AQ.slice(batch.length);aqSave()}}).catch(()=>{})\n    .finally(()=>{flush.busy=false;if(AQ.length&&!keep)setTimeout(flush,5000)});\n}\naddEventListener('pagehide',()=>flush(true));\ndocument.addEventListener('visibilitychange',()=>{if(document.hidden)flush(true)});\nfunction progPct(){return S&&S.total?Math.round((1-S.left/S.total)*100):0}\n\n/* ================= game state ================= */", 1], ["function startLevel(n){\n  const spec=levelSpec(n),rng=rngOf(n*9973+17);", "function startLevel(n){\n  if(S&&S.state==='play'&&S.n)track('level_quit',{lvl:S.n,secs:Math.round(S.t),prog:progPct()});\n  SV.tries=SV.tries||{};SV.tries[n]=(SV.tries[n]||0)+1;save();\n  const spec=levelSpec(n),rng=rngOf(n*9973+17);", 1], ["  tutorial('start');\n  if(!SV.tut.help)showHelp();", "  tutorial('start');\n  track('level_start',{lvl:n,tries:SV.tries[n],unl:SV.unl});\n  if(!SV.tut.help)showHelp();", 1], ["save();updCoins();sfx.win();toastEl.classList.add('hide');", "save();updCoins();sfx.win();toastEl.classList.add('hide');\n  track('level_win',{lvl:S.n,stars:st,secs:Math.round(S.t),tries:SV.tries&&SV.tries[S.n]||1,bench:S.benchMax,cont:S.cont,boost:!!S.boost});", 1], ["function showLose(){toastEl.classList.add('hide');", "function showLose(){toastEl.classList.add('hide');\n  track('level_lose',{lvl:S.n,secs:Math.round(S.t),prog:progPct(),reason:S.over?'bench':'stuck',cont:S.cont});", 1], ["function contRun(){S.cont=true;", "function contRun(via){track('continue',{lvl:S.n,via:via||'coins'});S.cont=true;", 1], ["  contRun();\n};", "  contRun(free?'free':'coins');\n};", 1], ["if(t<=0){clearInterval(iv);$('#ovAd').hidden=true;contRun()}", "if(t<=0){clearInterval(iv);$('#ovAd').hidden=true;contRun('ad')}", 1], ["function pay(kind,btn){", "function pay(kind,btn){track('booster',{lvl:S&&S.n,kind,via:SV.inv[kind]>0?'inv':SV.coins>=PRICE[kind]?'coins':'no_money'});", 1], ["function showHelp(after){", "function showHelp(after){track('help_open',{lvl:S&&S.n});", 1], ["function showMenu(){S=null;", "function showMenu(){if(S&&(S.state==='play'||S.state==='lose'))track('level_quit',{lvl:S.n,secs:Math.round(S.t),prog:progPct()});S=null;", 1], ["renderMenu();\nloadSkin();", "renderMenu();\nloadSkin();\ntrack('app_open',{unl:SV.unl,day:DAY,stars:Object.values(SV.stars).reduce((a,b)=>a+b,0)});", 1]]
p = 'index.html'
s = open(p, encoding='utf-8').read()
for old, new, cnt in PAIRS:
    assert s.count(old) == cnt, old[:80]
    s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)

import os
os.makedirs('skin', exist_ok=True)
open('skin/stats.html','w',encoding='utf-8').write(r'''<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Смена · статистика</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap">
<style>
:root{--bg:#f4f1ff;--card:#fff;--ink:#2d2a54;--muted:#6f6a99;--line:#e6e0fa;--accent:#6d4fe0;--accent-2:#b9a8ff;--good:#1f9a61;--warn:#c77700;--bad:#d6334f;--edge:#d4c9f5}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Nunito,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding-inline:16px;padding-block:20px 40px;display:flex;flex-direction:column;gap:16px}
header{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;flex-wrap:wrap}
h1{margin:0;font-weight:900;font-size:clamp(24px,6vw,34px);line-height:1.05}
h1 span{color:var(--accent)}
.sub{color:var(--muted);font-weight:700;font-size:14px;margin-top:4px}
button{font:inherit;font-weight:800;border:0;border-radius:12px;padding:10px 14px;background:var(--accent);color:#fff;cursor:pointer;box-shadow:0 3px 0 #4b33a8}
button:focus-visible{outline:3px solid var(--accent-2);outline-offset:2px}
.note{background:#fff7dd;border:1px solid #f1d48a;border-radius:14px;padding:12px 14px;font-weight:700;font-size:14px;line-height:1.45}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.tile{background:var(--card);border-radius:16px;padding:14px;box-shadow:0 3px 0 var(--edge)}
.tile .k{font-size:12px;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.tile .v{font-size:30px;font-weight:900;font-variant-numeric:tabular-nums;margin-top:2px}
.tile .h{font-size:13px;font-weight:700;color:var(--muted)}
.card{background:var(--card);border-radius:18px;padding:16px;box-shadow:0 3px 0 var(--edge)}
.card h2{margin:0 0 2px;font-size:18px;font-weight:900}
.card p.lead{margin:0 0 12px;color:var(--muted);font-weight:700;font-size:14px}
.chart{position:relative;width:100%;overflow-x:auto}
.chart svg{display:block}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:#fff;font-size:13px;font-weight:700;padding:7px 10px;border-radius:10px;white-space:nowrap;transform:translate(-50%,-110%);opacity:0;transition:opacity .1s}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}
th{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;font-weight:800}
th:first-child,td:first-child,td.l,th.l{text-align:left}
.pill{display:inline-block;border-radius:999px;padding:2px 9px;font-size:12px;font-weight:900}
.pill.easy{background:#e3f6ec;color:var(--good)}.pill.ok{background:#ece7ff;color:var(--accent)}.pill.hard{background:#fff0d6;color:var(--warn)}.pill.wall{background:#ffe3e8;color:var(--bad)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.kv{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--line);font-weight:700;font-size:14px}
.kv span:last-child{font-variant-numeric:tabular-nums}
.muted{color:var(--muted)}
.help{font-size:14px;line-height:1.5;color:var(--muted);font-weight:600}
.help b{color:var(--ink)}
</style>
</head><body>
<div class="wrap">
  <header>
    <div><h1>Пиксельная смена · <span>статистика</span></h1><div class="sub" id="upd">Загрузка…</div></div>
    <button id="refresh">Обновить</button>
  </header>
  <div class="note" id="demo" hidden>Это пример данных: аналитика еще не подключена к базе.</div>
  <div class="note" id="empty" hidden>Пока нет ни одного игрока. Раздай ссылку на игру, и через пару минут здесь появятся цифры: <a href="../" id="gameLink">открыть игру</a>.</div>
  <section class="tiles" id="tiles"></section>
  <section class="card">
    <h2>Сколько игроков дошли до уровня</h2>
    <p class="lead">Где столбик резко падает, там люди бросают игру. Это главное место для правок.</p>
    <div class="chart" id="funnel"></div>
  </section>
  <section class="card">
    <h2>Какой процент попыток заканчивается победой</h2>
    <p class="lead">Норма для казуалки: легкие уровни 80-95%, сложные 40-60%. Ниже 25% уровень превращается в стену.</p>
    <div class="chart" id="winrate"></div>
  </section>
  <section class="card">
    <h2>Уровни подробно</h2>
    <div class="scroll"><table id="tbl"></table></div>
  </section>
  <section class="grid2">
    <div class="card"><h2>Бустеры</h2><div id="boost"></div></div>
    <div class="card"><h2>Продолжения после проигрыша</h2><div id="cont"></div></div>
    <div class="card"><h2>Откуда играют</h2><div id="plat"></div></div>
  </section>
  <section class="card help">
    <b>Как читать.</b> «Дошли» это сколько разных игроков хотя бы раз начали уровень. «Бросили здесь» это игроки, для которых этот уровень оказался последним и которые не заходили больше суток. Возврат D1 и D7 считается от тех, кто впервые зашел хотя бы день или неделю назад.
  </section>
</div>
<script>
const AN={url:'https://vajpghoztikbcnvfkxtp.supabase.co',key:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhanBnaG96dGlrYmNudmZreHRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk4ODYyMDIsImV4cCI6MjEwNTQ2MjIwMn0.3OIKjC14WBKZmvftmptfNbhd2wtKXxCR5r3x1Lxk3TI'};
const $=s=>document.querySelector(s);
const pct=(a,b)=>b?Math.round(a/b*100):null;
function sample(){
  const levels=[];let p=48;
  for(let l=1;l<=16;l++){const wr=[.97,.95,.9,.62,.4,.7,.85,.55,.75,.3,.8,.6,.5,.66,.35,.5][l-1];const starts=Math.round(p/wr*.9)+1;const wins=Math.round(p*.92);
    levels.push({lvl:l,players:p,starts,winners:wins,wins,losses:Math.max(0,starts-wins),quits:Math.round(p*.05),continues:Math.round(p*(1-wr)*.4),boosters:Math.round(p*(1-wr)),win_secs:30+l*3,tries:+(1/wr).toFixed(2),stars:2.3});
    p=Math.max(1,Math.round(p*(l===5||l===10?.72:.93)))}
  return {updated:new Date().toISOString(),players:48,players_today:21,new_today:9,events:3120,d1_base:39,d1:15,d7_base:12,d7:2,avg_session_min:7.4,levels,
    stopped:{4:3,5:6,8:2,10:7,15:4},boosters:{'hint / inv':41,'hint / coins':12,'hammer / inv':18,'slot / coins':5},continues:{free:9,ad:14,coins:3},platforms:{web:30,pwa:11,apk:7}};
}
async function load(){
  $('#upd').textContent='Загрузка…';
  let d;
  if(!AN.url.startsWith('http')){d=sample();$('#demo').hidden=false}
  else{
    try{const r=await fetch(AN.url+'/rest/v1/rpc/game_stats',{method:'POST',headers:{apikey:AN.key,...(AN.key.startsWith('ey')?{Authorization:'Bearer '+AN.key}:{}),'Content-Type':'application/json'},body:'{}'});d=await r.json();if(!r.ok)throw new Error(d.message||r.status)}
    catch(e){$('#upd').textContent='Не удалось загрузить: '+e.message+'. База Supabase засыпает после недели без игроков, открой ее в панели Supabase, чтобы разбудить.';return}
  }
  render(d);
}
function tile(k,v,h){return `<div class="tile"><div class="k">${k}</div><div class="v">${v}</div><div class="h">${h||''}</div></div>`}
function render(d){
  const t=new Date(d.updated);$('#upd').textContent='Обновлено '+t.toLocaleString('ru-RU',{day:'numeric',month:'long',hour:'2-digit',minute:'2-digit'});
  $('#empty').hidden=d.players>0;
  const d1=pct(d.d1,d.d1_base),d7=pct(d.d7,d.d7_base);
  $('#tiles').innerHTML=tile('Игроков всего',d.players,'новых сегодня: '+d.new_today)+tile('Играли за сутки',d.players_today,'уникальных игроков')
    +tile('Возврат D1',d1==null?'нет данных':d1+'%',d.d1_base?`${d.d1} из ${d.d1_base} · цель 35-40%`:'нужны игроки старше суток')
    +tile('Возврат D7',d7==null?'нет данных':d7+'%',d.d7_base?`${d.d7} из ${d.d7_base} · цель от 15%`:'нужны игроки старше недели')
    +tile('Средняя сессия',d.avg_session_min==null?'нет':d.avg_session_min+' мин','от первого до последнего события');
  const L=(d.levels||[]).filter(x=>x.lvl>0&&x.lvl<=200);
  bars('#funnel',L.map(x=>({x:x.lvl,v:x.players,tip:`Уровень ${x.lvl}: дошли ${x.players}, прошли ${x.winners}`})),{max:Math.max(1,...L.map(x=>x.players)),fmt:v=>v});
  bars('#winrate',L.map(x=>{const w=pct(x.wins,x.wins+x.losses);return{x:x.lvl,v:w==null?0:w,tip:`Уровень ${x.lvl}: ${w==null?'нет попыток':w+'% побед'} (${x.wins} побед, ${x.losses} поражений)`}}),{max:100,fmt:v=>v+'%',ref:[25,50,85]});
  const rate=w=>w==null?'':w>=85?'<span class="pill easy">легко</span>':w>=50?'<span class="pill ok">норма</span>':w>=25?'<span class="pill hard">трудно</span>':'<span class="pill wall">стена</span>';
  let h='<tr><th>Уровень</th><th>Дошли</th><th>Прошли</th><th>Победы</th><th>Поражения</th><th>Попыток до победы</th><th>Время победы</th><th>Бросили здесь</th><th>Бустеры</th><th>Продолжения</th><th class="l">Оценка</th></tr>';
  for(const x of L){const w=pct(x.wins,x.wins+x.losses);h+=`<tr><td><b>${x.lvl}</b></td><td>${x.players}</td><td>${x.winners}</td><td>${x.wins}</td><td>${x.losses}</td><td>${x.tries??''}</td><td>${x.win_secs!=null?x.win_secs+' с':''}</td><td>${(d.stopped||{})[x.lvl]||0}</td><td>${x.boosters}</td><td>${x.continues}</td><td class="l">${rate(w)}</td></tr>`}
  $('#tbl').innerHTML=h;
  const kv=(o,map)=>{const e=Object.entries(o||{}).sort((a,b)=>b[1]-a[1]);return e.length?e.map(([k,v])=>`<div class="kv"><span>${map?map(k):k}</span><span>${v}</span></div>`).join(''):'<div class="muted">Пока пусто</div>'};
  const tr=k=>k.replace('hint','Подсказка').replace('hammer','Молот').replace('slot','+Место').replace('/ inv','· из запаса').replace('/ coins','· за монеты').replace('/ no_money','· не хватило монет');
  $('#boost').innerHTML=kv(d.boosters,tr);
  $('#cont').innerHTML=kv(d.continues,k=>({free:'Бесплатно (уровни 1-3)',ad:'Реклама',coins:'За монеты'})[k]||k);
  $('#plat').innerHTML=kv(d.platforms,k=>({web:'Браузер',pwa:'Иконка на экране (PWA)',apk:'Android-приложение'})[k]||k);
}
function bars(sel,data,o){
  const el=$(sel);if(!data.length){el.innerHTML='<div class="muted">Пока нет данных</div>';return}
  const bw=Math.max(18,Math.min(44,Math.floor((el.clientWidth-50)/data.length)-4)),gap=4,W=40+data.length*(bw+gap)+10,Hh=200,top=16,bottom=26,ph=Hh-top-bottom;
  const y=v=>top+ph-(v/o.max)*ph;
  let s=`<svg width="${W}" height="${Hh}" viewBox="0 0 ${W} ${Hh}" role="img">`;
  const ticks=o.max===100?[0,25,50,75,100]:[0,Math.round(o.max/2),o.max];
  for(const t of ticks)s+=`<line x1="36" x2="${W}" y1="${y(t)}" y2="${y(t)}" stroke="#e6e0fa" stroke-width="1"/><text x="30" y="${y(t)+4}" text-anchor="end" font-size="11" font-weight="700" fill="#6f6a99">${o.fmt(t)}</text>`;
  data.forEach((d,i)=>{const x=40+i*(bw+gap),yy=y(d.v),h=Math.max(0,top+ph-yy);
    s+=`<g class="b" data-i="${i}"><rect x="${x-2}" y="${top}" width="${bw+4}" height="${ph}" fill="transparent"/><path d="M${x},${top+ph} V${yy+Math.min(4,h)} q0,-4 4,-4 h${bw-8} q4,0 4,4 V${top+ph} Z" fill="#6d4fe0"/></g>`;
    s+=`<text x="${x+bw/2}" y="${Hh-8}" text-anchor="middle" font-size="11" font-weight="800" fill="#6f6a99">${d.x}</text>`});
  s+='</svg><div class="tip"></div>';el.innerHTML=s;
  const tip=el.querySelector('.tip');
  el.querySelectorAll('g.b').forEach(g=>{g.addEventListener('pointerenter',e=>{const d=data[+g.dataset.i];tip.textContent=d.tip;const r=g.getBoundingClientRect(),pr=el.getBoundingClientRect();tip.style.left=(r.left-pr.left+r.width/2+el.scrollLeft)+'px';tip.style.top=(y(d.v)+0)+'px';tip.style.opacity=1;g.querySelector('path').setAttribute('fill','#4b33a8')});
    g.addEventListener('pointerleave',()=>{tip.style.opacity=0;g.querySelector('path').setAttribute('fill','#6d4fe0')})});
}
$('#refresh').onclick=load;load();
</script>
</body></html>
''')
w=open('sw.js',encoding='utf-8').read()
open('sw.js','w',encoding='utf-8').write(w.replace("'smena-v2'","'smena-v3'"))
