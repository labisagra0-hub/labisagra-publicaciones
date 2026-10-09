import json, sys, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np, hero
W,H=1080,1920; M=84
F='/mnt/skills/examples/canvas-design/canvas-fonts/'
BB=F+'BigShoulders-Bold.ttf'; WS=F+'WorkSans-Bold.ttf'; WR=F+'WorkSans-Regular.ttf'
BG=(17,18,20); INK=(242,241,236); BR=(201,162,78); MU=(170,167,158); DIM=(70,70,68)
def f(p,s): return ImageFont.truetype(p,s)
def mark(d,x,y,k):
    ang=math.atan2(-38,40); w=int(11*k); ex,ey=x+55*k*math.cos(ang),y+55*k*math.sin(ang)
    d.line([(x-42*k,y),(x,y)],fill=INK,width=w); d.line([(x,y),(ex,ey)],fill=INK,width=w)
    r=w/2; d.ellipse([x-42*k-r,y-r,x-42*k+r,y+r],fill=INK); d.ellipse([ex-r,ey-r,ex+r,ey+r],fill=INK)
    d.ellipse([x-13.5*k,y-13.5*k,x+13.5*k,y+13.5*k],fill=BG); d.ellipse([x-8.5*k,y-8.5*k,x+8.5*k,y+8.5*k],fill=BR)
def wrap(d,text,font,maxw):
    out=[]; line=''
    for w in text.split(' '):
        t=(line+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: line=t
        else: out.append(line); line=w
    out.append(line); return out
def para(d,x,y,text,font,fill,maxw,lh):
    for ln in wrap(d,text,font,maxw): d.text((x,y),ln,font=font,fill=fill); y+=lh
    return y
def grain(im,amt=4):
    a=np.asarray(im).astype(float); n=np.random.default_rng(3).normal(0,amt,(H,W,1)); return Image.fromarray((a+n).clip(0,255).astype('uint8'))
def render(spec,out):
    ult=spec.get('modo','ahora')=='ultimo'; label="ÚLTIMO MOMENTO" if ult else "AHORA EN EL MUNDO"
    rib=BR if ult else (48,49,52); ribtxt=BG if ult else INK
    code=spec.get('pais'); iso3=spec.get('iso3')
    im=hero.flag_bg(code,(W,H),blur=90,bright=0.22) if code else Image.new('RGB',(W,H),BG)
    if code and iso3:
        fm=hero.flag_map(code,iso3,(980,980))
        if fm:
            a=fm.split()[3].point(lambda v:int(v*0.55)); fm.putalpha(a)
            im.paste(fm,(W-900,560),fm)
    ov=Image.new('L',(W,H),0); od=ImageDraw.Draw(ov)
    for i in range(H):
        t=i/H; a=int(90+110*(1-abs(t-0.62)*1.8)); od.line([(0,i),(W,i)],fill=max(40,min(200,a)))
    im.paste(Image.new('RGB',(W,H),BG),(0,0),ov)
    d=ImageDraw.Draw(im)
    y0=260; mark(d,M+42,y0,1.0); d.text((M+110,y0),"LA BISAGRA",font=f(BB,44),fill=INK,anchor='lm')
    if code:
        ch=hero.flag_chip(code,132); im.paste(ch,(W-M-132,y0-50)); d.rectangle([W-M-132,y0-50,W-M-1,y0+49],outline=(0,0,0),width=2)
    y=y0+66; d.rectangle([M,y,M+440,y+60],fill=rib); d.text((M+22,y+30),label,font=f(BB,38),fill=ribtxt,anchor='lm')
    y+=100; d.text((M,y),spec['tag'].upper(),font=f(WS,30),fill=BR); y+=50
    if spec.get('cifra'):
        cf=f(BB,300); d.text((M-6,y),spec['cifra'],font=cf,fill=BR); y+=318
        d.text((M,y),spec.get('cifra_sub','').upper(),font=f(WS,34),fill=INK); y+=70
    for ln in spec['titulo']:
        col=BR if ln.startswith('*') else INK; d.text((M,y),ln.lstrip('*'),font=f(BB,100),fill=col); y+=98
    y+=36
    for i,t in enumerate(spec['datos'][:3],1):
        d.rectangle([M,y+12,M+10,y+42],fill=BR)
        y=para(d,M+34,y,t,f(WR,35),INK,W-2*M-34,46)+20
    y+=16; d.line([(M,y),(W-M,y)],fill=DIM,width=2); y+=28
    d.text((M,y),"LA BISAGRA",font=f(BB,36),fill=BR); y+=46
    y=para(d,M,y,spec['bisagra'],f(WR,32),MU,W-2*M,42)
    y+=36
    if y+90>H-170: print("AVISO: contenido largo, acortar datos o bisagra")
    d.text((M,y),f"Fuente: {spec['fuente']}",font=f(WR,25),fill=MU,anchor='lm')
    d.text((M,y+46),"Más en @labisagrahistoria",font=f(WS,30),fill=INK,anchor='lm')
    grain(im).save(out,quality=94)
if __name__=='__main__':
    render(json.load(open(sys.argv[1])),sys.argv[2])
