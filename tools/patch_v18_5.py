from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* ===== v18.5: defensive counter stability ===== */'
if marker in s:
    print('v18.5 already applied')
    raise SystemExit(0)

s = s.replace('Pokémon Champions Support — v18.4', 'Pokémon Champions Support — v18.5')
s = s.replace('content="Pokémon Champions Support — v18.4"', 'content="Pokémon Champions Support — v18.5"')

patch = r'''

/* ===== v18.5: defensive counter stability ===== */
function v185TopIncomingMoveRisk(candidate, threat){
 const tp=v12Profile(threat);let best={rate:0,mult:1,name:'',type:'',value:0};
 for(const r of (tp?.moves||[])){
  const info=apiMoveInfo(r.name),type=info?.type||envMoveType(threat.name,r.name)||'';
  if(!type||info?.category==='status')continue;
  const rate=v12Pct(r),multv=dmg(candidate,type);
  const value=(rate||8)*Math.max(.2,multv);
  if(value>best.value)best={rate,mult:multv,name:displayEnvTerm('moves',r.name)||r.name,type,value};
 }
 return best;
}
function v185CounterStability(m,threat,base){
 const p=base.profile||v12Profile(m),match=base.match||v12MemberVsThreat(m,threat);
 const threatStabs=[threat.t1,threat.t2].filter(t=>t&&t!=='なし');
 const ownStabs=[m.t1,m.t2].filter(t=>t&&t!=='なし');
 const incomingStab=Math.max(...threatStabs.map(t=>dmg(m,t)),1);
 const outgoingStab=Math.max(...ownStabs.map(t=>dmg(threat,t)),1);
 const topRisk=v185TopIncomingMoveRisk(m,threat);
 const reciprocal=incomingStab>1&&outgoingStab>1;
 const bulk=Number(p?.bulk)||bulkIndex(m);
 const fast=match.speed>=.75;
 const sturdy=match.def>=.72;
 let delta=0,cap=98;const reasons=[];

 // Defensive typing is a first-class part of a counter: resist/immunity > merely hitting super effectively.
 if(incomingStab===0){delta+=16;reasons.push('相手の一致技をタイプで無効化できる');}
 else if(incomingStab<=.5){delta+=10;reasons.push('相手の一致技を半減以下にできる');}
 else if(incomingStab<1){delta+=6;reasons.push('相手の一致技を軽減できる');}
 else if(incomingStab>=4){delta-=22;cap=Math.min(cap,55);reasons.push('相手の一致技が4倍弱点で対面が不安定');}
 else if(incomingStab>1){delta-=11;cap=Math.min(cap,70);reasons.push('相手の一致技を弱点で受ける');}

 // Paper counter check: both sides hitting each other super-effectively is not a stable answer by itself.
 if(reciprocal){
  if(fast&&sturdy){delta-=4;reasons.push('相互弱点だが速度・耐久である程度補える');}
  else if(fast||sturdy){delta-=9;cap=Math.min(cap,70);reasons.push('相互弱点で安定した受け出しはしにくい');}
  else {delta-=17;cap=Math.min(cap,60);reasons.push('相互弱点で先に崩されやすく、対策として不安定');}
 }

 // Use the opponent's actual high-usage attacks, not only its listed types.
 if(topRisk.rate>=15&&topRisk.mult>1){
  const pen=topRisk.mult>=4?16:topRisk.rate>=40?12:8;
  delta-=pen;cap=Math.min(cap,topRisk.mult>=4?52:66);
  reasons.push(`${topRisk.name}（採用率${Math.round(topRisk.rate)}%）を弱点で受ける`);
 }else if(topRisk.rate>=20&&topRisk.mult<1){
  delta+=5;reasons.push(`主要技の${topRisk.name}を半減以下にできる`);
 }

 // Raw bulk matters after typing. High bulk can rescue neutral matchups, but not severe weaknesses.
 if(bulk>=110&&incomingStab<=1){delta+=5;reasons.push('耐久も高く繰り返し対面しやすい');}
 else if(bulk>=95&&incomingStab<1){delta+=3;}
 if(bulk<78&&incomingStab>1){delta-=6;cap=Math.min(cap,58);reasons.push('弱点を受けるうえ耐久も低め');}

 // Matchup engine already knows actual move pressure. Make poor defensive scores a hard ceiling.
 if(match.def<.38){delta-=10;cap=Math.min(cap,52);reasons.push('実際の採用技まで含めると受けが成立しにくい');}
 else if(match.def<.5){delta-=6;cap=Math.min(cap,60);}
 else if(match.def>=.82&&incomingStab<=1){delta+=5;reasons.push('実際の上位採用技にも安定しやすい');}

 // Mimikyu: a Ghost-weak candidate must not rank highly just because Ghost also hits Mimikyu.
 if(threat.name==='ミミッキュ'&&dmg(m,'ゴースト')>1){
  const tact=base.tactical||null;
  const bypass=!!(tact?.directBypass)||(tact?.priority?.rate>=12&&tact?.priority?.eff>1);
  if(!bypass){delta-=10;cap=Math.min(cap,56);reasons.push('ばけのかわ後のゴースト打点・かげうちまで考えると不安定');}
 }
 return {delta,cap,reasons:[...new Set(reasons)],incomingStab,outgoingStab,topRisk,bulk,reciprocal};
}

const _v185CounterScore=v14CounterScore;
v14CounterScore=function(m,threat){
 const base=_v185CounterScore(m,threat);if(!base)return null;
 const stable=v185CounterStability(m,threat,base);
 const score=Math.max(0,base.score+stable.delta);
 const pct=Math.min(stable.cap,Math.round(v12Clamp(score,30,98)));
 return {
  ...base,score,pct,stability:stable,
  reasons:[...new Set([...stable.reasons,...(base.reasons||[])])].slice(0,5)
 };
};

function runV185SelfTests(){
 const tests=[],ok=(n,c)=>tests.push([n,!!c]);
 const mimi=mons.find(m=>m.name==='ミミッキュ'),ghold=mons.find(m=>m.name==='サーフゴー');
 if(mimi&&ghold){
  const b=_v185CounterScore(ghold,mimi),st=b&&v185CounterStability(ghold,mimi,b);
  ok('Gholdengo takes Ghost super effectively',dmg(ghold,'ゴースト')>1);
  ok('reciprocal Ghost matchup recognized',!!st?.reciprocal);
  ok('unstable Mimikyu answer capped',Number(st?.cap)<=60);
 }else{ok('Mimikyu and Gholdengo exist',false);ok('reciprocal Ghost matchup recognized',false);ok('unstable Mimikyu answer capped',false);}
 const ghost=mons.find(m=>m.t1==='ゴースト'||m.t2==='ゴースト');
 ok('defensive type engine available',!!ghost&&typeof dmg==='function');
 const passed=tests.filter(x=>x[1]).length;
 window.__V185_SELFTEST__={passed,total:tests.length,tests};
 document.documentElement.setAttribute('data-v185-selftest',`${passed===tests.length?'ok':'fail'}-${passed}/${tests.length}`);
 if(passed!==tests.length)console.error('v18.5 self-test failed',tests);
 return window.__V185_SELFTEST__;
}
runV185SelfTests();
'''

needle='</script></body></html>'
if needle not in s:
    raise SystemExit('closing script marker not found')
s=s.replace(needle,patch+'\n'+needle,1)
p.write_text(s,encoding='utf-8')
print('patched v18.5')
