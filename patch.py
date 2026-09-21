import io,re,time,sys
P='index.html'
s=io.open(P,encoding='utf-8').read()
def sub(old,new):
    global s
    if s.count(old)!=1:print('MISS',s.count(old),old[:70]);sys.exit(1)
    s=s.replace(old,new,1)

# haptic vocabulary: tick (took it), peek (checking), cancel (armed), back (returned), go (launched)
sub("function vib(p){",
"""function hap(k){try{if(NATIVE&&CP.Haptics){
    if(k==='cancel')nativeCall(()=>CP.Haptics.notification({type:'WARNING'}));
    else nativeCall(()=>CP.Haptics.impact({style:k==='go'?'HEAVY':k==='peek'?'MEDIUM':'LIGHT'}));
  }else if(navigator.vibrate)navigator.vibrate({tick:6,peek:[10,45,10],cancel:[28,45,28],back:8,go:20}[k]||8)}catch(e){}}
function vib(p){""")

# the shooter under the finger follows it a little, grows while checking, fades when cancel is armed
sub("  const c=sh.c;ctx.save();ctx.globalAlpha=alpha;ctx.translate(x,y);",
"""  const c=sh.c;ctx.save();ctx.globalAlpha=alpha;ctx.translate(x,y);
  const pr=S&&S.press&&S.press.id===sh.id?S.press:null;
  if(pr){const k=Math.min(1,(S.t-pr.t0)/.16);ctx.translate(pr.ox*k,pr.oy*k);
    if(pr.cancel){ctx.globalAlpha=alpha*.5;ctx.rotate(Math.sin(S.t*28)*.06);ctx.scale(.9,.9)}
    else{const sc=pr.peek?1.14+.03*Math.sin(S.t*9):1-.06*k;ctx.scale(sc,sc)}}""")

sub("function pressStart(kind,i,sh,x,y){S.press={kind,i,id:sh.id,x,y,t0:S.t,cells:lapCells(S.g.slice(),S.W,S.H,S.lanes,sh.c,sh.a)}}",
"""function pressStart(kind,i,sh,x,y){S.press={kind,i,id:sh.id,x,y,t0:S.t,ox:0,oy:0,peek:false,cancel:false,cells:lapCells(S.g.slice(),S.W,S.H,S.lanes,sh.c,sh.a)};hap('tick')}
function pressPos(p){return p.kind==='b'?benchPos(p.i):colPos(p.i,0)}
function pressTick(){const p=S&&S.press;if(!p||p.cancel||p.peek)return;if(S.t-p.t0>.22){p.peek=true;hap('peek');sfx.click()}}
cv.addEventListener('pointermove',e=>{
  const p=S&&S.press;if(!p)return;
  const r=cv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,dx=x-p.x,dy=y-p.y,d=Math.hypot(dx,dy),lim=LY.ru*.7;
  const f=d>0?Math.min(1,lim/d)*.45:0;p.ox=dx*f;p.oy=dy*f;
  if(!p.cancel&&d>LY.ru*1.6){p.cancel=true;hap('cancel');sfx.deny()}
  else if(p.cancel&&d<LY.ru*1.15){p.cancel=false;p.t0=S.t-.3;p.peek=true;hap('back');sfx.click()}
});""")

sub("""  if(Math.hypot(x-p.x,y-p.y)>LY.ru*1.6)return;
  if(p.kind==='b'){if(S.bench[p.i]&&S.bench[p.i].id===p.id)launchBench(p.i)}
  else if(S.cols[p.i][0]&&S.cols[p.i][0].id===p.id)launchCol(p.i);""",
"""  if(p.cancel||Math.hypot(x-p.x,y-p.y)>LY.ru*1.6){hap('back');const sh=p.kind==='b'?S.bench[p.i]:S.cols[p.i][0];if(sh)sh.sq=1;return}
  if(p.peek){hap('go');S.quiet=true}
  if(p.kind==='b'){if(S.bench[p.i]&&S.bench[p.i].id===p.id)launchBench(p.i)}
  else if(S.cols[p.i][0]&&S.cols[p.i][0].id===p.id)launchCol(p.i);""")

