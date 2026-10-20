#!/usr/bin/env python3
"""Génère une page par pièce : /p/<N°>/index.html

Chaque page a sa propre photo d'aperçu (balises og:), donc quand une cliente
envoie le lien sur WhatsApp, Saran voit directement la photo de la tenue.
Tout est lu dans index.html (PRODUCTS, VENDUES, WHATSAPP) : il n'y a rien à
modifier ici. Netlify lance ce script à chaque mise à jour (voir netlify.toml).
"""
import html, json, os, re, shutil

SITE = 'https://sk-mode.netlify.app'
ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

def js_str(field, block):
    m = re.search(field + r":\s*'((?:[^'\\]|\\.)*)'", block)
    return m.group(1).replace("\\'", "'") if m else ''

WHATSAPP = re.search(r"const WHATSAPP = '([^']*)'", src).group(1)
VENDUES = [int(x) for x in re.findall(r'\d+', re.search(r'const VENDUES = \[([^\]]*)\]', src).group(1))]
block = re.search(r'const PRODUCTS = \[(.*?)\n  \];', src, re.S).group(1)

pieces = [dict(n=1, name='Robe bustier à bretelles nouées', price='180 000', aba=False, tag='Robe longue',
               desc='Haut bustier coloré, bretelles nouées sur les épaules, longue jupe fluide.',
               photo='photos/hero-robe-bretelles-3-vues.jpg')]
for i, line in enumerate(l for l in block.split('\n') if l.strip().startswith('{')):
    p = dict(n=i + 2, name=js_str('name', line), price=js_str('price', line), aba='aba: true' in line,
             tag=js_str('tag', line), desc=js_str('desc', line), photo=js_str('photo', line))
    if p['photo']:
        pieces.append(p)

def wa(msg):
    from urllib.parse import quote
    return 'https://wa.me/' + re.sub(r'\D', '', WHATSAPP) + '?text=' + quote(msg)

E = lambda s: html.escape(s, quote=True)
TPL = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · SK</title>
<meta name="description" content="{ogdesc}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="SK · Mode &amp; élégance">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{ogdesc}">
<meta property="og:image" content="{img}">
<meta property="og:image:alt" content="{name}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/logo-sk-profil.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@600;700&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<style>
  :root{{--sand:#F6F0E6;--ink:#231C16;--text2:#5A4E42;--clay:#8A4526;--green:#1F7A4D}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--sand);color:var(--ink);font-family:'Manrope',system-ui,sans-serif}}
  .wrap{{max-width:1040px;margin:0 auto;padding:16px 16px 48px;display:flex;flex-direction:column;gap:20px}}
  header{{display:flex;align-items:center;justify-content:space-between;gap:12px}}
  header a{{color:var(--ink);font-weight:700;font-size:15px}}
  .grid{{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start}}
  .ph{{flex:1 1 360px;min-width:0;position:relative}}
  .ph img{{display:block;width:100%;border-radius:24px;background:#EDE3D4}}
  .badge{{position:absolute;top:14px;left:14px;padding:6px 12px;border-radius:999px;background:var(--ink);color:var(--sand);font-size:13px;font-weight:800}}
  .sold{{left:auto;right:14px;background:var(--clay);color:#fff;text-transform:uppercase;letter-spacing:.06em}}
  .info{{flex:1 1 320px;min-width:0;display:flex;flex-direction:column;gap:16px}}
  .eyebrow{{font-size:13px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--clay)}}
  h1{{margin:0;font-family:'Cormorant',serif;font-weight:700;font-size:clamp(40px,6vw,60px);line-height:1}}
  .price{{font-weight:800;font-size:28px}}
  p{{margin:0;font-size:17px;line-height:1.6;color:var(--text2)}}
  .btn{{display:flex;align-items:center;justify-content:center;min-height:56px;padding:0 24px;border-radius:999px;font-weight:800;font-size:17px;text-decoration:none}}
  .wa{{background:var(--green);color:#fff}}
  .ghost{{border:1.5px solid var(--ink);color:var(--ink)}}
  ul{{margin:0;padding-left:20px;color:var(--text2);line-height:1.8}}
</style>
</head>
<body>
<div class="wrap">
  <header><a href="/"><img src="/logo-sk.svg" alt="SK" width="72" height="48"></a><a href="/#collection">Toute la collection →</a></header>
  <div class="grid">
    <div class="ph"><img src="/{photo}" alt="{name}"><span class="badge">N° {n}</span>{soldbadge}</div>
    <div class="info">
      <div class="eyebrow">{tag} · Pièce unique</div>
      <h1>{name}</h1>
      <div class="price">{price} GNF</div>
      <p>{desc}</p>
      <ul>{bullets}</ul>
      <a class="btn wa" id="cta" href="{href}" target="_blank" rel="noopener">{cta}</a>
      <a class="btn ghost" href="/#collection">Voir les autres pièces</a>
    </div>
  </div>
</div>
<script>
  // garde la référence de la pub (?src=fb…) dans le message WhatsApp
  const s = (new URLSearchParams(location.search).get('src') || '').slice(0, 20);
  if (s) {{ const a = document.getElementById('cta'); a.href = a.href.replace('fiche%29', encodeURIComponent(s) + '%29'); }}
</script>
</body>
</html>
'''

out = os.path.join(ROOT, 'p')
shutil.rmtree(out, ignore_errors=True)
for p in pieces:
    n, sold = p['n'], p['n'] in VENDUES
    url = f"{SITE}/p/{n}/"
    title = f"N° {n} · {p['name']} — {p['price']} GNF"
    if sold:
        msg = (f"Bonjour SK ! L’abaya N° {n} ({p['name']}) est vendue. Prévenez-moi au prochain arrivage de Dubaï."
               if p['aba'] else
               f"Bonjour SK ! La pièce N° {n} ({p['name']}) est vendue. Je voudrais qu’on me la recouse à ma taille.\nMa taille : \nMon quartier / ville : ")
        cta = 'Être prévenue du prochain arrivage' if p['aba'] else 'La recoudre à ma taille'
        ogdesc = 'Vendue · ' + ('prochain arrivage sur demande.' if p['aba'] else 'on peut la recoudre à ta taille.')
    else:
        msg = f"Bonjour SK ! Je veux la pièce N° {n} : {p['name']} ({p['price']} GNF). Elle est encore disponible ?\nMon quartier / ville : "
        cta = 'Je la veux sur WhatsApp'
        ogdesc = f"Pièce unique · {p['price']} GNF · payé à la livraison à Conakry."
    msg += f"\n\nPhoto : {url}\n(réf : fiche)"
    bullets = ''.join(f'<li>{b}</li>' for b in [
        'Une seule pièce : la première qui confirme l’emporte',
        'Voile inclus' if p['aba'] else 'Taille confirmée avec toi sur WhatsApp',
        'Livrée chez toi à Conakry · paiement à la livraison',
        'Espèces, Orange Money ou MTN MoMo'])
    page = TPL.format(title=E(title), ogdesc=E(ogdesc), img=E(SITE + '/' + p['photo']), name=E(p['name']),
                      url=E(url), photo=E(p['photo']), n=n, tag=E(p['tag']), price=E(p['price']), desc=E(p['desc']),
                      bullets=bullets, href=E(wa(msg)), cta=cta,
                      soldbadge='<span class="badge sold">Vendue</span>' if sold else '')
    os.makedirs(os.path.join(out, str(n)), exist_ok=True)
    open(os.path.join(out, str(n), 'index.html'), 'w', encoding='utf-8').write(page)
print(f'{len(pieces)} fiches générées dans p/ (vendues : {VENDUES or "aucune"})')
