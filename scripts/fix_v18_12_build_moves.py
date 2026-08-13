from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* ===== v18.12: build move editor + usage-sorted move suggestions ===== */'
if marker in s:
    raise SystemExit(0)

s = s.replace('Pokémon Champions Support — v18.11', 'Pokémon Champions Support — v18.12')

patch = r'''
<style>
/* ===== v18.12: compact build move editor ===== */
.buildMoveEditor{margin-top:7px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px}
.buildMoveSuggestWrap{position:relative;min-width:0}
.buildMoveInput{width:100%;min-width:0;background:#0b111b;color:#eef3fa;border:1px solid #33445d;border-radius:8px;padding:6px 7px;font-size:10px}
.buildMoveSuggestBox{position:absolute;left:0;right:0;top:calc(100% + 3px);z-index:90;max-height:170px;overflow:auto;background:#0b111b;border:1px solid #3a4d68;border-radius:9px;box-shadow:0 10px 24px rgba(0,0,0,.4);display:none;min-width:210px}
.buildMoveSuggestBox.show{display:block}
.buildMoveSuggestItem{display:flex;align-items:center;justify-content:space-between;gap:7px;padding:7px 8px;border-bottom:1px solid #1e2a3b;cursor:pointer;font-size:10px}
.buildMoveSuggestItem:last-child{border-bottom:0}
.buildMoveSuggestItem:hover{background:#172337}
.buildMoveSuggestMeta{display:flex;align-items:center;gap:5px;white-space:nowrap;color:#aebdd1;font-size:9px}
.buildMovePct{color:#9ec3ff;font-weight:900}
@media(max-width:700px){.buildMoveEditor{grid-template-columns:1fr}.buildMoveSuggestBox{min-width:180px}}
</style>
<script>
/* ===== v18.12: build move editor + usage-sorted move suggestions ===== */
(function(){
  function v1812Pct(row){
    if(!row)return 0;
    const raw=Array.isArray(row)?row[1]:(row.pct??row.percentage_value??row.percentage??0);
    const n=parseFloat(String(raw??'').replace(/[%％,]/g,'').trim());
    return Number.isFinite(n)?n:0;
  }
  function v1812MoveName(row){
    const raw=String(Array.isArray(row)?row[0]:(row?.name??row?.label??''));
    try{return displayEnvTerm('moves',raw)||raw;}catch(e){return raw;}
  }
  function v1812UsageMap(mon){
    const mp=new Map();
    const rows=(envData(mon)?.moves||[]).slice(0,40);
    for(const row of rows){
      const pct=v1812Pct(row), raw=String(Array.isArray(row)?row[0]:(row?.name??'')), ja=v1812MoveName(row);
      for(const key of [raw,ja]){
        const k=normalizeMoveSearch(key);
        if(k)mp.set(k,Math.max(mp.get(k)||0,pct));
      }
    }
    return mp;
  }
  window.moveUsagePctV1812=function(mon,name){
    return v1812UsageMap(mon).get(normalizeMoveSearch(name))||0;
  };

  // All move suggestion boxes: usage rate first. Search relevance only breaks ties.
  filterMoveSuggestions=function(mon,query){
    const q=normalizeMoveSearch(query||'');
    const usage=v1812UsageMap(mon);
    let list=moveSuggestionsFor(mon).map(x=>({...x,__usage:usage.get(normalizeMoveSearch(x.name))||0}));
    if(q)list=list.filter(x=>normalizeMoveSearch(x.name).includes(q));
    list.sort((a,b)=>{
      if(b.__usage!==a.__usage)return b.__usage-a.__usage;
      if(q){
        const aa=normalizeMoveSearch(a.name),bb=normalizeMoveSearch(b.name);
        const ap=aa.startsWith(q)?0:1,bp=bb.startsWith(q)?0:1;
        if(ap!==bp)return ap-bp;
      }
      return a.name.localeCompare(b.name,'ja');
    });
    return list.slice(0,30);
  };

  function v1812BuildEntry(name){return buildTeam.find(x=>x.name===name)||null;}
  function v1812EnsureMoves(entry){
    if(!entry)return [];
    if(!entry.set||typeof entry.set!=='object')entry.set={};
    const src=Array.isArray(entry.set.moves)?entry.set.moves:[];
    entry.set.moves=Array.from({length:4},(_,i)=>{
      const x=src[i];
      return x&&typeof x==='object'?{name:String(x.name||''),type:String(x.type||'')}:{name:'',type:''};
    });
    return entry.set.moves;
  }
  function v1812Persist(){
    localStorage.setItem('champ_build',JSON.stringify(buildTeam));
    try{V12_PROFILE_CACHE.clear();}catch(e){}
  }
  function v1812FindMove(mon,name){
    const key=normalizeMoveSearch(name);
    return moveSuggestionsFor(mon).find(x=>normalizeMoveSearch(x.name)===key)
      || (typeof globalMoveDB!=='undefined'?globalMoveDB.find(x=>normalizeMoveSearch(x.name)===key):null);
  }
  window.v1812SetBuildMove=function(monName,index,value){
    const entry=v1812BuildEntry(monName);if(!entry)return;
    const base=mons.find(x=>x.name===monName)||entry;
    const moves=v1812EnsureMoves(entry),name=String(value||'').trim(),hit=v1812FindMove(base,name);
    moves[index]={name,type:hit?moveDisplayType(hit):''};
    v1812Persist();
    try{renderTeamCompletion();}catch(e){}
  };
  window.v1812ChooseBuildMove=function(monName,index,name){
    v1812SetBuildMove(monName,index,name);
    renderBuildCurrent();
  };
  window.v1812ShowBuildMoveSuggestions=function(input,monName,index){
    const entry=v1812BuildEntry(monName);if(!entry)return;
    const mon=mons.find(x=>x.name===monName)||entry;
    const box=input.closest('.buildMoveSuggestWrap')?.querySelector('.buildMoveSuggestBox');if(!box)return;
    const list=filterMoveSuggestions(mon,input.value).slice(0,12);
    box.innerHTML=list.map(x=>{
      const pct=moveUsagePctV1812(mon,x.name),safe=String(x.name).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
      const attr=String(x.name).replace(/&/g,'&amp;').replace(/"/g,'&quot;');
      return `<div class="buildMoveSuggestItem" data-build-move-choice="${attr}"><span>${safe}</span><span class="buildMoveSuggestMeta"><span>${moveDisplayType(x)}</span>${pct>0?`<span class="buildMovePct">${pct.toFixed(1)}%</span>`:''}</span></div>`;
    }).join('');
    box.classList.toggle('show',list.length>0);
    box.querySelectorAll('[data-build-move-choice]').forEach(el=>{
      el.onpointerdown=e=>{e.preventDefault();e.stopPropagation();v1812ChooseBuildMove(monName,index,el.dataset.buildMoveChoice);};
    });
  };
  window.v1812HideBuildMoveSuggestions=function(input){
    setTimeout(()=>input.closest('.buildMoveSuggestWrap')?.querySelector('.buildMoveSuggestBox')?.classList.remove('show'),120);
  };
  function v1812BuildMoveHtml(m){
    const entry=v1812BuildEntry(m.name)||m,moves=v1812EnsureMoves(entry);
    return `<div class="buildMoveEditor">${moves.map((mv,i)=>{
      const val=String(mv?.name||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;');
      const monAttr=String(m.name).replace(/&/g,'&amp;').replace(/"/g,'&quot;');
      return `<div class="buildMoveSuggestWrap"><input class="buildMoveInput" value="${val}" placeholder="技${i+1}" autocomplete="off" data-build-mon="${monAttr}" data-build-move-index="${i}" onclick="event.stopPropagation()" onpointerdown="event.stopPropagation()" onfocus="v1812ShowBuildMoveSuggestions(this,this.dataset.buildMon,Number(this.dataset.buildMoveIndex))" oninput="v1812ShowBuildMoveSuggestions(this,this.dataset.buildMon,Number(this.dataset.buildMoveIndex))" onblur="v1812HideBuildMoveSuggestions(this)" onchange="v1812SetBuildMove(this.dataset.buildMon,Number(this.dataset.buildMoveIndex),this.value)"><div class="buildMoveSuggestBox"></div></div>`;
    }).join('')}</div>`;
  }

  // Restore the 4 move fields inside every build slot.
  renderBuildCurrent=function(){
    if(!buildCurrent)return;
    buildCurrent.innerHTML=Array.from({length:6},(_,i)=>{
      const m=buildTeam[i];
      if(!m)return `<div class="sel"><div class="empty">${i+1}</div></div>`;
      const item=m.mega?megaStoneFor(m):(buildItems[m.name]||'');
      if(m.mega&&buildItems[m.name]!==item){buildItems[m.name]=item;localStorage.setItem('champ_build_items',JSON.stringify(buildItems));}
      v1812EnsureMoves(m);
      return `<div class="buildSlot" data-build-index="${i}">
        <div class="dragHandle" onpointerdown="buildPointerDown(event,${i})" onpointermove="buildPointerMove(event)" onpointerup="buildPointerUp(event)" onpointercancel="buildPointerUp(event)">☰ 長押し/ドラッグで移動</div>
        <div class="tabletReorder"><button type="button" onclick="event.stopPropagation();moveBuildSlot(${i},-1)" aria-label="左へ移動">←</button><span>並び替え</span><button type="button" onclick="event.stopPropagation();moveBuildSlot(${i},1)" aria-label="右へ移動">→</button></div>
        <div class="sel" onclick="addBuild('${m.name.replace(/'/g,"\\'")}')"><img src="${sprite(m)}" onerror="if(!this.dataset.fallback){this.dataset.fallback='1';this.src='${fallback(m)}'}else{this.onerror=null}"><div class="name">${m.name}</div></div>
        ${buildItemInputHtml(m,item)}
        ${v1812BuildMoveHtml(m)}
      </div>`;
    }).join('');
    v1812Persist();
  };

  // Existing evaluation helpers that already read mon.set.moves now receive the custom build moves.
  try{renderBuildCurrent();}catch(e){console.error('v18.12 build move editor',e);}
  window.__V1812_SELFTEST__={filter:typeof filterMoveSuggestions==='function',editor:typeof v1812SetBuildMove==='function'};
  document.documentElement.setAttribute('data-v1812-selftest',Object.values(window.__V1812_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close marker not found')
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
