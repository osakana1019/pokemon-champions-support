from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v19.3: exact-form elite evidence ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v19.2','Pokémon Champions Support — v19.3')
patch=r'''
<style>
.v193ExactLow{font-size:9px;padding:3px 6px;border:1px solid #6a3944;background:#2c141a;border-radius:999px;color:#ffc0cb;font-weight:850}
.v193ExactHigh{font-size:9px;padding:3px 6px;border:1px solid #385b4a;background:#13261e;border-radius:999px;color:#a9e9c4;font-weight:850}
</style>
<script>
/* ===== v19.3: exact-form elite evidence ===== */
(function(){
'use strict';
const v193Norm=s=>String(s||'').normalize('NFKC').replace(/[\s　・･]/g,'').toLowerCase();
function v193ExactName(m){return v193Norm(m?.name||'');}
function v193BuildHasExact(b,m){
 const key=v193ExactName(m);if(!key)return false;
 return (b?.team||[]).some(n=>v193Norm(n)===key);
}
function v193ExactAppearances(c){
 const builds=Array.isArray(window.V191_ELITE_BUILDS)?window.V191_ELITE_BUILDS:[];
 let count=0,weighted=0,best=null;
 for(const b of builds){
   if(!v193BuildHasExact(b,c))continue;
   count++;weighted+=Number(b.weight)||1;
   if(!best||Number(b.weight)>Number(best.weight))best=b;
 }
 return {count,weighted,total:builds.length,best};
}
function v193ExactPairEvidence(c,team=buildTeam){
 const builds=Array.isArray(window.V191_ELITE_BUILDS)?window.V191_ELITE_BUILDS:[];
 let raw=0;const hits=[];
 for(const b of builds){
   if(!v193BuildHasExact(b,c))continue;
   const mates=team.filter(m=>v193BuildHasExact(b,m));
   if(!mates.length)continue;
   const uniq=[...new Map(mates.map(m=>[v193ExactName(m),m])).values()];
   const multiplier=uniq.length>=3?1.65:uniq.length===2?1.35:1;
   const score=(Number(b.weight)||1)*uniq.length*multiplier;
   raw+=score;hits.push({build:b,mates:uniq,score});
 }
 hits.sort((a,b)=>b.score-a.score);
 return {raw,bonus:Math.min(5.5,raw*1.15),hits};
}
function v193CorrectEvidence(c,x){
 const elite=v193ExactAppearances(c),pair=v193ExactPairEvidence(c),rank=Number(envData(c)?.rank||c.usageRank||999);
 const tier=x?.v192?.tier||null;
 let delta=0,cap=100;const reasons=[];
 // Exact-form adoption only. An alternate forme never inherits another forme's evidence.
 if(elite.count>=3){delta+=2.8;reasons.push(`上位構築でこの形態を${elite.count}件確認`);}
 else if(elite.count===2){delta+=1.8;reasons.push('上位構築でこの形態を複数確認');}
 else if(elite.count===1){delta+=.5;reasons.push('上位構築でこの形態の採用例あり');}
 else {
   // With no exact-form elite evidence, mediocre picks must not float upward only on neat typing.
   if(tier==='D'){delta-=12;cap=64;reasons.push('この形態の上位採用実績がなく、単体評価も低い');}
   else if(tier==='C'){delta-=10;cap=68;reasons.push('この形態の上位採用実績がほぼなく、優先度は低い');}
   else if(tier==='B'){delta-=8.5;cap=72;reasons.push('この形態の上位採用実績が薄く、補完だけでは優先しない');}
   else if(tier==='A'&&rank>45){delta-=4;cap=82;reasons.push('この形態の上位採用実績が薄い');}
   else if(rank>70){delta-=4.5;cap=80;reasons.push('この形態は上位採用・環境順位ともに低め');}
 }
 if(pair.bonus>0){
   delta+=pair.bonus;
   const top=pair.hits[0],names=top.mates.map(m=>m.name).join('・');
   reasons.unshift(`上位構築で${names}とこの形態が同居（${top.build.season} ${top.build.achievement}）`);
 }
 return {elite,pair,tier,rank,delta,cap,reasons};
}
window.v193ExactAppearances=v193ExactAppearances;
window.v193CorrectEvidence=v193CorrectEvidence;

// v19.1/v19.2 accidentally used sameSpecies(), so Wash Rotom evidence leaked into Heat Rotom.
// This final wrapper removes those old elite bonuses/deltas, then applies exact-form evidence once.
if(typeof v12CandidateScore==='function'){
 const _v193Candidate=v12CandidateScore;
 v12CandidateScore=function(c,ctx){
   const x=_v193Candidate(c,ctx);if(!x)return x;
   try{
     const wrongPair=Number(x?.v191?.bonus)||0;
     const wrongFreq=Number(x?.v192?.delta)||0;
     const ev=v193CorrectEvidence(c,x);
     let s=Number(x.s||0)-wrongPair-wrongFreq+ev.delta;
     s=Math.max(0,Math.min(ev.cap,s));
     const badPrefixes=['上位構築実績：','上位構築で複数回採用','上位構築で複数採用','上位構築実績が薄く','上位構築での採用根拠が薄い','上位実績・単体性能ともに','環境順位と上位採用の両方'];
     const old=(x.r||[]).filter(r=>!badPrefixes.some(p=>String(r).startsWith(p)));
     const reasons=[...ev.reasons,...old].filter((v,i,a)=>a.indexOf(v)===i).slice(0,7);
     return {...x,s,p:Math.round(s),r:reasons,v193:ev};
   }catch(e){console.warn('v19.3 exact-form evidence',e);return x;}
 };
}

// Clean misleading old badges and show exact-form evidence instead.
if(typeof v12RenderBuildCandidates==='function'){
 const _v193Render=v12RenderBuildCandidates;
 v12RenderBuildCandidates=function(scored,ctx,metaLoad){
   _v193Render(scored,ctx,metaLoad);
   const cards=[...document.querySelectorAll('#buildSuggestions .v12BuildPick')];
   cards.forEach((card,i)=>{
     card.querySelectorAll('.v191EliteTag,.v192EvidenceHigh,.v192EvidenceLow').forEach(el=>el.remove());
     const ev=scored[i]?.v193;if(!ev)return;
     let row=card.querySelector('.v19CandidateTags');
     if(!row){row=document.createElement('div');row.className='v19CandidateTags';const btn=card.querySelector('.buildAddBtn');if(btn)btn.insertAdjacentElement('beforebegin',row);else card.appendChild(row);}
     const t=document.createElement('span');
     if(ev.elite.count>=2){t.className='v193ExactHigh';t.textContent=`上位構築・この形態 ${ev.elite.count}件`;row.prepend(t);}
     else if(ev.elite.count===0&&ev.delta<0){t.className='v193ExactLow';t.textContent=`この形態の上位実績なし${ev.tier?' / '+ev.tier:''}`;row.prepend(t);}
   });
 };
}

const heat=mons.find(m=>m.name==='ヒートロトム'),wash=mons.find(m=>m.name==='ウォッシュロトム');
const heatN=heat?v193ExactAppearances(heat).count:null, washN=wash?v193ExactAppearances(wash).count:null;
window.__V193_SELFTEST__={
 exactFn:typeof v193ExactAppearances==='function',
 formsSeparate:!heat||!wash||v193ExactName(heat)!==v193ExactName(wash),
 washDoesNotLeak:!heat||!wash||!(v193BuildHasExact({team:['ウォッシュロトム']},heat)),
 washMatches:!wash||v193BuildHasExact({team:['ウォッシュロトム']},wash),
 heatCount:heatN,
 washCount:washN
};
document.documentElement.setAttribute('data-v193-selftest',window.__V193_SELFTEST__.formsSeparate&&window.__V193_SELFTEST__.washDoesNotLeak&&window.__V193_SELFTEST__.washMatches?'ok':'fail');
})();
</script>
'''
if '</body>' not in s: raise SystemExit('no body close')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
