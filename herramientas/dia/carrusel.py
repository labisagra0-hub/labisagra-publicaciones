import json, sys, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np, hero
W,H=1080,1350; M=84
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
def header(d,im,fecha,n,total):
    mark(d,M+42,M+10,1.0); d.text((M+110,M+10),"LA BISAGRA",font=f(BB,40),fill=INK,anchor='lm')
    d.text((W-M,M+10),f"EL DÍA EN EL MUNDO · {fecha}",font=f(WS,24),fill=MU,anchor='rm')
    d.line([(M,M+56),(W-M,M+56)],fill=DIM,width=2)
    d.text((W-M,H-M+8),f"{n}/{total}",font=f(BB,30),fill=MU,anchor='rm')
def collage_bg(items):
    codes=[it['pais'] for it in items if it.get('pais')]
    if not codes: return Image.new('RGB',(W,H),BG)
    im=Image.new('RGB',(W,H),BG); n=len(codes); hh=H//n
    for i,c in enumerate(codes):
        tile=hero.flag_bg(c,(W,hh+2),blur=70,bright=0.22); im.paste(tile,(0,i*hh))
    ov=Image.new('L',(W,H),110); im.paste(Image.new('RGB',(W,H),BG),(0,0),ov)
    return im
def cover(spec,items,out):
    im=collage_bg(items); d=ImageDraw.Draw(im)
    header(d,im,spec['fecha'],1,len(items)+2)
    y=M+120; d.text((M,y),"EL DÍA EN",font=f(BB,150),fill=INK); y+=140
    d.text((M,y),"EL MUNDO",font=f(BB,150),fill=BR); y+=190
    d.text((M,y),f"{len(items)} NOTICIAS QUE IMPORTAN · {spec['fecha']}",font=f(WS,28),fill=MU); y+=70
    for i,it in enumerate(items,1):
        d.text((M,y),f"0{i}",font=f(BB,40),fill=BR)
        y=para(d,M+70,y+2,it['resumen'],f(WR,32),INK,W-2*M-70,40)+26
    d.text((M,H-M+8),"Deslizá →",font=f(WS,26),fill=INK,anchor='lm')
    grain(im).save(out,quality=94)
def slide(spec,it,n,total,out):
    code=it.get('pais'); iso3=it.get('iso3')
    im=hero.flag_bg(code,(W,H),blur=90,bright=0.22) if code else Image.new('RGB',(W,H),BG)
    if code and iso3:
        fm=hero.flag_map(code,iso3,(760,760))
        if fm:
            a=fm.split()[3].point(lambda v:int(v*0.5)); fm.putalpha(a); im.paste(fm,(W-700,380),fm)
    ov=Image.new('L',(W,H),0); od=ImageDraw.Draw(ov)
    for i in range(H):
        t=i/H; a=int(90+110*(1-abs(t-0.6)*1.8)); od.line([(0,i),(W,i)],fill=max(40,min(200,a)))
    im.paste(Image.new('RGB',(W,H),BG),(0,0),ov)
    d=ImageDraw.Draw(im); header(d,im,spec['fecha'],n,total)
    y=M+100
    if code:
        ch=hero.flag_chip(code,96); im.paste(ch,(M,y-14)); d.rectangle([M,y-14,M+95,y+57],outline=(0,0,0),width=2); d.text((M+120,y+6),it['tag'].upper(),font=f(WS,28),fill=BR)
    else: d.text((M,y+6),it['tag'].upper(),font=f(WS,28),fill=BR)
    y+=90
    if it.get('cifra'):
        d.text((M-6,y),it['cifra'],font=f(BB,240),fill=BR); y+=256
        d.text((M,y),it.get('cifra_sub','').upper(),font=f(WS,30),fill=INK); y+=62
    for ln in it['titulo']:
        col=BR if ln.startswith('*') else INK; d.text((M,y),ln.lstrip('*'),font=f(BB,84),fill=col); y+=82
    y+=24
    for t in it['datos'][:2]:
        d.rectangle([M,y+10,M+10,y+38],fill=BR); y=para(d,M+34,y,t,f(WR,31),INK,W-2*M-34,40)+16
    y+=10; d.line([(M,y),(W-M,y)],fill=DIM,width=2); y+=22
    d.text((M,y),"LA BISAGRA",font=f(BB,30),fill=BR); y+=38
    y=para(d,M,y,it['bisagra'],f(WR,28),MU,W-2*M,36)
    if y>H-M-40: print(f"AVISO: lámina {n} larga")
    d.text((M,H-M+8),f"Fuente: {it['fuente']}",font=f(WR,22),fill=MU,anchor='lm')
    grain(im).save(out,quality=94)
def last(spec,items,total,out):
    im=collage_bg(items); d=ImageDraw.Draw(im); header(d,im,spec['fecha'],total,total)
    y=M+160; d.text((M,y),"MAÑANA",font=f(BB,130),fill=INK); y+=120; d.text((M,y),"HAY MÁS",font=f(BB,130),fill=BR); y+=190
    y=para(d,M,y,spec.get('cierre',"Cada día, lo que pasa en el mundo con su dato y su historia. Guardá este carrusel y seguinos para el de mañana."),f(WR,34),INK,W-2*M,46)+40
    d.rectangle([M,y,M+10,y+30],fill=BR); y=para(d,M+30,y,spec.get('cta',"Seguinos: cada día, lo que pasa en el mundo con su dato y su historia."),f(WS,30),INK,W-2*M-30,40)+30
    d.text((M,H-M+8),"@labisagrahistoria",font=f(WS,26),fill=INK,anchor='lm')
    grain(im).save(out,quality=94)
if __name__=='__main__':
    spec=json.load(open(sys.argv[1])); pre=sys.argv[2]; items=spec['items']; total=len(items)+2
    cover(spec,items,f"{pre}-1.jpg")
    for i,it in enumerate(items,2): slide(spec,it,i,total,f"{pre}-{i}.jpg")
    last(spec,items,total,f"{pre}-{total}.jpg"); print("ok")
