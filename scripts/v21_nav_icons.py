from pathlib import Path
import json,re,hashlib,urllib.request

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v21.0 env nav + local transparent zukan icons ===== */'
if marker in s:
    raise SystemExit(0)

# --- Build transparent local icons from the official Pokémon Zukan artwork map ---
# V208_ZUKAN_ART was generated from zukan.pokemon.co.jp in v20.8.
m=re.search(r'const V208_ZUKAN_ART=(\{.*?\});\s*\n',s,re.S)
if not m:
    raise SystemExit('V208_ZUKAN_ART not found')
art=json.loads(m.group(1))

from PIL import Image
from io import BytesIO

outdir=Path('assets/zukan-icons')
outdir.mkdir(parents=True,exist_ok=True)
local={}
UA='Mozilla/5.0 (compatible; ChampionsSupport/21.0)'

def near_white(px):
    r,g,b,a=px
    return a>0 and r>=242 and g>=242 and b>=242 and max(r,g,b)-min(r,g,b)<=10

def clear_edge_white(im):
    im=im.convert('RGBA')
    w,h=im.size
    pix=im.load()
    # Flood-fill only near-white pixels connected to an outer edge. This preserves
    # intentional white parts inside a Pokémon while removing the rectangular tile.
    stack=[]; seen=set()
    for x in range(w):
        stack.append((x,0)); stack.append((x,h-1))
    for y in range(h):
        stack.append((0,y)); stack.append((w-1,y))
    while stack:
        x,y=stack.pop()
        if (x,y) in seen or x<0 or y<0 or x>=w or y>=h: continue
        seen.add((x,y))
        if not near_white(pix[x,y]): continue
        pix[x,y]=(255,255,255,0)
        stack.extend(((x+1,y),(x-1,y),(x,y+1),(x,y-1)))
    # Crop to content with a little breathing room, then fit into a square canvas.
    bbox=im.getbbox()
    if bbox:
        im=im.crop(bbox)
    max_side=220
    im.thumbnail((max_side,max_side),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(240,240),(255,255,255,0))
    x=(240-im.width)//2; y=(240-im.height)//2
    canvas.alpha_composite(im,(x,y))
    return canvas

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'})
    with urllib.request.urlopen(req,timeout=25) as r:
        return r.read()

ok=0; fail=[]
for name,url in art.items():
    if not isinstance(url,str) or not url.startswith('http'):
        continue
    key=hashlib.sha1((name+'|'+url).encode('utf-8')).hexdigest()[:16]
    rel=f'assets/zukan-icons/{key}.webp'
    dest=Path(rel)
    try:
        if not dest.exists():
            raw=fetch(url)
            im=Image.open(BytesIO(raw))
            im=clear_edge_white(im)
            im.save(dest,'WEBP',lossless=True,quality=90,method=6)
        local[name]=rel
        ok+=1
    except Exception as e:
        fail.append((name,str(e)[:120]))

# Require strong coverage; if network is flaky, keep official remote images for misses.
if ok < max(20,int(len(art)*0.70)):
    raise SystemExit(f'local zukan icon coverage too low: {ok}/{len(art)}; sample={fail[:3]}')

local_json=json.dumps(local,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
insert=f"const V210_LOCAL_ZUKAN={local_json};\n"
anchor='const V208_ZUKAN_ART='
pos=s.find(anchor)
if pos<0: raise SystemExit('art anchor missing')
s=s[:pos]+insert+s[pos:]

# Make local transparent copies the primary source. Remote official art remains fallback.
old="const v208ZukanArtwork=m=>V208_ZUKAN_ART[String(m?.name||'')]||V208_ZUKAN_BASE[String(Number(m?.dex)||0)]||v208FallbackArtwork(m);"
new="const v208ZukanArtwork=m=>V210_LOCAL_ZUKAN[String(m?.name||'')]||V208_ZUKAN_ART[String(m?.name||'')]||V208_ZUKAN_BASE[String(Number(m?.dex)||0)]||v208FallbackArtwork(m);"
if old in s:
    s=s.replace(old,new,1)
else:
    s=re.sub(r"const v208ZukanArtwork=m=>[^;]+;",new,s,count=1)

# Version bump.
s=s.replace('Pokémon Champions Support — v20.9','Pokémon Champions Support — v21.0')
s=s.replace('<div class="badge">v20.9</div>','<div class="badge">v21.0</div>',1)

patch=r'''<style id="v210-nav-icon-fix">
/* ===== v21.0 env nav + local transparent zukan icons ===== */
@media(min-width:1080px){
 #v209Nav{width:112px!important}
 body.v209NavOn .wrap{padding-left:140px!important}
 #v209Nav button{min-height:60px!important;overflow:visible!important}
 .v209Ico{font-size:18px!important}
 .v209Lbl{font-size:10px!important;overflow:visible!important;text-overflow:unset!important}
}
/* The processed Zukan assets are transparent; never paint a tile behind the img element. */
.mon img,.sel img,.rankRow img,.oppQuickMon img,.profile img,.pick img,.metaRec img,.savedHead img,.homePartyMon img,.homeMetaMon img,.variantChoice img,.v206SourceMon img,.buildSlot img{
 background:none!important;background-color:transparent!important;border:none!important;outline:none!important;box-shadow:none!important;border-radius:0!important;padding:0!important
}
</style>
<script>
(function(){
'use strict';
function hardOpenEnv(){
  // First use the app's original environment navigation button so all original render hooks run.
  const old=[...document.querySelectorAll('.appnav button')].find(b=>/環境/.test(b.textContent||''));
  if(old){ try{old.click()}catch(e){} }
  setTimeout(()=>{
    const env=document.getElementById('envPage');
    if(!env)return;
    if(!env.classList.contains('activePage')){
      document.querySelectorAll('.page').forEach(x=>x.classList.remove('activePage'));
      env.classList.add('activePage');
      document.querySelectorAll('.appnav button').forEach(x=>x.classList.remove('activeApp'));
    }
    try{ if(typeof renderEnv==='function')renderEnv(); }catch(e){}
    try{ if(typeof renderEnvironment==='function')renderEnvironment(); }catch(e){}
    try{ if(typeof renderEnvRanking==='function')renderEnvRanking(); }catch(e){}
    try{ if(typeof renderRanking==='function')renderRanking(); }catch(e){}
    window.scrollTo({top:0,behavior:'instant'});
  },0);
}
function wire(){
 const n=document.getElementById('v209Nav'); if(!n)return;
 const env=n.querySelector('[data-k="env"]');
 if(env && !env.dataset.v210){ env.dataset.v210='1'; env.onclick=hardOpenEnv; }
}
wire();setTimeout(wire,100);setInterval(wire,1000);
window.__V210_TEST__={env:hardOpenEnv,localIcons:()=>Object.keys(V210_LOCAL_ZUKAN||{}).length};
})();
</script>'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print(f'v21.0 local transparent zukan icons: {ok}/{len(art)}; failures={len(fail)}')
