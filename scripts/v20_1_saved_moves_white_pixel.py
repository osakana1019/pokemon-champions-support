from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v20.1: durable saved moves + white UI + unified pixel sprites ===== */'
if marker in s:
    raise SystemExit(0)

s=s.replace('Pokémon Champions Support — v20.0','Pokémon Champions Support — v20.1')
s=s.replace('<meta name="color-scheme" content="dark">','<meta name="color-scheme" content="light">')

old_sprite="const sprite=m=>specialMegaArt[m.name]||m.spriteUrl||homeSprite(m);"
new_sprite=r'''const v201PixelSlug=m=>{
 const known=String(m?.spriteUrl||'').match(/\/sprites\/gen5\/([^?#]+)/i);
 if(known)return known[1].replace(/\.png$/i,'');
 return String(m?.championsId||'').toLowerCase().normalize('NFKD')
  .replace(/[.’'`]/g,'').replace(/\s+/g,'').replace(/[^a-z0-9-]/g,'');
};
const v201PixelSprite=m=>`https://play.pokemonshowdown.com/sprites/gen5/${v201PixelSlug(m)}.png`;
const sprite=m=>v201PixelSprite(m);'''
if old_sprite not in s:
    raise SystemExit('sprite declaration not found')
s=s.replace(old_sprite,new_sprite,1)

old_fallback="const fallback=m=>SHOWDOWN_SPRITE_OVERRIDES[m.name]||`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${m.dex}.png`;"
new_fallback=r'''const V201_PIXEL_PLACEHOLDER='data:image/svg+xml;charset=UTF-8,'+encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><rect width="96" height="96" rx="18" fill="#f1f3f5"/><circle cx="48" cy="48" r="27" fill="none" stroke="#aeb5bf" stroke-width="6"/><path d="M21 48h54" stroke="#aeb5bf" stroke-width="6"/><circle cx="48" cy="48" r="9" fill="#fff" stroke="#aeb5bf" stroke-width="5"/></svg>`);
const fallback=m=>V201_PIXEL_PLACEHOLDER;'''
if old_fallback not in s:
    raise SystemExit('fallback declaration not found')
s=s.replace(old_fallback,new_fallback,1)

