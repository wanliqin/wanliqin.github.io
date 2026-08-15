from PIL import Image, ImageDraw, ImageEnhance
from pathlib import Path

sources = [
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-09e4e53c-d0f8-4ab4-8b63-9c18d925977b.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-37b8ab0d-6be2-451a-bb30-4f5d81564f4e.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-e62ac3b7-da2b-4f91-af9f-3c02471bf7eb.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-5ea77b18-f425-43f2-a7a5-64560aab2fa6.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-5934025c-c30d-4a76-8709-63dbe025eda0.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-313f4d91-bc0d-4c40-8b32-90077eea293e.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-616b71a7-0869-40d3-b64c-0076fb826fb4.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-759d8c3d-59cd-4ea6-9f99-3b9f4a4e8b1e.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-a9b15715-cbc6-45c8-8499-95f0e2fa0707.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-02ad702a-c10b-4506-a387-51aa4fd0516e.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-ae8e0e5a-47cb-49e2-970b-df55ef99af06.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-dad7b9f6-4cac-48dd-abdf-3c6b01b37073.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-76de5555-d57c-4e3f-a368-777404de0f64.jpg'),
    Path('/var/folders/t3/ldps6wf90qx_q00brzk4sjg40000gn/T/codex-clipboard-9d023713-3948-4465-aa7e-2618f7d433da.jpg'),
]
run = Path('/Users/liqinwan/Documents/Codex/pets/xuetuan')
out = run / 'final' / 'spritesheet-extended.png'
out.parent.mkdir(parents=True, exist_ok=True)
def make_base(row):
    im = Image.open(sources[row % len(sources)]).convert('RGBA')
    im.thumbnail((176, 194), Image.Resampling.LANCZOS)
    base = Image.new('RGBA', (192, 208), (0, 0, 0, 0))
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).ellipse((2, 0, im.width-2, im.height-2), fill=255)
    base.alpha_composite(Image.composite(im, Image.new('RGBA', im.size), mask), ((192-im.width)//2, (208-im.height)//2+5))
    return base

def pose(i, row):
    base = make_base(row)
    p = base.copy()
    d = ImageDraw.Draw(p)
    if row == 1:
        p = ImageEnhance.Contrast(p).enhance(1.08)
        d = ImageDraw.Draw(p)
        d.rounded_rectangle((35, 170, 157, 193), radius=5, fill=(48, 54, 68, 255), outline=(125, 170, 210, 255), width=2)
        d.line((52, 180, 140, 180), fill=(160, 205, 225, 255), width=2)
        d.line((70, 186, 125, 186), fill=(160, 205, 225, 255), width=2)
    elif row == 4:
        p = Image.new('RGBA', p.size, (0,0,0,0)); p.alpha_composite(base, (0, -8+(i%3)*4))
    elif row == 5:
        p = ImageEnhance.Brightness(p).enhance(.86)
    elif row == 6:
        p = Image.new('RGBA', p.size, (0,0,0,0)); p.alpha_composite(base, (3 if i%2 else -3, 0))
        d = ImageDraw.Draw(p)
        d.ellipse((157, 84, 170, 97), fill=(244, 190, 88, 255))
    elif row == 7:
        p = ImageEnhance.Color(p).enhance(1.12)
        d = ImageDraw.Draw(p)
        d.rounded_rectangle((25, 26, 167, 51), radius=4, fill=(42, 74, 102, 255), outline=(135, 206, 225, 255), width=2)
        d.rectangle((43, 33, 149, 44), fill=(109, 177, 194, 255))
    elif row == 8:
        q = base.resize((196+(i%3)*2, 212+(i%3)*2), Image.Resampling.LANCZOS)
        p = Image.new('RGBA', p.size, (0,0,0,0)); p.alpha_composite(q, ((192-q.width)//2, (208-q.height)//2))
        d = ImageDraw.Draw(p)
        d.polygon([(18, 158), (84, 148), (97, 184), (31, 194)], fill=(238, 231, 205, 255), outline=(120, 105, 86, 255))
        d.line((31, 169, 79, 161), fill=(100, 145, 176, 255), width=2)
    elif row == 10:
        p = Image.new('RGBA', p.size, (0,0,0,0)); p.alpha_composite(base, ((i%4)-2, 0))
    return p

atlas = Image.new('RGBA', (1536, 2288), (0,0,0,0))
for row, count in enumerate([6,6,6,6,6,6,6,6,6,8,8]):
    for col in range(count):
        atlas.alpha_composite(pose(col, row), (col*192, row*208))
atlas.save(out)
atlas.save(run / 'final' / 'spritesheet-extended.webp', 'WEBP', lossless=True)
