from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v19.4: unique moves + canonical Maushold + unified icons + Mega learnsets ===== */'
if marker in s:
    raise SystemExit(0)

s=s.replace('Pokémon Champions Support — v19.3','Pokémon Champions Support — v19.4')

patch=r'''
<style id="v194-style">
/* ===== v19.4: unified compact UI icons ===== */
.v194UiIcon{width:16px;height:16px;display:inline-block;vertical-align:-3px;flex:0 0 16px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.v194IconLabel{display:inline-flex;align-items:center;justify-content:center;gap:7px}
.appnav button .v194UiIcon{width:17px;height:17px;flex-basis:17px}
.v194Toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(12px);z-index:500;background:#111b2a;border:1px solid #4a607d;color:#f3f7fc;border-radius:10px;padding:9px 13px;font-size:12px;font-weight:800;box-shadow:0 10px 30px rgba(0,0,0,.35);opacity:0;pointer-events:none;transition:.16s ease;max-width:min(90vw,520px);text-align:center}
.v194Toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.v194Duplicate{border-color:#a95f6c!important;box-shadow:0 0 0 2px rgba(205,91,110,.12)!important}
</style>
<script>
/* ===== v19.4: unique moves + canonical Maushold + unified icons + Mega learnsets ===== */
(function(){
'use strict';
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const norm=s=>{try{return normalizeMoveSearch(s)}catch(e){return String(s||'').trim().toLowerCase()}};

// ---------- Small toast ----------
let toastTimer=0;
function toast(msg){
 let el=document.getElementById('v194Toast');
 if(!el){el=document.createElement('div');el.id='v194Toast';el.className='v194Toast';document.body.appendChild(el);}
 el.textContent=msg;el.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('show'),1800);
}
window.v194Toast=toast;

// ---------- Mega move suggestions inherit the pre-Mega learnset ----------
const _v194MoveSuggestionsFor=moveSuggestionsFor;
function v194PreMega(mon){
 if(!mon?.mega)return mon;
 let same=[];
 try{same=mons.filter(x=>!x.mega&&sameSpecies(x,mon));}catch(e){same=mons.filter(x=>!x.mega&&x.dex===mon.dex);}
 return same.sort((a,b)=>(Number(a.usageRank)||9999)-(Number(b.usageRank)||9999))[0]||mon;
}
function v194MergeMoves(...lists){
 const out=[],seen=new Set();
 for(const list of lists)for(const x of (list||[])){
  if(!x?.name)continue;const k=norm(x.name);if(!k||seen.has(k))continue;seen.add(k);out.push(x);
 }
 return out;
}
moveSuggestionsFor=function(mon){
 if(!mon)return [];
 if(!mon.mega)return _v194MoveSuggestionsFor(mon);
 const base=v194PreMega(mon);
 return v194MergeMoves(_v194MoveSuggestionsFor(base),_v194MoveSuggestionsFor(mon));
};
function v194UsageRows(mon){
 const rows=[];
 const add=m=>{try{rows.push(...(envData(m)?.moves||[]))}catch(e){}};
 if(mon?.mega)add(v194PreMega(mon));add(mon);
 const mp=new Map();
 for(const r of rows){
  const raw=String(Array.isArray(r)?r[0]:(r?.name??r?.label??''));
  const pct=parseFloat(String(Array.isArray(r)?r[1]:(r?.pct??r?.percentage_value??r?.percentage??0)).replace(/[%％,]/g,''))||0;
  let ja=raw;try{ja=displayEnvTerm('moves',raw)||raw}catch(e){}
  for(const n of [raw,ja]){const k=norm(n);if(k)mp.set(k,Math.max(mp.get(k)||0,pct));}
 }
 return mp;
}
window.moveUsagePctV1812=function(mon,name){return v194UsageRows(mon).get(norm(name))||0};
filterMoveSuggestions=function(mon,query){
 const q=norm(query||''),usage=v194UsageRows(mon);
 let list=moveSuggestionsFor(mon).map(x=>({...x,__usage:usage.get(norm(x.name))||0}));
 if(q)list=list.filter(x=>norm(x.name).includes(q));
 list.sort((a,b)=>{
  if(b.__usage!==a.__usage)return b.__usage-a.__usage;
  if(q){const aa=norm(a.name),bb=norm(b.name),ap=aa.startsWith(q)?0:1,bp=bb.startsWith(q)?0:1;if(ap!==bp)return ap-bp;}
  return a.name.localeCompare(b.name,'ja');
 });
 return list.slice(0,30);
};

// ---------- Never allow the same move twice in one Pokemon's four slots ----------
function savedDuplicate(i,j,name){
 const k=norm(name);if(!k)return false;const moves=savedParty[i]?.moves||[];
 return moves.some((x,idx)=>idx!==j&&norm(x?.name)===k);
}
function buildEntry(monName){return buildTeam.find(x=>x.name===monName)||null}
function ensureBuildMoves(entry){
 if(!entry)return [];
 if(!entry.set||typeof entry.set!=='object')entry.set={};
 if(!Array.isArray(entry.set.moves))entry.set.moves=[];
 while(entry.set.moves.length<4)entry.set.moves.push({name:'',type:''});
 return entry.set.moves;
}
function buildDuplicate(monName,index,name){
 const k=norm(name);if(!k)return false;const e=buildEntry(monName),moves=ensureBuildMoves(e);
 return moves.some((x,i)=>i!==index&&norm(x?.name)===k);
}
function persistSaved(){try{saveSavedParty()}catch(e){localStorage.setItem('champ_saved_party',JSON.stringify(savedParty))}}
function persistBuild(){localStorage.setItem('champ_build',JSON.stringify(buildTeam));try{V12_PROFILE_CACHE.clear()}catch(e){}}

// Saved-party suggestions hide moves already selected in the other three slots.
showMoveSuggestions=function(input,i,j){
 const wrap=input.closest('.moveSuggestWrap'),box=wrap?.querySelector('.moveSuggestBox'),mon=savedParty[i];if(!box||!mon)return;
 const used=new Set((mon.moves||[]).map((x,idx)=>idx===j?'':norm(x?.name)).filter(Boolean));
 const list=filterMoveSuggestions(mon,input.value).filter(x=>!used.has(norm(x.name))).slice(0,20);
 box.innerHTML=list.map(x=>{
  const pct=moveUsagePctV1812(mon,x.name),attr=esc(x.name);
  return `<div class="moveSuggestItem" data-v194-saved-move="${attr}"><span>${esc(x.name)}</span><span style="display:flex;align-items:center;gap:5px"><span class="moveKind ${moveDisplayType(x)==='変化'?'status':''}">${esc(moveDisplayType(x))}</span>${pct>0?`<span class="buildMovePct">${pct.toFixed(1)}%</span>`:''}</span></div>`;
 }).join('');
 box.classList.toggle('show',list.length>0);
 box.querySelectorAll('[data-v194-saved-move]').forEach(el=>el.onpointerdown=e=>{e.preventDefault();e.stopPropagation();chooseMoveSuggestion(i,j,el.dataset.v194SavedMove);});
};
chooseMoveSuggestion=function(i,j,name){
 const mon=savedParty[i];if(!mon)return;
 if(savedDuplicate(i,j,name)){toast('同じポケモンに同じ技は2つ入れられません');return;}
 const hit=moveSuggestionsFor(mon).find(x=>norm(x.name)===norm(name))||(typeof globalMoveDB!=='undefined'?globalMoveDB.find(x=>norm(x.name)===norm(name)):null);
 mon.moves[j].name=name;mon.moves[j].type=hit?moveDisplayType(hit):'変化';persistSaved();renderSavedEditors();try{renderSavedCompletion()}catch(e){}
};
const _v194HideSaved=hideMoveSuggestions;
hideMoveSuggestions=function(input){
 const editor=input.closest('.savedEditor'),root=document.getElementById('savedEditors'),row=input.closest('.moveRow');
 let bad=false;
 if(editor&&root&&row){
  const i=[...root.children].indexOf(editor),j=[...editor.querySelectorAll('.moveRow')].indexOf(row),name=String(input.value||'').trim();
  if(i>=0&&j>=0&&name&&savedDuplicate(i,j,name)){
    bad=true;input.classList.add('v194Duplicate');savedParty[i].moves[j]={name:'',type:'変化'};input.value='';persistSaved();toast('同じポケモンに同じ技は2つ入れられません');setTimeout(()=>input.classList.remove('v194Duplicate'),700);
  }
 }
 if(!bad){try{_v194HideSaved(input);return}catch(e){}}
 setTimeout(()=>input.closest('.moveSuggestWrap')?.querySelector('.moveSuggestBox')?.classList.remove('show'),120);
};

// Builder setter and suggestions also enforce uniqueness.
const _v194SetBuildMove=window.v1812SetBuildMove;
window.v1812SetBuildMove=function(monName,index,value){
 const name=String(value||'').trim();
 if(name&&buildDuplicate(monName,index,name)){toast('同じポケモンに同じ技は2つ入れられません');return false;}
 return _v194SetBuildMove(monName,index,value);
};
window.v1812ChooseBuildMove=function(monName,index,name){
 if(buildDuplicate(monName,index,name)){toast('同じポケモンに同じ技は2つ入れられません');return;}
 v1812SetBuildMove(monName,index,name);renderBuildCurrent();
};
window.v1812ShowBuildMoveSuggestions=function(input,monName,index){
 const entry=buildEntry(monName);if(!entry)return;const mon=mons.find(x=>x.name===monName)||entry,box=input.closest('.buildMoveSuggestWrap')?.querySelector('.buildMoveSuggestBox');if(!box)return;
 const moves=ensureBuildMoves(entry),used=new Set(moves.map((x,i)=>i===index?'':norm(x?.name)).filter(Boolean));
 const list=filterMoveSuggestions(mon,input.value).filter(x=>!used.has(norm(x.name))).slice(0,12);
 box.innerHTML=list.map(x=>{const pct=moveUsagePctV1812(mon,x.name),attr=esc(x.name);return `<div class="buildMoveSuggestItem" data-v194-build-move="${attr}"><span>${esc(x.name)}</span><span class="buildMoveSuggestMeta"><span>${esc(moveDisplayType(x))}</span>${pct>0?`<span class="buildMovePct">${pct.toFixed(1)}%</span>`:''}</span></div>`}).join('');
 box.classList.toggle('show',list.length>0);
 box.querySelectorAll('[data-v194-build-move]').forEach(el=>el.onpointerdown=e=>{e.preventDefault();e.stopPropagation();v1812ChooseBuildMove(monName,index,el.dataset.v194BuildMove);});
};
window.v1812HideBuildMoveSuggestions=function(input){
 const monName=input.dataset.buildMon,index=Number(input.dataset.buildMoveIndex),name=String(input.value||'').trim();
 if(name&&buildDuplicate(monName,index,name)){
  const entry=buildEntry(monName),moves=ensureBuildMoves(entry);moves[index]={name:'',type:''};persistBuild();input.value='';input.classList.add('v194Duplicate');toast('同じポケモンに同じ技は2つ入れられません');setTimeout(()=>input.classList.remove('v194Duplicate'),700);
 }
 setTimeout(()=>input.closest('.buildMoveSuggestWrap')?.querySelector('.buildMoveSuggestBox')?.classList.remove('show'),120);
};

// Remove duplicates already stored from older versions, keeping the first occurrence.
function cleanMoveArray(arr){const seen=new Set();let changed=false;for(let i=0;i<(arr||[]).length;i++){const k=norm(arr[i]?.name);if(!k)continue;if(seen.has(k)){arr[i]={name:'',type:'変化'};changed=true}else seen.add(k)}return changed}
let cleanedSaved=false;for(const m of savedParty||[])cleanedSaved=cleanMoveArray(m.moves)||cleanedSaved;if(cleanedSaved)persistSaved();
let cleanedBuild=false;for(const m of buildTeam||[]){if(m.set?.moves)cleanedBuild=cleanMoveArray(m.set.moves)||cleanedBuild}if(cleanedBuild)persistBuild();

// ---------- Maushold: show/recommend one canonical form only ----------
const mausholds=mons.filter(m=>/^イッカネズミ/.test(m.name));
const mausholdKeep=mausholds.find(m=>m.name==='イッカネズミ')||[...mausholds].sort((a,b)=>(Number(envData(a)?.rank||a.usageRank)||9999)-(Number(envData(b)?.rank||b.usageRank)||9999))[0]||null;
const hiddenMaushold=new Set(mausholds.filter(m=>m!==mausholdKeep).map(m=>m.name));
window.__V194_MAUSHOLD_KEEP__=mausholdKeep?.name||null;
if(typeof sortBrowseMons==='function'){
 const _v194SortBrowseMons=sortBrowseMons;
 sortBrowseMons=function(list,mode='dex'){return _v194SortBrowseMons((list||[]).filter(m=>!hiddenMaushold.has(m.name)),mode)};
}
if(typeof v14FormPolicy==='function'){
 const _v194FormPolicy=v14FormPolicy;
 v14FormPolicy=function(m){const x=_v194FormPolicy(m);return hiddenMaushold.has(m?.name)?{...x,hardExclude:true,evidence:0,reason:'イッカネズミはフォルム違いを1枠に統合'}:x};
}
if(typeof v14RecommendableForm==='function')v14RecommendableForm=function(m){return !v14FormPolicy(m).hardExclude};
// If an old saved/build team contains the hidden visual form, keep data but normalize it to the retained representative.
function normalizeMausholdIn(arr){if(!mausholdKeep)return false;let changed=false;for(let i=0;i<(arr||[]).length;i++){if(hiddenMaushold.has(arr[i]?.name)){const prev=arr[i],base={...mausholdKeep};arr[i]={...base,...prev,name:mausholdKeep.name,dex:mausholdKeep.dex,t1:mausholdKeep.t1,t2:mausholdKeep.t2};changed=true;}}return changed}
if(normalizeMausholdIn(savedParty)){persistSaved();try{renderSavedEditors();renderSavedRoster()}catch(e){}}
if(normalizeMausholdIn(buildTeam)){persistBuild();try{renderBuildCurrent();renderBuildRoster()}catch(e){}}

// ---------- Consistent monochrome line icons for primary app navigation/actions ----------
const ICON={
 home:'<svg class="v194UiIcon" viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10.5V20h13v-9.5"/><path d="M9.5 20v-6h5v6"/></svg>',
 quick:'<svg class="v194UiIcon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/><circle cx="12" cy="12" r="2"/></svg>',
 save:'<svg class="v194UiIcon" viewBox="0 0 24 24"><path d="M5 3h12l2 2v16H5z"/><path d="M8 3v6h8V3M8 16h8"/></svg>',
 build:'<svg class="v194UiIcon" viewBox="0 0 24 24"><circle cx="6" cy="7" r="2.5"/><circle cx="18" cy="7" r="2.5"/><circle cx="12" cy="17" r="2.5"/><path d="m8 8.5 2.5 6M16 8.5l-2.5 6M8.5 7h7"/></svg>',
 chart:'<svg class="v194UiIcon" viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
 search:'<svg class="v194UiIcon" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>',
 plus:'<svg class="v194UiIcon" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',
 trash:'<svg class="v194UiIcon" viewBox="0 0 24 24"><path d="M4 7h16M9 7V4h6v3M7 7l1 14h8l1-14"/></svg>',
 menu:'<svg class="v194UiIcon" viewBox="0 0 24 24"><path d="M5 7h14M5 12h14M5 17h14"/></svg>'
};
const rules=[
 [/ホーム/,'home'],[/クイック選出/,'quick'],[/パーティ登録/,'save'],[/パーティ構築/,'build'],[/環境データ/,'chart'],[/分析|解析/,'chart'],[/検索/,'search'],[/構築\＋|構築\+/,'plus'],[/登録\＋|登録\+/,'plus'],[/クリア|削除|全消し/,'trash']
];
function iconize(root=document){
 const els=root.querySelectorAll?root.querySelectorAll('.appnav button,button'):[];
 els.forEach(el=>{
  if(el.dataset.v194Iconized==='1')return;
  const text=el.textContent.replace(/[⌂⚡💾🧩📊🔎🔍➕＋🗑️🗑✕❌]/gu,'').trim();
  const hit=rules.find(([re])=>re.test(text));if(!hit)return;
  el.dataset.v194Iconized='1';el.innerHTML=`<span class="v194IconLabel">${ICON[hit[1]]}<span>${esc(text)}</span></span>`;
 });
 // Drag handles used a different glyph; make them use the same line-icon system.
 document.querySelectorAll('.dragHandle').forEach(el=>{if(el.dataset.v194Iconized==='1')return;const text=el.textContent.replace(/^☰\s*/,'').trim();el.dataset.v194Iconized='1';el.innerHTML=`<span class="v194IconLabel">${ICON.menu}<span>${esc(text)}</span></span>`;});
}
iconize();new MutationObserver(m=>{for(const x of m)for(const n of x.addedNodes)if(n.nodeType===1)iconize(n)}).observe(document.body,{childList:true,subtree:true});

// Refresh visible lists after form filtering.
try{renderRoster()}catch(e){}try{renderSavedRoster()}catch(e){}try{renderBuildRoster()}catch(e){}try{renderEnvList()}catch(e){}try{renderOppQuickGrid()}catch(e){}

window.__V194_SELFTEST__={
 uniqueSaved:typeof savedDuplicate==='function',
 uniqueBuild:typeof buildDuplicate==='function',
 megaBase:(()=>{const mg=mons.find(m=>m.name==='メガゲンガー'),g=mons.find(m=>m.name==='ゲンガー');if(!mg||!g)return true;const a=new Set(moveSuggestionsFor(mg).map(x=>norm(x.name))),b=moveSuggestionsFor(g).filter(x=>x.name).slice(0,8);return b.every(x=>a.has(norm(x.name)))})(),
 maushold:mausholds.length<2||hiddenMaushold.size===mausholds.length-1,
 icons:!!ICON.home
};
document.documentElement.setAttribute('data-v194-selftest',Object.values(window.__V194_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close marker not found')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
