from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

patch=r'''

/* ===== v18.4: tactical counter reliability + universal kana search ===== */
function v184NormalizeSearch(v){
 return kataToHira(String(v||'').toLowerCase())
  .normalize('NFD').replace(/[\u3099\u309A]/g,'')
  .replace(/[・･\s\u3000ー\-‐‑‒–—―_()（）\[\]{}]/g,'')
  .replace(/[ぁぃぅぇぉっゃゅょゎ]/g,m=>({
   'ぁ':'あ','ぃ':'い','ぅ':'う','ぇ':'え','ぉ':'お','っ':'つ','ゃ':'や','ゅ':'ゆ','ょ':'よ','ゎ':'わ'
  }[m]||m));
}
// Use one normalization rule everywhere: Pokemon, moves, held items, and the counter finder.
normalizePokemonSearch=v184NormalizeSearch;
normalizeMoveSearch=v184NormalizeSearch;
normalizeHeldItemSearch=v184NormalizeSearch;
v14NormalizeCounterText=v184NormalizeSearch;

function v184EscAttr(v){return String(v||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;');}
renderCounterDatalist=function(){
 const dl=document.getElementById('counterPokemonOptions');if(!dl)return;
 dl.innerHTML=sortBrowseMons(mons,'usage').map(m=>{
  const canonical=v184EscAttr(m.name),hira=v184EscAttr(kataToHira(m.name));
  return `<option value="${canonical}"></option>${hira!==canonical?`<option value="${hira}" label="${canonical}"></option>`:''}`;
 }).join('');
};
renderCounterDatalist();

const V184_MULTI_JA=new Set(['タネマシンガン','つららばり','ロックブラスト','ミサイルばり','スケイルショット','ダブルウイング','トリプルアクセル','みずしゅりけん','ネズミざん']);
const V184_MULTI_RAW=new Set(['bulletseed','iciclespear','rockblast','pinmissile','scaleshot','dualwingbeat','tripleaxel','watershuriken','populationbomb']);
const V184_BURN_JA=new Set(['おにび']);
const V184_BURN_RAW=new Set(['willowisp']);

function v184BestMoveTrait(profile,threat,jaSet,rawSet){
 let best={rate:0,eff:0,name:'',type:''};
 for(const r of (profile?.moves||[])){
  const ja=displayEnvTerm('moves',r.name),raw=normalizedDataId(r.name);
  if(!jaSet.has(ja)&&!rawSet.has(raw))continue;
  const type=apiMoveInfo(r.name)?.type||envMoveType(profile.mon?.name||'',r.name)||'';
  const eff=type?dmg(threat,type):1,rate=v12Pct(r);
  const value=rate*(eff>1?1.3:eff>0?1:0);
  const old=best.rate*(best.eff>1?1.3:best.eff>0?1:0);
  if(value>old)best={rate,eff,name:ja||r.name,type};
 }
 return best;
}
function v184PriorityThreat(candidate,threat,tp){
 let best={rate:0,mult:1,name:''};
 for(const r of (tp?.moves||[])){
  const ja=displayEnvTerm('moves',r.name),raw=normalizedDataId(r.name);
  if(!V12_PRIORITY_MOVES.has(ja)&&!V12_RAW_MOVE_GROUPS.priority.has(raw))continue;
  const type=apiMoveInfo(r.name)?.type||envMoveType(threat.name,r.name)||'';
  const multv=type?dmg(candidate,type):1,rate=v12Pct(r);
  if(rate*Math.max(1,multv)>best.rate*Math.max(1,best.mult))best={rate,mult:multv,name:ja||r.name};
 }
 const mimikyuSneak=threat.name==='ミミッキュ'&&dmg(candidate,'ゴースト')>1;
 return {...best,weak:(best.rate>=12&&best.mult>1)||mimikyuSneak,mimikyuSneak};
}
function v184CounterTactics(m,threat,base){
 const p=base.profile||v12Profile(m),tp=v12Profile(threat),match=base.match||v12MemberVsThreat(m,threat);
 const disguisePct=threat.name==='ミミッキュ'?100:v12TopAbilityPct(tp,['disguise'],['ばけのかわ']);
 const isDisguise=disguisePct>=40;
 const mold=Math.max(
  v12TopAbilityPct(p,['moldbreaker'],['かたやぶり']),
  v12TopAbilityPct(p,['teravolt'],['テラボルテージ']),
  v12TopAbilityPct(p,['turboblaze'],['ターボブレイズ'])
 );
 const multi=v184BestMoveTrait(p,threat,V184_MULTI_JA,V184_MULTI_RAW);
 const priority=v184BestMoveTrait(p,threat,V12_PRIORITY_MOVES,V12_RAW_MOVE_GROUPS.priority);
 const burn=v184BestMoveTrait(p,threat,V184_BURN_JA,V184_BURN_RAW);
 const incomingPriority=v184PriorityThreat(m,threat,tp);
 const directBypass=mold>=15||(multi.rate>=12&&multi.eff>0);
 let delta=0;const reasons=[];

 if(isDisguise){
  if(mold>=15){delta+=18;reasons.push('かたやぶり系で「ばけのかわ」を無視できる');}
  if(multi.rate>=12&&multi.eff>0){delta+=multi.eff>1?16:12;reasons.push(`${multi.name}など連続技で皮を剥がしながら削れる`);}
  if(priority.rate>=12&&priority.eff>1&&match.def>=.55){delta+=12;reasons.push(`${priority.name}の先制弱点技で詰めやすい`);}
  if((p.pivot||0)>=20&&buildTeam.length>=2){delta+=4;reasons.push('交代技で皮を剥がして後続へつなげやすい');}
  if(burn.rate>=15){delta+=5;reasons.push('やけどで物理火力を落とせる');}

  if(!directBypass&&match.eff>=1.7){
   delta-=10;reasons.push('弱点を突けても「ばけのかわ」で最初の一撃を止められる');
  }
  if(incomingPriority.weak){
   const ownPriorityAnswer=priority.rate>=12&&priority.eff>1;
   if(ownPriorityAnswer&&match.def>=.55){delta-=4;}
   else if(match.def<.58){delta-=22;}
   else if(match.def<.72){delta-=15;}
   else delta-=8;
   reasons.push(incomingPriority.mimikyuSneak?'「かげうち」が弱点になり対面が不安定':`${incomingPriority.name||'先制技'}が弱点になりやすい`);
  }
  if(!directBypass&&match.def<.48){delta-=8;reasons.push('皮を剥がした後の打ち合いで耐久が足りにくい');}
 }

 // Counter recommendations should value repeatable answers over a paper type advantage.
 if(match.def>=.82&&match.eff>=.95){delta+=5;reasons.push('受けと打点の両方が安定している');}
 if(match.def<.38&&match.speed<.6){delta-=7;reasons.push('対面から安定して行動しにくい');}
 return {delta,reasons:[...new Set(reasons)],isDisguise,directBypass,incomingPriority,multi,priority,mold};
}

const _v184CounterScore=v14CounterScore;
v14CounterScore=function(m,threat){
 const base=_v184CounterScore(m,threat);if(!base)return null;
 const tactical=v184CounterTactics(m,threat,base);
 const score=Math.max(0,base.score+tactical.delta);
 return {
  ...base,
  score,
  pct:Math.round(v12Clamp(score,35,98)),
  reasons:[...new Set([...tactical.reasons,...(base.reasons||[])])].slice(0,4),
  tactical
 };
};

function runV184SelfTests(){
 const tests=[],ok=(n,c)=>tests.push([n,!!c]);
 ok('pokemon kana search',v184NormalizeSearch('ミミッキュ')===v184NormalizeSearch('みみっきゅ'));
 ok('move kana search',v184NormalizeSearch('シャドーボール')===v184NormalizeSearch('しゃどーぼーる'));
 ok('item kana search',v184NormalizeSearch('オボンのみ')===v184NormalizeSearch('おぼんのみ'));
 const mimi=mons.find(m=>m.name==='ミミッキュ'),ghold=mons.find(m=>m.name==='サーフゴー');
 if(mimi&&ghold){
  const fake={profile:v12Profile(ghold),match:v12MemberVsThreat(ghold,mimi)};
  const t=v184CounterTactics(ghold,mimi,fake);
  ok('Mimikyu recognizes Disguise',t.isDisguise===true);
  ok('Ghost-weak candidate gets priority risk',t.incomingPriority.weak===true);
 }else{
  ok('Mimikyu sample exists',!!mimi);ok('Gholdengo sample exists',!!ghold);
 }
 const passed=tests.filter(x=>x[1]).length;
 window.__V184_SELFTEST__={passed,total:tests.length,tests};
 document.documentElement.setAttribute('data-v184-selftest',`${passed===tests.length?'ok':'fail'}-${passed}/${tests.length}`);
 if(passed!==tests.length)console.error('v18.4 self-test failed',tests);
 return window.__V184_SELFTEST__;
}
runV184SelfTests();
'''

marker='</script></body></html>'
assert marker in s, 'closing script marker not found'
if 'v18.4: tactical counter reliability + universal kana search' not in s:
    s=s.replace(marker,patch+'\n'+marker,1)

s=s.replace('v18.3','v18.4')
p.write_text(s,encoding='utf-8')
print('patched tactical counter + universal kana search')
