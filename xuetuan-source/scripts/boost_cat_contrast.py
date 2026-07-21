from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path

src = Path('work/xuetuan-rebuild/final/spritesheet-final.png')
dst = Path('outputs/xuetuan-spritesheet-v2-contrast.png')
im = Image.open(src).convert('RGBA')
W,H = 192,208
atlas = Image.new('RGBA', im.size, (0,0,0,0))

for row in range(11):
    for col in range(8):
        cell = im.crop((col*W,row*H,(col+1)*W,(row+1)*H))
        alpha = cell.getchannel('A')
        # Preserve the transparent background and gently restore contrast lost in cleanup.
        rgb = cell.convert('RGB')
        rgb = ImageEnhance.Contrast(rgb).enhance(1.28)
        rgb = ImageEnhance.Color(rgb).enhance(1.18)
        rgb = ImageEnhance.Brightness(rgb).enhance(1.03)
        cell = Image.merge('RGBA', (*rgb.split(), alpha))
        # A restrained warm-gray silhouette edge improves readability on white backgrounds.
        expanded = alpha.filter(ImageFilter.MaxFilter(5))
        outline = Image.new('RGBA', cell.size, (82,70,68,0))
        outline.putalpha(expanded.point(lambda a: min(155, int(a*0.62))))
        outline.putalpha(Image.eval(outline.getchannel('A'), lambda a: a))
        outline.alpha_composite(cell)
        # Restore the original sprite over the outline, keeping fur edges natural.
        outline.alpha_composite(cell)
        atlas.alpha_composite(outline, (col*W,row*H))

dst.parent.mkdir(parents=True, exist_ok=True)
atlas.save(dst)
print(dst)