patch=r'''
<style id="v201-white-theme">
/* ===== v20.1: clean white / graphite UI ===== */
:root{
 --bg:#f5f6f8!important;--panel:#ffffff!important;--line:#d9dee6!important;--text:#171a1f!important;--muted:#727986!important;
 --accent:#171a1f!important;--accent2:#3b4048!important;
 --v201-bg:#f5f6f8;--v201-card:#fff;--v201-card2:#f9fafb;--v201-line:#d9dee6;--v201-line2:#c8ced8;
 --v201-text:#171a1f;--v201-muted:#747b87;--v201-strong:#111318;--v201-soft:#eef1f4;--v201-hover:#f0f2f5;
 --v201-danger:#b33d4c;--v201-danger-bg:#fff1f3;--v201-mega:#9b6a18;--v201-mega-bg:#fff6df;
}
html{background:var(--v201-bg)!important;color-scheme:light!important}
body{background:linear-gradient(180deg,#fff 0,#f6f7f9 180px,#f3f5f7 100%)!important;color:var(--v201-text)!important}
header h1,h1,h2,h3,h4,.pn,.mn,.name,b,strong{color:var(--v201-strong)}
.small,.sub,.v19Muted,.formEvidence,.loadedSet,.buildReasons{color:var(--v201-muted)!important}
.card,.teamPane,.savedEditor,.counterToolCard,.v19IntelCard,.metaRec,.pick,.v12BuildPick,.v19Mini,.v19TeamSpeed,.variantCard{
 background:var(--v201-card)!important;border-color:var(--v201-line)!important;color:var(--v201-text)!important;
 box-shadow:0 8px 28px rgba(25,32,44,.055)!important;
}
.card .card,.dataSection,.typeMatchSection{background:var(--v201-card2)!important;border-color:var(--v201-line)!important}
.appnav{background:rgba(255,255,255,.94)!important;border-color:var(--v201-line)!important;box-shadow:0 8px 28px rgba(20,27,39,.08)!important}
.appnav button{background:transparent!important;color:#69717d!important;box-shadow:none!important}
.appnav button:hover{background:#f1f3f5!important;color:#171a1f!important}
.appnav button.activeApp,.appnav .activeApp{background:#171a1f!important;color:#fff!important;box-shadow:none!important}
button{background:#eef1f4!important;color:#24282f!important;box-shadow:inset 0 0 0 1px #d7dce4!important}
button:hover{background:#e5e9ee!important;filter:none!important}
button.primary,.primary,.mineAdd,.buildAddBtn{background:#171a1f!important;color:#fff!important;box-shadow:none!important}
.oppAdd{background:#fff0f2!important;color:#a33b49!important;box-shadow:inset 0 0 0 1px #efc9cf!important}
input,select,textarea,.savedItem,.moveRow input,.moveRow select,.buildItemInput,.buildMoveInput{
 background:#fff!important;color:#171a1f!important;border-color:#cfd5de!important;box-shadow:none!important;
}
input::placeholder,textarea::placeholder{color:#a0a6b0!important}
input:focus,select:focus,textarea:focus,.buildMoveInput:focus{outline:none!important;border-color:#777f8c!important;box-shadow:0 0 0 3px rgba(32,37,45,.08)!important}
.moveSuggestBox,.buildMoveSuggestBox,.itemSuggestBox,.counterSuggestBoxV186{background:#fff!important;border-color:#cfd5de!important;color:#171a1f!important;box-shadow:0 14px 36px rgba(21,27,38,.13)!important}
.moveSuggestItem,.buildMoveSuggestItem,.counterSuggestRowV186{color:#171a1f!important;border-color:#edf0f3!important}
.moveSuggestItem:hover,.buildMoveSuggestItem:hover,.counterSuggestRowV186:hover,.counterSuggestRowV186.active{background:#f2f4f6!important;color:#111318!important}
.moveKind,.v19Chip,.v19Speed,.v19CandidateTag,.buildBreakdown span,.v12Breakdown span,.matchChip,.counterRecBadge,.badge,.sourceBadge,.v19Source{
 background:#f1f3f5!important;border-color:#d9dee5!important;color:#555d69!important;
}
.mon,.sel,.rankRow,.oppQuickMon,.variantChoice,.savedEmpty{background:#fafbfc!important;border-color:#dce1e7!important;color:#171a1f!important}
.mon:hover,.rankRow:hover,.oppQuickMon:hover,.variantChoice:hover{background:#f1f3f5!important}
.rankRow.envSelected,.oppQuickMon.selected{background:#eceff3!important;outline-color:#8e96a3!important}
.profile img,.savedHead img,.mon img,.sel img,.rankRow img,.oppQuickMon img,.pick img,.metaRec img,.variantChoice img{image-rendering:pixelated;filter:none!important}
.compatPct,.quickPct,.completionScore,.metaScore,.rankNo,.counter,.buildMovePct,.spreadStat.active .spValue,.v19Chip strong,.v19Speed strong{color:#252a31!important}
.compatBar,.bar,.spreadMiniBar,.envDbProgress,.envPctBar{background:#e4e8ed!important}
.compatBar>div,.bar>div,.spreadMiniBar>div,.envDbProgress>div,.envPctBar>div{background:#505763!important}
.metaAnalysisStatus,.buildMetaStatus{background:#f6f7f9!important;border-color:#d7dce4!important;color:#3b424c!important}
.dragHandle,.tabletReorder button{background:#f3f5f7!important;border-color:#d7dce4!important;color:#626a76!important}
.megaBadge{background:var(--v201-mega-bg)!important;color:var(--v201-mega)!important;border:1px solid #ead49f!important}
.v193ExactHigh,.v192EvidenceHigh{background:#eef8f2!important;border-color:#bedcc9!important;color:#29714a!important}
.v193ExactLow,.v192EvidenceLow,.v194Duplicate{background:var(--v201-danger-bg)!important;border-color:#e8bcc4!important;color:var(--v201-danger)!important}
.v19TrendUp{color:#25734b!important}.v19TrendDown{color:#b43d4c!important}
.typeChip{box-shadow:none!important}
.v194UiIcon{stroke-width:1.9}
.v194Toast{background:#171a1f!important;border-color:#171a1f!important;color:#fff!important;box-shadow:0 12px 32px rgba(0,0,0,.15)!important}
::-webkit-scrollbar-thumb{background:#c6ccd4!important;border-radius:999px}::-webkit-scrollbar-track{background:#f1f3f5!important}
::selection{background:#d9dde3!important;color:#111!important}
</style>
<script>
/* ===== v20.1: durable saved moves + white UI + unified pixel sprites ===== */
(function(){
'use strict';
const STORE='champ_saved_move_shadow_v201';
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const norm=s=>{try{return normalizeMoveSearch(s)}catch(e){return String(s||'').normalize('NFKC').trim().toLowerCase()}};
const moveObj=x=>typeof x==='string'?{name:String(x).trim(),type:'変化'}:(x&&typeof x==='object'?{name:String(x.name||'').trim(),type:String(x.type||'変化').trim()||'変化'}:{name:'',type:'変化'});
function readShadow(){try{const x=JSON.parse(localStorage.getItem(STORE)||'{}');return x&&typeof x==='object'?x:{}}catch(e){return {}}}
function writeShadow(x){try{localStorage.setItem(STORE,JSON.stringify(x))}catch(e){}}
let shadow=readShadow();
function arr4(src){return Array.from({length:4},(_,i)=>moveObj(Array.isArray(src)?src[i]:null))}
function hasAny(arr){return (arr||[]).some(x=>String(x?.name||'').trim())}
function rescueSources(mon){
 const out=[];
 if(Array.isArray(mon?.moves))out.push(arr4(mon.moves));
 if(Array.isArray(mon?.set?.moves))out.push(arr4(mon.set.moves));
 try{const q=(mine||[]).find(x=>x?.name===mon?.name);if(Array.isArray(q?.set?.moves))out.push(arr4(q.set.moves));}catch(e){}
 try{const b=(buildTeam||[]).find(x=>x?.name===mon?.name);if(Array.isArray(b?.set?.moves))out.push(arr4(b.set.moves));}catch(e){}
 return out;
}
function canonicalMoves(mon){
 if(!mon)return arr4([]);
 const key=String(mon.name||'');
 if(Object.prototype.hasOwnProperty.call(shadow,key))return arr4(shadow[key]);
 const sources=rescueSources(mon);
 const out=arr4([]);
 for(let i=0;i<4;i++){
   for(const src of sources){if(src[i]?.name){out[i]=moveObj(src[i]);break;}}
 }
 // If no slot-aligned data survived, salvage the first non-empty array as entered.
 if(!hasAny(out)){
   const best=sources.find(hasAny);if(best)for(let i=0;i<4;i++)out[i]=moveObj(best[i]);
 }
 shadow[key]=out;writeShadow(shadow);
 return arr4(out);
}
function persistMon(i){
 const mon=savedParty?.[i];if(!mon)return;
 mon.moves=arr4(mon.moves);shadow[String(mon.name||'')]=arr4(mon.moves);writeShadow(shadow);
 try{saveSavedParty()}catch(e){localStorage.setItem('champ_saved_party',JSON.stringify(savedParty))}
}
function hydrateMon(i){
 const mon=savedParty?.[i];if(!mon)return null;
 mon.moves=canonicalMoves(mon);persistMon(i);return mon;
}
function duplicate(i,j,name){const k=norm(name);if(!k)return false;return (savedParty?.[i]?.moves||[]).some((x,n)=>n!==j&&norm(x?.name)===k)}
function inferMove(mon,name){
 const k=norm(name);return moveSuggestionsFor(mon).find(x=>norm(x.name)===k)||(typeof globalMoveDB!=='undefined'?globalMoveDB.find(x=>norm(x.name)===k):null);
}

// Migrate every currently registered set before anything can render it.
for(let i=0;i<(savedParty||[]).length;i++)hydrateMon(i);

// Source of truth: every keystroke writes both the party payload and a shadow copy.
updateSavedMove=function(i,j,key,v){
 const mon=hydrateMon(i);if(!mon)return;
 if(key==='name'){
   const name=String(v||'');
   if(name.trim()&&duplicate(i,j,name))return;
   mon.moves[j].name=name;
 }else mon.moves[j][key]=v;
 persistMon(i);
 try{renderSavedCompletion()}catch(e){}
};
chooseMoveSuggestion=function(i,j,name){
 const mon=hydrateMon(i);if(!mon)return;
 if(duplicate(i,j,name)){try{v194Toast('同じポケモンに同じ技は2つ入れられません')}catch(e){}return;}
 const hit=inferMove(mon,name);mon.moves[j]={name,type:hit?moveDisplayType(hit):'変化'};persistMon(i);renderSavedEditors();try{renderSavedCompletion()}catch(e){}
};
applyMoveSuggestion=function(i,j,name){return chooseMoveSuggestion(i,j,name)};

// Rebuild the registration editor from the durable source instead of relying on an old length===4 branch.
renderSavedEditors=function(){
 const root=document.getElementById('savedEditors');if(!root)return;
 root.innerHTML=Array.from({length:6},(_,i)=>{
   const m=savedParty[i];if(!m)return `<div class="savedEmpty">空き ${i+1}</div>`;
   hydrateMon(i);const moves=arr4(m.moves);
   return `<div class="savedEditor" data-v201-saved-index="${i}">
    <div class="savedHead">
     <img src="${sprite(m)}" onerror="if(!this.dataset.fallback){this.dataset.fallback='1';this.src=fallback(savedParty[${i}]||{})}else{this.onerror=null}">
     <div style="min-width:0;flex:1"><b>${esc(m.name)}</b><div>${typeChip(m.t1)}${typeChip(m.t2)}</div></div>
     <button onclick="addSaved('${String(m.name).replace(/'/g,"\\'")}')">外す</button>
    </div>
    <div class="small" style="margin:4px 0 6px">${moveSuggestionsFor(m).length?`Champions習得技候補 ${moveSuggestionsFor(m).length}件`:'習得技候補は未取得・手入力可'}</div>
    <select class="savedItem" onchange="updateSavedRole(${i},this.value)">${savedRoleOptions.map(r=>`<option ${((m.customRole||m.role)===r)?'selected':''}>${r}</option>`).join('')}</select>
    ${savedItemInputHtml(m,i)}
    ${moves.map((mv,j)=>`<div class="moveRow" data-type="${esc(mv.type||'変化')}">
      <div class="moveSuggestWrap">
       <input value="${esc(mv.name||'')}" placeholder="技${j+1}" autocomplete="off" autocorrect="off" spellcheck="false"
        data-v201-i="${i}" data-v201-j="${j}"
        onfocus="showMoveSuggestions(this,${i},${j})"
        oninput="updateSavedMove(${i},${j},'name',this.value);showMoveSuggestions(this,${i},${j})"
        onblur="v201SavedMoveBlur(this,${i},${j})">
       <div class="moveSuggestBox"></div><div class="moveTypeBadge">${esc(mv.type||'変化')}</div>
      </div>
      <select onchange="updateSavedMove(${i},${j},'type',this.value)">${moveTypeOptions.map(t=>`<option ${mv.type===t?'selected':''}>${t}</option>`).join('')}</select>
     </div>`).join('')}
   </div>`;
 }).join('');
};
window.v201SavedMoveBlur=function(input,i,j){
 const mon=hydrateMon(i),name=String(input.value||'').trim();
 if(mon&&name&&duplicate(i,j,name)){
   mon.moves[j]={name:'',type:'変化'};persistMon(i);input.value='';try{v194Toast('同じポケモンに同じ技は2つ入れられません')}catch(e){}
 }
 try{hideMoveSuggestions(input)}catch(e){setTimeout(()=>input.closest('.moveSuggestWrap')?.querySelector('.moveSuggestBox')?.classList.remove('show'),120)}
};

// Re-adding a Pokemon restores its last remembered four moves when available.
if(typeof addSaved==='function'){
 const oldAddSaved=addSaved;
 addSaved=function(name){
   oldAddSaved(name);
   const i=(savedParty||[]).findIndex(x=>x?.name===name);
   if(i>=0){hydrateMon(i);renderSavedEditors();try{renderSavedCompletion()}catch(e){}}
 };
}

// Normalize all current images immediately after a re-render. Existing HTML already calls sprite(),
// and sprite() now always resolves to the same Showdown Gen5 pixel-art family.
try{renderSavedEditors();renderSavedRoster();renderBuildRoster();renderBuildCurrent();renderRoster();renderOppQuickGrid();renderEnvList()}catch(e){console.warn('v20.1 refresh',e)}

const testMon={name:'__v201test',moves:[{name:'シャドーボール',type:'ゴースト'}]};delete shadow[testMon.name];const test=canonicalMoves(testMon);delete shadow[testMon.name];writeShadow(shadow);
window.__V201_SELFTEST__={durable:test.length===4&&test[0].name==='シャドーボール',pixel:/play\.pokemonshowdown\.com\/sprites\/gen5\//.test(sprite(mons[0])),light:!!document.getElementById('v201-white-theme')};
document.documentElement.setAttribute('data-v201-selftest',Object.values(window.__V201_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close marker not found')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
