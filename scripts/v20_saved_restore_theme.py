from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v20.0: saved move restore + obsidian teal theme ===== */'
if marker in s:
    raise SystemExit(0)

for old in [
    'Pokémon Champions Support — v19.4',
    'Pokémon Champions Support — v19.3',
]:
    s=s.replace(old,'Pokémon Champions Support — v20.0')

patch=r'''
<style id="v20-theme">
/* ===== v20.0: Obsidian Teal ===== */
:root{
  --bg:#06100f;
  --panel:#0c1716;
  --line:#24413e;
  --text:#f3fbf9;
  --muted:#8ca8a4;
  --accent:#35d6b5;
  --accent2:#14a69e;
  --v20-bg:#06100f;
  --v20-surface:#0b1514;
  --v20-surface2:#0f1d1b;
  --v20-surface3:#142623;
  --v20-line:#24413e;
  --v20-line2:#31534f;
  --v20-text:#f3fbf9;
  --v20-muted:#91aaa6;
  --v20-accent:#35d6b5;
  --v20-accent-strong:#14a69e;
  --v20-accent-soft:rgba(53,214,181,.12);
  --v20-danger:#ff8d94;
  --v20-warn:#f2bf68;
  --v20-mega:#e8b15f;
}
html{background:var(--v20-bg)}
body{
  background:
    radial-gradient(circle at 12% -8%,rgba(53,214,181,.10),transparent 31%),
    radial-gradient(circle at 90% 0%,rgba(20,166,158,.07),transparent 27%),
    linear-gradient(180deg,#081413 0%,#06100f 48%,#050c0b 100%);
  color:var(--v20-text);
}
.card,.teamPane,.savedEditor,.counterToolCard,.v19IntelCard{
  background:linear-gradient(180deg,rgba(13,25,23,.97),rgba(9,18,17,.98))!important;
  border-color:var(--v20-line)!important;
}
.card{box-shadow:0 12px 34px rgba(0,0,0,.22)}
.appnav{
  border-color:#294844!important;
  background:rgba(7,16,15,.90)!important;
  box-shadow:0 12px 32px rgba(0,0,0,.22)!important;
}
.appnav button{color:#8fa9a5!important}
.appnav button:hover{background:#10211f!important;color:#e7f7f3!important}
.appnav button.activeApp,.appnav .activeApp{
  background:linear-gradient(180deg,#173b35,#112e2a)!important;
  color:#f5fffc!important;
  box-shadow:inset 0 0 0 1px #39756b,0 5px 16px rgba(0,0,0,.18)!important;
}
button{background:#17312e!important;color:#eefaf7!important;box-shadow:inset 0 0 0 1px rgba(73,126,118,.44)!important}
button:hover{filter:none!important;background:#1d3d39!important}
button.primary,.primary,.activeApp,.mineAdd,.buildAddBtn{
  background:linear-gradient(135deg,#188f83,#27b497)!important;
  color:#f8fffd!important;
}
.oppAdd{background:#5a2a30!important}
.badge,.sourceBadge,.counterRecBadge,.v19Source{
  border-color:#31544f!important;background:#10211f!important;color:#aee6da!important;
}
input,select,textarea,.savedItem,.moveRow input,.moveRow select,.buildItemInput,.buildMoveInput,
.counterSuggestBoxV186,.moveSuggestBox,.buildMoveSuggestBox,.itemSuggestBox{
  background:#081312!important;
  border-color:#294944!important;
  color:#f2fbf8!important;
}
input:focus,select:focus,textarea:focus,.buildMoveInput:focus{
  outline:none!important;
  border-color:#39b9a2!important;
  box-shadow:0 0 0 3px rgba(53,214,181,.10)!important;
}
.mon,.sel,.rankRow,.oppQuickMon,.pick,.v12BuildPick,.metaRec,.v19Mini,.v19TeamSpeed,.variantChoice{
  background:#0b1715!important;
  border-color:#243f3b!important;
}
.mon:hover,.rankRow:hover,.oppQuickMon:hover,.variantChoice:hover,.moveSuggestItem:hover,.buildMoveSuggestItem:hover,.counterSuggestRowV186:hover{
  background:#11231f!important;
}
.compatPct,.quickPct,.completionScore,.metaScore,.rankNo,.counter,.buildMovePct,.spreadStat.active .spValue{
  color:#6fe4ca!important;
}
.compatBar,.bar,.spreadMiniBar,.envDbProgress{background:#18302d!important}
.compatBar>div,.bar>div,.spreadMiniBar>div,.envDbProgress>div,.envPctBar>div{
  background:linear-gradient(90deg,#1cae99,#59d9b9)!important;
}
.v19Chip,.v19Speed,.v19CandidateTag,.buildBreakdown span,.v12Breakdown span,.matchChip{
  background:#10201e!important;border-color:#2c4a46!important;color:#bfd4d0!important;
}
.v19Chip strong,.v19Speed strong{color:#72dfc6!important}
.metaAnalysisStatus,.buildMetaStatus{
  border-color:#2e5b53!important;background:#0e211e!important;color:#bcecdf!important;
}
.dragHandle,.tabletReorder button{background:#10211f!important;border-color:#2b4b46!important;color:#a7c4be!important}
.megaBadge{background:linear-gradient(135deg,#b87a31,#e0ae58)!important;color:#fffaf1!important}
.v193ExactHigh,.v192EvidenceHigh{border-color:#326b59!important;background:#10271f!important;color:#9be8c8!important}
.v193ExactLow,.v192EvidenceLow,.v194Duplicate{border-color:#714149!important;background:#2a171a!important;color:#ffc0c5!important}
.v19TrendUp{color:#72e4bd!important}.v19TrendDown{color:#ff9da5!important}
.small,.sub,.v19Muted,.formEvidence{color:var(--v20-muted)!important}
.moveTypeBadge{color:#a9c8c2!important}
::-webkit-scrollbar-thumb{background:#274844;border-radius:999px}
::-webkit-scrollbar-track{background:#091210}
::selection{background:rgba(53,214,181,.28);color:#fff}
</style>
<script>
/* ===== v20.0: saved move restore + obsidian teal theme ===== */
(function(){
'use strict';
const v20Norm=s=>String(s||'').normalize('NFKC').trim();
function v20MoveObj(x){
  if(typeof x==='string')return {name:v20Norm(x),type:'変化'};
  if(x&&typeof x==='object')return {name:v20Norm(x.name||''),type:v20Norm(x.type||'')||'変化'};
  return {name:'',type:'変化'};
}
function v20NormalizeSavedMoves(mon){
  if(!mon)return false;
  const direct=Array.isArray(mon.moves)?mon.moves:[];
  const legacy=Array.isArray(mon.set?.moves)?mon.set.moves:[];
  const out=[];
  let changed=!Array.isArray(mon.moves)||mon.moves.length!==4;
  for(let i=0;i<4;i++){
    const a=v20MoveObj(direct[i]);
    const b=v20MoveObj(legacy[i]);
    // Prefer the current saved-party field, but rescue older data from set.moves.
    const picked=a.name?a:(b.name?b:a);
    out.push(picked);
    const old=direct[i];
    const oldName=typeof old==='string'?v20Norm(old):v20Norm(old?.name||'');
    const oldType=typeof old==='object'?v20Norm(old?.type||''):'変化';
    if(oldName!==picked.name||(oldName&&oldType!==picked.type))changed=true;
  }
  mon.moves=out;
  return changed;
}
function v20RestoreAllSavedMoves(){
  let changed=false;
  for(const mon of (savedParty||[]))changed=v20NormalizeSavedMoves(mon)||changed;
  if(changed){try{localStorage.setItem('champ_saved_party',JSON.stringify(savedParty))}catch(e){}}
  return changed;
}
window.v20NormalizeSavedMoves=v20NormalizeSavedMoves;
window.v20RestoreAllSavedMoves=v20RestoreAllSavedMoves;

// The old renderer replaced every move with blanks unless moves.length was exactly 4.
// Normalize first so existing 1-3 saved moves survive and only missing slots are padded.
if(typeof renderSavedEditors==='function'){
  const _v20RenderSavedEditors=renderSavedEditors;
  renderSavedEditors=function(){v20RestoreAllSavedMoves();return _v20RenderSavedEditors.apply(this,arguments)};
}
if(typeof updateSavedMove==='function'){
  const _v20UpdateSavedMove=updateSavedMove;
  updateSavedMove=function(i,j,key,v){
    const mon=savedParty?.[i];if(mon)v20NormalizeSavedMoves(mon);
    return _v20UpdateSavedMove(i,j,key,v);
  };
}
if(typeof chooseMoveSuggestion==='function'){
  const _v20ChooseMoveSuggestion=chooseMoveSuggestion;
  chooseMoveSuggestion=function(i,j,name){
    const mon=savedParty?.[i];if(mon)v20NormalizeSavedMoves(mon);
    return _v20ChooseMoveSuggestion(i,j,name);
  };
}
if(typeof applyMoveSuggestion==='function'){
  const _v20ApplyMoveSuggestion=applyMoveSuggestion;
  applyMoveSuggestion=function(i,j,name){
    const mon=savedParty?.[i];if(mon)v20NormalizeSavedMoves(mon);
    return _v20ApplyMoveSuggestion(i,j,name);
  };
}

// Rescue data from the exact localStorage payload before the first visible render.
try{
  const raw=JSON.parse(localStorage.getItem('champ_saved_party')||'[]');
  if(Array.isArray(raw)){
    let changed=false;
    for(let i=0;i<Math.min(raw.length,savedParty.length);i++){
      const live=savedParty[i],disk=raw[i];if(!live||!disk)continue;
      const liveMoves=Array.isArray(live.moves)?live.moves:[];
      const diskMoves=Array.isArray(disk.moves)?disk.moves:(Array.isArray(disk.set?.moves)?disk.set.moves:[]);
      for(let j=0;j<4;j++){
        const l=v20MoveObj(liveMoves[j]),d=v20MoveObj(diskMoves[j]);
        if(!l.name&&d.name){if(!Array.isArray(live.moves))live.moves=[];live.moves[j]=d;changed=true;}
      }
    }
    if(changed)v20RestoreAllSavedMoves();
  }
}catch(e){console.warn('v20 saved restore',e)}
v20RestoreAllSavedMoves();
try{renderSavedEditors();renderSavedCompletion();}catch(e){}

// Non-destructive regression test: partial arrays must keep their existing names.
const fake={moves:[{name:'シャドーボール',type:'ゴースト'},{name:'ヘドロばくだん',type:'どく'}]};
v20NormalizeSavedMoves(fake);
window.__V20_SELFTEST__={
  partialPreserved:fake.moves.length===4&&fake.moves[0].name==='シャドーボール'&&fake.moves[1].name==='ヘドロばくだん',
  padded:fake.moves[2].name===''&&fake.moves[3].name==='',
  theme:!!document.getElementById('v20-theme')
};
document.documentElement.setAttribute('data-v20-selftest',Object.values(window.__V20_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close marker not found')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
