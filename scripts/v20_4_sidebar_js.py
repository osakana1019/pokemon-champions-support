from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.7 pokedex artwork + rail repair ===== */'
if marker in s: raise SystemExit(0)
old="const v202ClearSprite=m=>`https://play.pokemonshowdown.com/sprites/home-centered/${v201PixelSlug(m)}.png`;\nconst sprite=m=>v202ClearSprite(m);"
new="const v207DexArtworkId=m=>Number(m?.spriteId)||Number(m?.dex)||0;\nconst v207BaseArtwork=m=>`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${Number(m?.dex)||0}.png`;\nconst v202ClearSprite=m=>`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${v207DexArtworkId(m)}.png`;\nconst sprite=m=>v202ClearSprite(m);"
if old in s:s=s.replace(old,new,1)
oldfb="const fallback=m=>specialMegaArt[m.name]||homeSprite(m)||V201_PIXEL_PLACEHOLDER;"
if oldfb in s:s=s.replace(oldfb,"const fallback=m=>v207BaseArtwork(m);",1)
js=r'''<script>
/* ===== v20.7 pokedex artwork + rail repair ===== */
(function(){
'use strict';
function glyph(kind){return `<span class="v207Glyph v207-${kind}" aria-hidden="true"></span>`}
function repairRail(){
 const rail=document.getElementById('v205Rail');if(!rail)return;
 const map=[['[data-page="home"]','home'],['[data-page="quick"]','quick'],['[data-page="party"]','party'],['[data-page="env"]','env'],['[data-settings]','settings']];
 for(const [sel,k] of map){const b=rail.querySelector(sel);if(!b)continue;b.querySelectorAll('svg,.v207Glyph').forEach(x=>x.remove());b.insertAdjacentHTML('afterbegin',glyph(k));}
}
repairRail();setTimeout(repairRail,0);setTimeout(repairRail,300);
window.__V207_TEST__={railGlyphs:()=>document.querySelectorAll('#v205Rail .v207Glyph').length,artwork:String(typeof sprite==='function'?sprite({dex:25}):'').includes('/official-artwork/')};
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1);p.write_text(s,encoding='utf-8')
