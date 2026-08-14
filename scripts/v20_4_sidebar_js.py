from pathlib import Path
import concurrent.futures, html as htmlmod, json, re, time, unicodedata
from urllib.parse import urljoin
from urllib.request import Request, urlopen

p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.8 official zukan artwork + labeled rail ===== */'
if marker in s: raise SystemExit(0)

# Build an exact artwork map from the official Japanese Pokémon Pokédex.
# The Pokédex already contains the newly introduced Mega forms, so this avoids
# waiting for third-party sprite repositories to add them.
mons_match=re.search(r'const mons=(\[.*?\]);\s*\n',s,re.S)
if not mons_match:
    raise SystemExit('mons dataset not found')
mons=json.loads(mons_match.group(1))
used_dex=sorted({int(m.get('dex') or 0) for m in mons if int(m.get('dex') or 0)>0})

UA='Mozilla/5.0 (compatible; ChampionsSupport/20.8; +https://github.com/osakana1019/pokemon-champions-support)'

def fetch(url,retries=2):
    last=None
    for n in range(retries+1):
        try:
            req=Request(url,headers={'User-Agent':UA,'Accept-Language':'ja,en;q=0.7'})
            with urlopen(req,timeout=18) as r:
                return r.read().decode('utf-8','replace')
        except Exception as e:
            last=e
            if n<retries: time.sleep(.35*(n+1))
    raise last

def meta_value(text,key):
    pats=[
        rf'<meta[^>]+property=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']{re.escape(key)}["\']'
    ]
    for pat in pats:
        m=re.search(pat,text,re.I)
        if m:return htmlmod.unescape(m.group(1)).strip()
    return ''

def clean_title(v):
    v=htmlmod.unescape(v or '').split('｜')[0].strip()
    return v

def key_name(v):
    v=unicodedata.normalize('NFKC',str(v or '')).strip().lower()
    v=v.replace('（','(').replace('）',')')
    v=re.sub(r'[\s・･]+','',v)
    return v

def loose_key(v):
    v=key_name(v)
    for x in ['のすがた','すがた']:
        v=v.replace(x,'')
    v=v.replace('(','').replace(')','')
    return v

def collect_dex(dex):
    root=f'https://zukan.pokemon.co.jp/detail/{dex:04d}'
    out=[]
    try:
        base=fetch(root)
    except Exception as e:
        return dex,[],str(e)
    def add(page,url):
        title=clean_title(meta_value(page,'og:title'))
        image=meta_value(page,'og:image')
        if title and image:
            out.append((title,image,url))
    add(base,root)
    paths=set(re.findall(r'href=["\']([^"\']*?/detail/%04d(?:-[0-9]+)?(?:[?#][^"\']*)?)["\']'%dex,base,re.I))
    urls=[]
    for path in paths:
        u=urljoin(root,path).split('#')[0]
        if u.rstrip('/')!=root.rstrip('/'):urls.append(u)
    for u in sorted(set(urls)):
        try:add(fetch(u,1),u)
        except Exception:pass
    return dex,out,''

zukan_entries={}
errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futs=[ex.submit(collect_dex,d) for d in used_dex]
    for f in concurrent.futures.as_completed(futs):
        dex,rows,err=f.result()
        if err: errors.append((dex,err))
        if rows:zukan_entries[dex]=rows

art={}; base_art={}; detail_urls={}
for dex,rows in zukan_entries.items():
    if rows:
        # Prefer the no-suffix base detail as base artwork.
        base_row=next((r for r in rows if r[2].rstrip('/').endswith(f'/{dex:04d}')),rows[0])
        base_art[str(dex)]=base_row[1]
    by_exact={key_name(t):(t,img,u) for t,img,u in rows}
    by_loose={loose_key(t):(t,img,u) for t,img,u in rows}
    for m in [x for x in mons if int(x.get('dex') or 0)==dex]:
        name=str(m.get('name') or '')
        hit=by_exact.get(key_name(name)) or by_loose.get(loose_key(name))
        if not hit:
            # Fuzzy fallback for app labels such as shortened gender/form annotations.
            lk=loose_key(name)
            hit=next((r for r in rows if lk and (lk in loose_key(r[0]) or loose_key(r[0]) in lk)),None)
        if hit:
            art[name]=hit[1];detail_urls[name]=hit[2]
        elif str(dex) in base_art:
            art[name]=base_art[str(dex)]