sub("  ac();if(!S||S.state!=='play'||S.paused)return;\n  const r=cv.getBoundingClientRect()",
    "  ac();if(!S||S.state!=='play'||S.paused)return;\n  try{cv.setPointerCapture(e.pointerId)}catch(_){}\n  const r=cv.getBoundingClientRect()")

sub("function update(dt){\n  if(!S)return;\n  S.t+=dt;","function update(dt){\n  if(!S)return;\n  S.t+=dt;pressTick();")

# what the finger means right now: ring colour + a short word above the shooter
sub("  if(S.press&&S.t-S.press.t0>.22){",
"""  if(S.press){const p=S.press,[px,py]=pressPos(p),k=Math.min(1,(S.t-p.t0)/.16),cx=px+p.ox*k,cy=py+p.oy*k,R=LY.ru*1.25;
    ctx.save();ctx.lineWidth=4;
    if(p.cancel){ctx.strokeStyle='#ff5d73';ctx.setLineDash([7,6])}
    else if(p.peek){ctx.strokeStyle='rgba(255,255,255,'+(.7+.3*Math.sin(S.t*9))+')'}
    else{ctx.strokeStyle='rgba(255,255,255,.55)';ctx.beginPath();ctx.arc(cx,cy,R,-Math.PI/2,-Math.PI/2+Math.PI*2*Math.min(1,(S.t-p.t0)/.22));ctx.stroke();ctx.restore()}
    if(p.cancel||p.peek){ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.stroke();ctx.setLineDash([]);
      const idle=!p.cells.length,txt=p.cancel?'отпусти - отмена':idle?(p.kind==='b'?'рано, уведи палец':'отпусти - на скамейку'):'отпусти - запуск';ctx.font='900 13px '+FB;const w=ctx.measureText(txt).width+18;
      ctx.fillStyle=p.cancel?'#ff5d73':idle?'#ffae1a':'#2fcb82';const lx=Math.max(w/2+6,Math.min(CW-w/2-6,cx));rr(ctx,lx-w/2,cy-R-30,w,22,11);ctx.fill();ctx.fillStyle='#fff';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(txt,lx,cy-R-19);ctx.restore()}}
  if(S.press&&S.press.peek&&!S.press.cancel){""")

sub("\n    if(!S.press.cells.length){ctx.font='900 15px '+FB;ctx.fillStyle='#fff';ctx.textAlign='center';ctx.fillText('сейчас ему некого сбить',CW/2,LY.oy-8)}ctx.restore()}","ctx.restore()}")
sub("const a=.55+.45*Math.sin(S.t*10);ctx.save();ctx.lineWidth=Math.max(2,LY.cs*.14);ctx.strokeStyle='rgba(255,255,255,'+a+')';\n    for(const c of S.press.cells){const[x0,y0]=cellCenter(c),h=LY.cs*.46;rr(ctx,x0-h,y0-h,h*2,h*2,h*.5);ctx.stroke()}",
"const a=.8+.2*Math.sin(S.t*10);ctx.save();{const[ax,ay]=cellCenter(0),[bx,by]=cellCenter(S.W*S.H-1),m=LY.cs*.55,h=LY.cs*.5;ctx.beginPath();ctx.rect(ax-m,ay-m,bx-ax+2*m,by-ay+2*m);for(const c of S.press.cells){const[x0,y0]=cellCenter(c);ctx.rect(x0-h,y0-h,h*2,h*2)}ctx.fillStyle='rgba(20,14,50,.5)';ctx.fill('evenodd')}\n    ctx.lineWidth=Math.max(2.5,LY.cs*.15);ctx.strokeStyle='rgba(255,255,255,'+a+')';\n    for(const c of S.press.cells){const[x0,y0]=cellCenter(c),h=LY.cs*.48;rr(ctx,x0-h,y0-h,h*2,h*2,h*.45);ctx.stroke()}")
sub("sfx.launch();vib(8);","sfx.launch();if(!S.quiet)vib(8);S.quiet=false;")
io.open(P,'w',encoding='utf-8').write(s)
w=io.open('sw.js',encoding='utf-8').read()
w=re.sub(r"smena-v\d+","smena-v"+str(int(time.time())),w,1)
io.open('sw.js','w',encoding='utf-8').write(w)
print('OK press feedback',len(s))
