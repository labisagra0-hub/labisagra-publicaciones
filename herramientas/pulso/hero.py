import json, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
GEO='world.geo.json/countries.geo.json'
def country_poly(iso3):
    for f in json.load(open(GEO))['features']:
        if f['id']==iso3:
            g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
            return [p[0] for p in polys]
    return None
def silhouette(iso3, size, fill, pad=0.06):
    polys=country_poly(iso3)
    if not polys: return None
    def area(r):
        return abs(sum(r[i][0]*r[(i+1)%len(r)][1]-r[(i+1)%len(r)][0]*r[i][1] for i in range(len(r))))/2
    polys=sorted(polys,key=area,reverse=True)
    big=polys[0]; A=area(big); polys=[p for p in polys if area(p)>A*0.004]
    xs=[x for p in polys for x,y in p]; ys=[y for p in polys for x,y in p]
    lat0=(min(ys)+max(ys))/2; k=math.cos(math.radians(lat0))
    xs=[x*k for x in xs]
    minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
    W,H=size; s=min(W*(1-2*pad)/(maxx-minx), H*(1-2*pad)/(maxy-miny))
    ox=(W-(maxx-minx)*s)/2; oy=(H-(maxy-miny)*s)/2
    im=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(im)
    for p in polys:
        pts=[(ox+(x*k-minx)*s, oy+(maxy-y)*s) for x,y in p]
        d.polygon(pts,fill=fill)
    return im
def flag_bg(code, size, blur=60, bright=0.30):
    fl=Image.open(f'flags/{code}.png').convert('RGB')
    W,H=size; r=max(W/fl.width,H/fl.height); fl=fl.resize((int(fl.width*r)+1,int(fl.height*r)+1))
    fl=fl.crop(((fl.width-W)//2,(fl.height-H)//2,(fl.width-W)//2+W,(fl.height-H)//2+H))
    fl=fl.filter(ImageFilter.GaussianBlur(blur)); fl=ImageEnhance.Brightness(fl).enhance(bright)
    return fl
def flag_chip(code, w):
    fl=Image.open(f'flags/{code}.png').convert('RGB')
    return fl.resize((w,int(w*0.75)))
def flag_map(code, iso3, size):
    s=silhouette(iso3,size,(255,255,255,255),pad=0.02)
    if s is None: return None
    fl=Image.open(f'flags/{code}.png').convert('RGB')
    W,H=size; r=max(W/fl.width,H/fl.height); fl=fl.resize((int(fl.width*r)+1,int(fl.height*r)+1))
    fl=fl.crop(((fl.width-W)//2,(fl.height-H)//2,(fl.width-W)//2+W,(fl.height-H)//2+H))
    out=Image.new('RGBA',size,(0,0,0,0)); out.paste(fl,(0,0),s.split()[3]); return out
