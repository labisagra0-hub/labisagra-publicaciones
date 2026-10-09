import sys, asyncio, os
from playwright.async_api import async_playwright
async def main(code, out, w=1200):
    svg=open(f'flag-icons/flags/4x3/{code}.svg').read()
    html=f"<html><body style='margin:0;background:#000'><img src='data:image/svg+xml;utf8,{svg.replace(chr(35),'%23')}' style='width:{w}px;height:{int(w*0.75)}px;display:block'></body></html>"
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':int(w*0.75)})
        await pg.set_content(html); await pg.screenshot(path=out); await b.close()
os.makedirs('flags',exist_ok=True); asyncio.run(main(sys.argv[1], 'flags/'+sys.argv[1]+'.png'))
