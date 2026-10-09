"""Adapta una imagen (por ejemplo 4:5) a historia de Instagram 9:16 (1080x1920).

Uso: python3 historia916.py entrada.jpg salida.jpg
La imagen va centrada y entera; el fondo es la misma imagen agrandada, difuminada y oscurecida.
Si la entrada ya es 9:16, solo la reescala.
"""
import sys
from PIL import Image, ImageFilter, ImageEnhance

W, H = 1080, 1920


def adaptar(src, dst):
    im = Image.open(src).convert("RGB")
    if abs(im.width / im.height - W / H) < 0.01:
        im.resize((W, H), Image.LANCZOS).save(dst, quality=92)
        return
    s = max(W / im.width, H / im.height)
    bg = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x, y = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(0.35)
    k = min(W / im.width, H / im.height)
    fg = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    bg.save(dst, quality=92)


if __name__ == "__main__":
    adaptar(sys.argv[1], sys.argv[2])
    print("ok")
