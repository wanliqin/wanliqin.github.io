from PIL import Image, ImageOps
from pathlib import Path

TMP = Path('/Users/liqinwan/Desktop/tmp')
OUT = Path('/Users/liqinwan/Documents/Codex/2026-07-21/hatch-pet-users-liqinwan-codex-skills-2/work/xuetuan-rebuild/final')
OUT.mkdir(parents=True, exist_ok=True)
W,H=192,208
KEY=(243,105,118)

def load_strip(n):
    p=TMP/f'奶油白长毛猫桌宠生成 ({n}).png'
    return Image.open(p).convert('RGBA')

def cut(strip, count):
    sw=strip.width//count
    out=[]
    for i in range(count):
        im=strip.crop((i*sw,0,(i+1)*sw,strip.height))
        px=im.load()
        for y in range(im.height):
            for x in range(im.width):
                r,g,b,a=px[x,y]
                d=((r-KEY[0])**2+(g-KEY[1])**2+(b-KEY[2])**2)**0.5
                if d<105: px[x,y]=(0,0,0,0)
                elif d<145: px[x,y]=(r,g,b,max(0,int((d-105)*255/40)))
        out.append(im)
    return out

def normalize(frames):
    boxes=[]
    for im in frames:
        a=im.getchannel('A'); box=a.getbbox(); boxes.append(box)
    maxh=max(b[3]-b[1] for b in boxes)
    scale=min(1.0,190/maxh)
    result=[]
    for im,b in zip(frames,boxes):
        crop=im.crop(b)
        crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.LANCZOS)
        cell=Image.new('RGBA',(W,H),(0,0,0,0))
        x=(W-crop.width)//2; y=H-8-crop.height
        cell.alpha_composite(crop,(x,y))
        cp=cell.load()
        for yy in range(H):
            for xx in range(W):
                if cp[xx,yy][3] == 0: cp[xx,yy]=(0,0,0,0)
        result.append(cell)
    return result

def row(n, count): return normalize(cut(load_strip(n),count))

rows={
 0: row(8,8)[:6], 1: row(2,8), 2: [ImageOps.mirror(x) for x in row(2,8)],
 3: row(3,4), 4: row(4,5), 5: row(10,8), 6: row(5,8)[:6],
 7: row(17,8)[:6], 8: row(20,8)[:6], 9: row(12,8), 10: row(13,8),
}

atlas=Image.new('RGBA',(W*8,H*11),(0,0,0,0))
for r,frames in rows.items():
    for c,im in enumerate(frames): atlas.alpha_composite(im,(c*W,r*H))
atlas.save(OUT/'spritesheet-extended.png')
atlas.save(OUT/'spritesheet-extended.webp',lossless=True)
print(OUT/'spritesheet-extended.png')