# These are critical regression checks: the official Pokédex has pages for them.
# Only require a name when that Pokémon exists in the app's roster.
required=['メガカイリュー','メガスターミー','メガライチュウX','メガライチュウＸ','メガライチュウY','メガライチュウＹ']
app_names={str(m.get('name') or '') for m in mons}
missing=[n for n in required if n in app_names and n not in art]
if missing:
    raise SystemExit('official zukan artwork missing for: '+', '.join(missing))
coverage=len(art)/max(1,len(mons))
if coverage<0.90:
    raise SystemExit(f'zukan artwork coverage too low: {len(art)}/{len(mons)} ({coverage:.1%}); sample errors={errors[:3]}')

art_json=json.dumps(art,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
base_json=json.dumps(base_art,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
url_json=json.dumps(detail_urls,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

# Replace the temporary PokeAPI artwork provider with the official Pokédex map.
pat=r"const v207DexArtworkId=m=>.*?const sprite=m=>v202ClearSprite\(m\);"
replacement=(
    f"const V208_ZUKAN_ART={art_json};\n"
    f"const V208_ZUKAN_BASE={base_json};\n"
    f"const V208_ZUKAN_DETAIL={url_json};\n"
    "const v208FallbackArtwork=m=>`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${Number(m?.spriteId)||Number(m?.dex)||0}.png`;\n"
    "const v208ZukanArtwork=m=>V208_ZUKAN_ART[String(m?.name||'')]||V208_ZUKAN_BASE[String(Number(m?.dex)||0)]||v208FallbackArtwork(m);\n"
    "const v207BaseArtwork=m=>V208_ZUKAN_BASE[String(Number(m?.dex)||0)]||v208FallbackArtwork(m);\n"
    "const v202ClearSprite=m=>v208ZukanArtwork(m);\n"
    "const sprite=m=>v208ZukanArtwork(m);"
)
s,n=re.subn(pat,replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('v20.7 artwork provider not found')

js=r'''<script>
/* ===== v20.8 official zukan artwork + labeled rail ===== */
(function(){
'use strict';
const RAIL={
 home:['⌂','ホーム'],quick:['⚡','選出'],party:['●●','パーティ'],env:['▥','環境'],settings:['⚙','設定']
};
function decorate(sel,key){
 const b=document.querySelector('#v205Rail '+sel);if(!b)return;
 b.querySelectorAll('svg,.v207Glyph,.v208RailIcon,.v208RailLabel').forEach(x=>x.remove());
 const [icon,label]=RAIL[key];
 b.insertAdjacentHTML('afterbegin',`<span class="v208RailIcon" aria-hidden="true">${icon}</span><span class="v208RailLabel">${label}</span>`);
 b.setAttribute('aria-label',label);b.title=label;
}
function repairRail(){
 decorate('[data-page="home"]','home');decorate('[data-page="quick"]','quick');decorate('[data-page="party"]','party');decorate('[data-page="env"]','env');decorate('[data-settings]','settings');
}
repairRail();setTimeout(repairRail,0);setTimeout(repairRail,250);
window.__V208_TEST__={
 railLabels:()=>document.querySelectorAll('#v205Rail .v208RailLabel').length,
 zukanArt:()=>typeof V208_ZUKAN_ART==='object'&&Object.keys(V208_ZUKAN_ART).length,
 megaDragonite:()=>V208_ZUKAN_ART['メガカイリュー']||'',
 source:'zukan.pokemon.co.jp'
};
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print(f'v20.8 zukan artwork: {len(art)}/{len(mons)} ({coverage:.1%}), dex groups {len(zukan_entries)}')
