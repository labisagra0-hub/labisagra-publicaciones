import json, sys, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W,H=1080,1350; M=84
F='/mnt/skills/examples/canvas-design/canvas-fonts/'
BB=F+'BigShoulders-Bold.ttf'; WS=F+'WorkSans-Bold.ttf'; WR=F+'WorkSans-Regular.ttf'
BG=(17,18,20); INK=(242,241,236); BR=(201,162,78); MU=(142,139,130); DIM=(52,52,50)
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
def grain(im,amt=5):
    a=np.asarray(im).astype(float); n=np.random.default_rng(3).normal(0,amt,(H,W,1)); return Image.fromarray((a+n).clip(0,255).astype('uint8'))
def fondo(path):
    im=Image.open(path).convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1))
    x=(im.width-W)//2; y=(im.height-H)//3; im=im.crop((x,y,x+W,y+H))
    a=np.asarray(im).astype(float); g=a@np.array([0.299,0.587,0.114]); a=a*0.35+g[...,None]*0.65
    yy=np.linspace(0,1,H)[:,None,None]; k=0.62-0.5*np.clip((yy-0.25)/0.6,0,1); a=a*(1-k)+np.array(BG,float)*k
    return Image.fromarray(a.clip(0,255).astype('uint8'))
def render(spec,out):
    im=fondo(spec['foto']) if spec.get('foto') else Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    k=2.6; px,py=W-120,H-250; ang=math.atan2(-38,40)
    d.line([(px-42*k,py),(px,py)],fill=(24,25,27),width=int(11*k)); d.line([(px,py),(px+55*k*math.cos(ang),py+55*k*math.sin(ang))],fill=(24,25,27),width=int(11*k))
    mark(d,M+42,M+10,1.0); d.text((M+110,M+10),"LA BISAGRA",font=f(BB,40),fill=INK,anchor='lm')
    d.text((W-M,M+10),f"HOY EN EL MUNDO · {spec['fecha']}",font=f(WS,24),fill=MU,anchor='rm')
    d.line([(M,M+56),(W-M,M+56)],fill=DIM,width=2)
    y=M+100; d.rectangle([M,y+6,M+10,y+30],fill=BR); d.text((M+26,y),spec['tag'].upper(),font=f(WS,28),fill=BR)
    y+=60
    for ln in spec['titulo']:
        col=BR if ln.startswith('*') else INK; d.text((M,y),ln.lstrip('*'),font=f(BB,96),fill=col); y+=96
    y+=24
    if spec.get('barras'):
        mx=max(b['pct'] for b in spec['barras']); bw=W-2*M-250-150
        for i,b in enumerate(spec['barras']):
            col=BR if i==0 else (120,118,110)
            d.text((M,y+2),b['label'],font=f(WS,30),fill=INK)
            d.rectangle([M+250,y+8,M+250+int(bw*b['pct']/mx),y+36],fill=col)
            d.text((M+250+int(bw*b['pct']/mx)+16,y+2),b['valor'],font=f(BB,40),fill=INK)
            y+=58
        y+=20
    for i,t in enumerate(spec['datos'],1):
        d.text((M,y-2),f"0{i}",font=f(BB,40),fill=BR)
        y=para(d,M+70,y,t,f(WR,31),INK,W-2*M-70,40)+20
    y+=10; d.line([(M,y),(W-M,y)],fill=DIM,width=2); y+=28
    d.text((M,y),"LA BISAGRA",font=f(BB,34),fill=BR); y+=44
    y=para(d,M,y,spec['bisagra'],f(WR,31),MU,W-2*M,40)
    d.text((M,H-M+8),f"Fuente: {spec['fuente']}",font=f(WR,22),fill=MU,anchor='lm')
    d.text((W-M,H-M+8),"@labisagrahistoria",font=f(WS,24),fill=INK,anchor='rm')
    grain(im).save(out,quality=94)
if __name__=='__main__':
    render(json.load(open(sys.argv[1])),sys.argv[2])
