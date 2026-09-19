from PIL import Image, ImageDraw, ImageFilter
PAL={'o':'#ff9433','w':'#f2ede2','d':'#4a5580','k':'#ff7eb9'}
cat=[".o........o.",".oo......oo.",".ooo....ooo.",".oooooooooo.","oooooooooooo","oowdoooowdoo","ooddooooddoo","oooookkooooo","oooodoodoooo",".oooooooooo.","..oooooooo.."]
H=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def icon(S, maskable=False):
    im=Image.new('RGB',(S,S)); d=ImageDraw.Draw(im)
    top,mid,bot=H('#7ccaff'),H('#b3a3ff'),H('#ffb6d9')
    for y in range(S):
        t=y/S; c=lerp(top,mid,t/0.55) if t<0.55 else lerp(mid,bot,(t-0.55)/0.45); d.line((0,y,S,y),fill=c)
    pad=S*(0.15 if maskable else 0.08)
    # shadow
    sh=Image.new('L',(S,S),0); ImageDraw.Draw(sh).rounded_rectangle((pad,pad+S*0.03,S-pad,S-pad+S*0.03),radius=S*0.16,fill=110)
    sh=sh.filter(ImageFilter.GaussianBlur(S*0.03)); im.paste(Image.new('RGB',(S,S),(70,40,150)),(0,0),sh)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((pad,pad,S-pad,S-pad),radius=S*0.16,fill=(255,255,255))
    bw=S*0.07; b0=pad+S*0.04
    d.rounded_rectangle((b0,b0,S-b0,S-b0),radius=S*0.12,outline=H('#353a70'),width=int(bw))
    for k in range(7):
        xx=b0+bw*1.3+k*(S-2*b0-bw*2.6)/6
        for yy in (b0+bw/2,S-b0-bw/2):
            d.polygon([(xx-S*0.012,yy-S*0.02),(xx+S*0.012,yy),(xx-S*0.012,yy+S*0.02)],fill=(90,96,150))
    t0=b0+bw+S*0.015
    d.rounded_rectangle((t0,t0,S-t0,S-t0),radius=S*0.06,fill=H('#262a55'))
    w=len(cat[0]);h=len(cat);cell=(S-2*t0-S*0.05)/w;ox=S/2-cell*w/2;oy=S/2-cell*h/2
    for yy,row in enumerate(cat):
        for xx,ch in enumerate(row):
            if ch=='.':continue
            c=H(PAL[ch]);g=cell*0.05;X=ox+xx*cell;Y=oy+yy*cell;dk=tuple(int(v*.68) for v in c);hi=lerp(c,(255,255,255),.4)
            d.rounded_rectangle((X+g,Y+g+cell*.05,X+cell-g,Y+cell-g),radius=cell*.26,fill=dk)
            d.rounded_rectangle((X+g,Y+g,X+cell-g,Y+cell-g-cell*.12),radius=cell*.26,fill=c)
            d.rounded_rectangle((X+cell*.2,Y+cell*.15,X+cell*.55,Y+cell*.27),radius=cell*.06,fill=hi)
    R=S*0.1;cx=S-b0-R*0.95;cy=S-b0-bw*0.5
    d.ellipse((cx-R,cy-R,cx+R,cy+R),fill=H('#4f8bff'),outline=H('#2a53ad'),width=max(2,int(R*.1)))
    d.ellipse((cx-R*.62,cy-R*.72,cx-R*.18,cy-R*.46),fill=(170,200,255))
    for s in(-1,1):
        d.ellipse((cx+s*R*.3-R*.2,cy-R*.56,cx+s*R*.3+R*.2,cy-R*.08),fill='white')
        d.ellipse((cx+s*R*.3-R*.1,cy-R*.42,cx+s*R*.3+R*.1,cy-R*.2),fill=H('#221d3d'))
    return im
for S,n,m in [(512,'icon-512.png',0),(192,'icon-192.png',0),(180,'apple-touch-icon.png',0),(512,'icon-maskable-512.png',1),(32,'favicon-32.png',0)]:
    im=icon(1024,m).resize((S,S),Image.LANCZOS)
    im.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save('icons/'+n,optimize=True)
