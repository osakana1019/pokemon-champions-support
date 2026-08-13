from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v19.1: stable saved move input + elite team synergy ===== */'
if marker in s:
    raise SystemExit(0)

s=s.replace('Pokémon Champions Support — v19.0','Pokémon Champions Support — v19.1')

patch=r'''
<style id="v191-style">
.v191EliteTag{font-size:9px;padding:3px 6px;border:1px solid #5b4c79;background:#211a31;border-radius:999px;color:#e0d2ff;font-weight:800}
.v191EliteBox{margin-top:7px;border-top:1px solid #29384e;padding-top:7px;font-size:9px;color:#aebed2;line-height:1.45}
.v191EliteBox b{color:#dac8ff}
</style>
<script>
/* ===== v19.1: stable saved move input + elite team synergy ===== */
(function(){
'use strict';

// ---- 1) Party registration: do not rebuild the whole editor on every keystroke. ----
let v191SavedCompletionTimer=0;
function v191SaveOnly(){try{localStorage.setItem('champ_saved_party',JSON.stringify(savedParty));}catch(e){}}
function v191ScheduleSavedCompletion(){
  clearTimeout(v191SavedCompletionTimer);
  v191SavedCompletionTimer=setTimeout(()=>{try{renderSavedCompletion();}catch(e){}},140);
}
updateSavedMove=function(i,j,key,v){
  const mon=savedParty[i];if(!mon)return;
  if(!Array.isArray(mon.moves))mon.moves=Array.from({length:4},()=>({name:'',type:'変化'}));
  while(mon.moves.length<4)mon.moves.push({name:'',type:'変化'});
  if(!mon.moves[j])mon.moves[j]={name:'',type:'変化'};
  mon.moves[j][key]=String(v??'');
  v191SaveOnly();
  // Critical: no renderSavedEditors() here. Rebuilding destroys focus after one character.
  v191ScheduleSavedCompletion();
};
function v191SavedIndexes(input){
  const editor=input.closest('.savedEditor'),root=document.getElementById('savedEditors');
  if(!editor||!root)return null;
  const i=[...root.children].indexOf(editor),row=input.closest('.moveRow');
  if(i<0||!row)return null;
  const j=[...editor.querySelectorAll('.moveRow')].indexOf(row);
  return j<0?null:{i,j,row};
}
function v191FinalizeSavedMove(input){
  const at=v191SavedIndexes(input);if(!at)return;
  const mon=savedParty[at.i],base=mons.find(m=>m.name===mon?.name)||mon;if(!mon||!base)return;
  const name=String(input.value||'').trim();
  mon.moves[at.j].name=name;
  let hit=null;
  try{hit=moveSuggestionsFor(base).find(x=>normalizeMoveSearch(x.name)===normalizeMoveSearch(name))||globalMoveDB.find(x=>normalizeMoveSearch(x.name)===normalizeMoveSearch(name));}catch(e){}
  if(hit){
    let type='変化';
    try{type=moveDisplayType(hit);}catch(e){type=hit.type||'変化';}
    mon.moves[at.j].type=type;
    at.row.dataset.type=type;
    const badge=at.row.querySelector('.moveTypeBadge');if(badge)badge.textContent=type;
    const sel=at.row.querySelector('select');if(sel&&[...sel.options].some(o=>o.value===type||o.textContent===type))sel.value=type;
  }
  v191SaveOnly();
  v191ScheduleSavedCompletion();
}
hideMoveSuggestions=function(input){
  v191FinalizeSavedMove(input);
  setTimeout(()=>{const box=input.closest('.moveSuggestWrap')?.querySelector('.moveSuggestBox');if(box)box.classList.remove('show');},120);
};

// ---- 2) Curated high-level public team results. ----
// These are compact factual team/achievement records from publicly posted player build articles.
// Newer seasons and stronger ladder results receive more weight. This stays a SMALL bonus;
// type matchups, role balance and actual Battle Data remain the primary recommendation score.
const V191_ELITE_BUILDS=[
  {
    id:'m4-starmie-2100',season:'M-4',achievement:'R2100・3桁到達',weight:1.35,
    team:['エレザード','スターミー','メガペンドラー','コノヨザル','ニンフィア','ガブリアス'],
    source:'t2.micro 公開構築記事'
  },
  {
    id:'m3-158-2432',season:'M-3',achievement:'最終158位・最高R2432',weight:1.85,
    team:['クエスパトラ','メガゲッコウガ','ミミッキュ','メガバシャーモ','ビビヨン','ブリジュラス'],
    source:'もちゃらてぃ 公開構築記事'
  },
  {
    id:'m3-831-2309',season:'M-3',achievement:'最終831位・R2309',weight:1.55,
    team:['メガドラミドロ','アーマーガア','ヒスイダイケンキ','メガフラエッテ','ヤバソチャ(ボンサクのすがた)','ラウドボーン'],
    source:'だいすけ 公開構築記事'
  },
  {
    id:'m3-866-2307',season:'M-3',achievement:'最終866位・R2307',weight:1.55,
    team:['メガエアームド','メガクチート','メタグロス','ヒスイヌメルゴン','ギルガルド(シールドフォルム)','ブリジュラス'],
    source:'しーく 公開構築記事'
  },
  {
    id:'m3-starmie-2175',season:'M-3',achievement:'最高R2175・瞬間3桁',weight:1.20,
    team:['エレザード','スターミー','メガバシャーモ','ウルガモス','メガミミロップ','ギャラドス'],
    source:'t2.micro 公開構築記事'
  },
  {
    id:'m3-facing-2100',season:'M-3',achievement:'R2100到達',weight:1.05,
    team:['メガムクホーク','メガライチュウY','カバルドン','ミミッキュ','ドリュウズ','アシレーヌ'],
    source:'shine_keio 公開構築記事'
  },
  {
    id:'m3-2104',season:'M-3',achievement:'最終R2104',weight:.72,
    team:['メガキラフロル','カバルドン','ギャラドス','メガバシャーモ','ミミッキュ','ウォッシュロトム'],
    source:'エギナ 公開構築記事'
  }
];
function v191Mon(name){return mons.find(m=>m.name===name)||null;}
function v191ContainsCandidate(build,c){
  return build.team.some(name=>{
    const m=v191Mon(name);if(!m)return name===c.name;
    // Mega evidence must stay Mega-specific. Do not use Mega results to justify the normal forme.
    if(m.mega||c.mega)return m.name===c.name;
    return sameSpecies(m,c);
  });
}
function v191ContainsCurrent(build,m){
  return build.team.some(name=>{const e=v191Mon(name);return e?sameSpecies(e,m):name===m.name;});
}
function v191EliteEvidence(c,team=buildTeam){
  let raw=0;const hits=[];
  for(const b of V191_ELITE_BUILDS){
    if(!v191ContainsCandidate(b,c))continue;
    const mates=team.filter(m=>v191ContainsCurrent(b,m));
    if(!mates.length)continue;
    const unique=[...new Map(mates.map(m=>[speciesKey(m),m])).values()];
    // Same elite team containing 2+ of the user's current members is much stronger evidence.
    const multiplier=unique.length>=3?1.65:unique.length===2?1.35:1;
    const score=b.weight*unique.length*multiplier;
    raw+=score;
    hits.push({build:b,mates:unique,score});
  }
  hits.sort((a,b)=>b.score-a.score);
  const bonus=Math.min(5.5,raw*1.15);
  return {raw,bonus,hits};
}
window.v191EliteEvidence=v191EliteEvidence;
window.V191_ELITE_BUILDS=V191_ELITE_BUILDS;

// Blend elite-player co-use into recommendation scoring, but cap it so matchup quality still wins.
if(typeof v12CandidateScore==='function'){
  const _v191CandidateScore=v12CandidateScore;
  v12CandidateScore=function(c,ctx){
    const x=_v191CandidateScore(c,ctx);if(!x)return x;
    try{
      const ev=v191EliteEvidence(c,buildTeam),add=ev.bonus;
      if(add<=0)return {...x,v191:ev};
      const top=ev.hits[0],mateNames=top.mates.slice(0,3).map(m=>m.name).join('・');
      const reason=`上位構築実績：${mateNames}と同居（${top.build.season} ${top.build.achievement}）`;
      const s=Math.min(100,Number(x.s||0)+add);
      return {...x,s,p:Math.round(s),r:[reason,...(x.r||[])].filter((v,i,a)=>a.indexOf(v)===i).slice(0,7),v191:ev};
    }catch(e){return x;}
  };
}

// Add a visible elite-result badge to recommendation cards.
if(typeof v12RenderBuildCandidates==='function'){
  const _v191RenderCandidates=v12RenderBuildCandidates;
  v12RenderBuildCandidates=function(scored,ctx,metaLoad){
    _v191RenderCandidates(scored,ctx,metaLoad);
    const cards=[...document.querySelectorAll('#buildSuggestions .v12BuildPick')];
    cards.forEach((card,i)=>{
      const ev=scored[i]?.v191;if(!ev?.hits?.length)return;
      const top=ev.hits[0],mate=top.mates.map(m=>m.name).join('・');
      let row=card.querySelector('.v19CandidateTags');
      if(!row){row=document.createElement('div');row.className='v19CandidateTags';const btn=card.querySelector('.buildAddBtn');if(btn)btn.insertAdjacentElement('beforebegin',row);else card.appendChild(row);}
      const tag=document.createElement('span');tag.className='v191EliteTag';tag.textContent=`上位勢実績 ${top.build.season}：${mate}と同居`;
      row.prepend(tag);
    });
  };
}

function v191BestEliteTeamMatches(){
  const out=[];
  for(const b of V191_ELITE_BUILDS){
    const matched=[];for(const m of buildTeam)if(v191ContainsCurrent(b,m))matched.push(m);
    const uniq=[...new Map(matched.map(m=>[speciesKey(m),m])).values()];
    if(!uniq.length)continue;
    const missing=b.team.filter(name=>{const em=v191Mon(name);return !buildTeam.some(m=>em?sameSpecies(em,m):m.name===name);});
    out.push({build:b,matched:uniq,missing,score:b.weight*uniq.length});
  }
  return out.sort((a,b)=>b.score-a.score||b.matched.length-a.matched.length).slice(0,3);
}
function v191AppendEliteSummary(){
  const card=document.getElementById('v19BuildIntel');if(!card)return;
  card.querySelector('.v191EliteBox')?.remove();
  const rows=v191BestEliteTeamMatches();if(!rows.length||!buildTeam.length)return;
  const box=document.createElement('div');box.className='v191EliteBox';
  box.innerHTML=`<b>上位プレイヤー構築との一致</b><br>`+rows.map(x=>{
    const used=x.matched.map(m=>m.name).join('・');
    const next=x.missing.slice(0,3).join('・');
    return `・${x.build.season} ${x.build.achievement}：${v19Esc? v19Esc(used):used}${next?` → 同居実績 ${v19Esc? v19Esc(next):next}`:''}`;
  }).join('<br>');
  card.appendChild(box);
}

// v19RenderBuildIntel is scoped inside v19, so observe the card and append our elite summary after re-renders.
const v191BuildRoot=document.getElementById('buildPage')||document.body;
new MutationObserver(()=>setTimeout(v191AppendEliteSummary,0)).observe(v191BuildRoot,{childList:true,subtree:true});
setTimeout(v191AppendEliteSummary,0);

window.__V191_SELFTEST__={
  stableInput:typeof updateSavedMove==='function',
  eliteData:V191_ELITE_BUILDS.length>=6,
  scorer:typeof v191EliteEvidence==='function',
  topResult:V191_ELITE_BUILDS.some(x=>/158位|831位|866位/.test(x.achievement))
};
document.documentElement.setAttribute('data-v191-selftest',Object.values(window.__V191_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close marker not found')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
