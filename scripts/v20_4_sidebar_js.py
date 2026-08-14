from pathlib import Path
import concurrent.futures, html as htmlmod, json, re, unicodedata
from urllib.parse import urljoin
from urllib.request import Request, urlopen

p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.9 zukan transparent artwork + rebuilt nav ===== */'
if marker in s: raise SystemExit(0)

def key(v):
    v=unicodedata.normalize('NFKC',str(v or '')).strip().lower()
    v=v.replace('（','(').replace('）',')')
    v=re.sub(r'[\s・･]+','',v)
    return v

def attrs(tag):
    out={}
    for m in re.finditer(r'([:\w-]+)\s*=\s*(["\'])(.*?)\2',tag,re.S):
        out[m.group(1).lower()]=htmlmod.unescape(m.group(3).strip())
    return out

def fetch(url):
    req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; ChampionsSupport/20.9)','Accept-Language':'ja,en;q=0.7'})
    with urlopen(req,timeout=20) as r:
        return r.read().decode('utf-8','replace')

mons_m=re.search(r'const mons=(\[.*?\]);\s*\n',s,re.S)
detail_m=re.search(r'const V208_ZUKAN_DETAIL=(\{.*?\});\s*\n',s,re.S)
if not mons_m or not detail_m: raise SystemExit('v20.8 zukan maps not found')
mons=json.loads(mons_m.group(1)); details=json.loads(detail_m.group(1))

# Fetch each official detail page once, then choose the actual in-page image whose alt text
# matches the Pokémon name. This avoids the white social-preview og:image tile.
by_url={}
for name,url in details.items():
    if url: by_url.setdefault(url,[]).append(name)

def one(url,names):
    try: page=fetch(url)
    except Exception: return {}
    tags=re.findall(r'<img\b[^>]*>',page,re.I|re.S)
    found={}
    for name in names:
        nk=key(name); candidates=[]
        for pos,tag in enumerate(tags):
            a=attrs(tag)
            alt=key(a.get('alt',''))
            if not alt or alt!=nk: continue
            src=a.get('src') or a.get('data-src') or a.get('data-original') or ''
            if not src or src.startswith('data:'): continue
            src=urljoin(url,src)
            score=1000-pos
            low=src.lower()
            if any(x in low for x in ('pokemon','detail','zukan')): score+=100
            if low.endswith(('.png','.webp')): score+=30
            if 'icon' in low or 'logo' in low: score-=500
            try: score+=min(200,int(a.get('width','0'))+int(a.get('height','0')))
            except Exception: pass
            candidates.append((score,src))
        if candidates:
            candidates.sort(reverse=True);found[name]=candidates[0][1]
    return found

art={}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    futs=[ex.submit(one,u,names) for u,names in by_url.items()]
    for f in concurrent.futures.as_completed(futs):
        try: art.update(f.result())
        except Exception: pass

old_art_m=re.search(r'const V208_ZUKAN_ART=(\{.*?\});\s*\n',s,re.S)
old_base_m=re.search(r'const V208_ZUKAN_BASE=(\{.*?\});\s*\n',s,re.S)
old_art=json.loads(old_art_m.group(1)) if old_art_m else {}
old_base=json.loads(old_base_m.group(1)) if old_base_m else {}
# Keep old official map only as fallback when the live detail page did not expose an exact img tag.
merged=dict(old_art);merged.update(art)
base={}
for m in mons:
    name=str(m.get('name') or '');dex=str(int(m.get('dex') or 0))
    if not dex or dex=='0': continue
    if name in art and (not name.startswith('メガ')) and dex not in base: base[dex]=art[name]
for dex,u in old_base.items(): base.setdefault(str(dex),u)

art_json=json.dumps(merged,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
base_json=json.dumps(base,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
s,n=re.subn(r'const V208_ZUKAN_ART=\{.*?\};\s*\n',f'const V208_ZUKAN_ART={art_json};\n',s,count=1,flags=re.S)
if n!=1: raise SystemExit('V208_ZUKAN_ART replace failed')
s,n=re.subn(r'const V208_ZUKAN_BASE=\{.*?\};\s*\n',f'const V208_ZUKAN_BASE={base_json};\n',s,count=1,flags=re.S)
if n!=1: raise SystemExit('V208_ZUKAN_BASE replace failed')

# Require exact transparent-page artwork for important new Mega forms when they are in the roster.
app_names={str(m.get('name') or '') for m in mons}
critical=['メガカイリュー','メガスターミー','メガライチュウX','メガライチュウＸ','メガライチュウY','メガライチュウＹ']
missing=[x for x in critical if x in app_names and x not in art]
if missing: raise SystemExit('exact official detail artwork missing: '+', '.join(missing))

js=r'''<script>
/* ===== v20.9 zukan transparent artwork + rebuilt nav ===== */
(function(){
'use strict';
function openSettings(){const p=document.getElementById('v202SettingsPanel');if(p)p.classList.add('show');else document.getElementById('v202SettingsBtn')?.click()}
function make(){
 document.getElementById('v205Rail')?.remove();document.getElementById('v209Nav')?.remove();
 const n=document.createElement('aside');n.id='v209Nav';n.setAttribute('aria-label','メインメニュー');
 n.innerHTML=`<div class="v209Brand">CS</div><div class="v209Sep"></div>
 <button data-k="home"><span class="v209Ico">⌂</span><span class="v209Lbl">ホーム</span></button>
 <button data-k="quick"><span class="v209Ico">⚡</span><span class="v209Lbl">選出</span></button>
 <button data-k="party"><span class="v209Ico">6</span><span class="v209Lbl">パーティ</span><span class="v209Count">0</span></button>
 <button data-k="env"><span class="v209Ico">▥</span><span class="v209Lbl">環境</span></button>
 <div class="v209Bottom"><button data-k="settings"><span class="v209Ico">⚙</span><span class="v209Lbl">設定</span></button></div>`;
 document.body.appendChild(n);document.body.classList.add('v209NavOn');
 n.querySelector('[data-k=home]').onclick=()=>switchPage('home');
 n.querySelector('[data-k=quick]').onclick=()=>switchPage('quick');
 n.querySelector('[data-k=party]').onclick=()=>typeof v205OpenParty==='function'?v205OpenParty():switchPage('saved');
 n.querySelector('[data-k=env]').onclick=()=>switchPage('env');
 n.querySelector('[data-k=settings]').onclick=openSettings;
}
function active(){
 const n=document.getElementById('v209Nav');if(!n)return;
 const activePage=document.querySelector('.page.activePage')?.id||'';
 let k=activePage==='homePage'?'home':activePage==='quickPage'?'quick':activePage==='partyPage'?'party':activePage==='envPage'?'env':'';
 n.querySelectorAll('button[data-k]').forEach(b=>b.classList.toggle('active',b.dataset.k===k));
 const c=n.querySelector('.v209Count');if(c){try{c.textContent=String((savedParty||[]).length)}catch(e){c.textContent='0'}}
}
make();active();setTimeout(()=>{make();active()},80);setInterval(active,500);
window.__V209_TEST__={nav:()=>document.querySelectorAll('#v209Nav .v209Lbl').length,exactZukan:()=>Object.keys(V208_ZUKAN_ART||{}).length,source:'zukan.pokemon.co.jp detail img'};
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print(f'v20.9 exact in-page zukan images: {len(art)} / {len(details)}')
