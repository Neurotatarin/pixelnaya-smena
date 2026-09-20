# Builds source images for @capacitor/assets from the same drawing code as the site icons.
import os
src = open('mkicons.py', encoding='utf-8').read().split('\nfor S,n,m')[0]
ns = {}
exec(src, ns)
icon, Image = ns['icon'], ns['Image']
os.makedirs('assets', exist_ok=True)
icon(1024, 0).save('assets/icon-only.png')
icon(1024, 1).save('assets/icon-foreground.png')
Image.new('RGB', (1024, 1024), (159, 182, 255)).save('assets/icon-background.png')
def splash(path):
    S = 2732
    im = Image.new('RGB', (S, S))
    top, mid, bot = (124, 202, 255), (179, 163, 255), (255, 182, 217)
    px = im.load()
    rows = []
    for y in range(S):
        t = y / S
        a, b, k = (top, mid, t / 0.55) if t < 0.55 else (mid, bot, (t - 0.55) / 0.45)
        rows.append(tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
    for y, c in enumerate(rows):
        im.paste(c, (0, y, S, y + 1))
    ic = icon(1024, 0).resize((640, 640))
    im.paste(ic, ((S - 640) // 2, (S - 640) // 2))
    im.save(path)
splash('assets/splash.png')
splash('assets/splash-dark.png')
print('assets ready')
