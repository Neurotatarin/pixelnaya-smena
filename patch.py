import io,re,time,sys
P='index.html'
s=io.open(P,encoding='utf-8').read()
NEW='''<div class="steps">
      <div class="step"><div class="sn">1</div><div><b>Цель.</b> Сбей все кубики картины.</div><img data-help="help_1" alt="" hidden></div>
      <div class="step"><div class="sn">2</div><div><b>Стрелки.</b> Цвет стрелка = цвет кубиков, которые он бьет. Число = патроны. <span class="ball" style="background:#3f7cff">20</span> собьет до 20 синих.</div><img data-help="help_2" alt="" hidden></div>
      <div class="step"><div class="sn">3</div><div><b>Тапни стрелка.</b> Он объедет картину и собьет только <b>крайние</b> кубики своего цвета. Внутренние темнее <span class="chip" style="background:#ffd23f"></span><span class="chip dim" style="background:#ffd23f"></span> до них пока не достать.</div><img data-help="help_3" alt="" hidden></div>
      <div class="step"><div class="sn">4</div><div><b>Скамейка.</b> Остались патроны - стрелок сядет на скамейку. Тапни его, когда его цвет окажется снаружи. <b>Скамейка забилась - проигрыш.</b> Один раз за смену выручит аварийное место.</div><img data-help="help_4" alt="" hidden></div>
      <div class="step"><div class="sn">5</div><div><b>Не уверен?</b> Зажми палец на стрелке: подсветятся кубики, которые он собьет. Отпустил - поехал. Увел палец - отмена.</div></div>
      <div class="step"><div class="sn">6</div><div><b>Лихорадка.</b> Сбивай кубики без пауз, и шкала наполнится. 6 секунд все быстрее, а каждый кубик дает монеты.</div></div>
      <div class="step"><div class="sn">7</div><div><b>Награды.</b> Выполнил задание смены: +50. Собрал коллекцию картин: +200. Прошел смену быстрее всех: +100.</div></div>
      <div class="step"><div class="sn">!</div><div><b>Главное правило:</b> пускай стрелка того цвета, который сейчас снаружи.</div></div>
    </div>
    <div class="row"><button class="btn primary" id="helpOk">'''
s2,n=re.subn(r'<div class="steps">.*?</div>\n    <div class="row"><button class="btn primary" id="helpOk">',lambda m:NEW,s,count=1,flags=re.S)
if n!=1:print('MISS help');sys.exit(1)
s=s2
old="else if(n===3)once('t3',"
if s.count(old)!=1:print('MISS t3');sys.exit(1)
s=s.replace(old,"else if(n===4)once('t4','Не уверен в ходе? Зажми палец на стрелке и увидишь, какие кубики он собьет',5500);\n    else if(n===3)once('t3',",1)
io.open(P,'w',encoding='utf-8').write(s)
w=io.open('sw.js',encoding='utf-8').read()
w=re.sub(r"smena-v\d+","smena-v"+str(int(time.time())),w,1)
io.open('sw.js','w',encoding='utf-8').write(w)
print('OK help v10',len(s))
