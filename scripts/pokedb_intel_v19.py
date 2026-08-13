from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v19.0: PokeDB-inspired live battle intelligence ===== */'
if marker in s:
    raise SystemExit(0)

s=s.replace('Pokémon Champions Support — v18.13','Pokémon Champions Support — v19.0')
s=s.replace('Pokémon Champions Support — v18.12','Pokémon Champions Support — v19.0')

patch=r'''
<style id="v19-intel-style">
.v19IntelCard{margin-top:10px;border:1px solid #33445f;border-radius:14px;background:#0b121d;padding:11px}
.v19IntelHead{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.v19IntelHead b{font-size:13px}.v19Source{font-size:9px;color:#91a5c1;border:1px solid #30435f;border-radius:999px;padding:3px 7px}
.v19ChipRow{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0}.v19Chip{border:1px solid #32465f;background:#111d2d;border-radius:999px;padding:4px 7px;font-size:9px;color:#c8d6e9}.v19Chip strong{color:#a9c9ff}
.v19TrendUp{color:#7de6ac}.v19TrendDown{color:#ff9aab}.v19TrendFlat{color:#9eacc0}
.v19Grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-top:8px}.v19Mini{border:1px solid #27374d;background:#0e1724;border-radius:10px;padding:8px;font-size:10px;line-height:1.5;min-width:0}.v19Mini b{font-size:10px;color:#dce8f7}.v19Muted{color:#8191a8}
.v19Btns{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.v19Btns button{font-size:10px;padding:7px 9px}.v19PokeDbBtn{background:#28496f}.v19DataBtn{background:#263750}
.v19SpeedList{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}.v19Speed{font-size:9px;border-radius:7px;background:#142034;border:1px solid #31445f;padding:3px 6px}.v19Speed strong{color:#a9c9ff}
.v19BuildIntel{margin:8px 0 2px}.v19TeamSpeeds{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px}.v19TeamSpeed{border:1px solid #2c3c52;background:#101927;border-radius:9px;padding:6px;font-size:9px;overflow:hidden}.v19TeamSpeed b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:10px}
.v19CandidateTags{display:flex;gap:4px;flex-wrap:wrap;margin:7px 0}.v19CandidateTag{font-size:9px;padding:3px 6px;border:1px solid #344966;background:#122036;border-radius:999px;color:#c5d5e9}
.v19DailyLine{display:grid;grid-template-columns:1fr auto;gap:8px;border-top:1px solid #26364c;padding-top:5px;margin-top:5px}.v19DailyDelta.up{color:#7de6ac}.v19DailyDelta.down{color:#ff9aab}
@media(max-width:850px){.v19Grid{grid-template-columns:1fr}.v19TeamSpeeds{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
<script>
/* ===== v19.0: PokeDB-inspired live battle intelligence ===== */
(function(){
'use strict';
const V19_API='https://championsbattledata.com';
const V19_POKEDB='https://champs.pokedb.tokyo';
const V19_FMT='Singles';
const V19_DAY=24*60*60*1000;
const v19Norm=s=>String(s||'').normalize('NFKC').toLowerCase().replace(/[\s　・･_\-‐‑‒–—―'’"“”`´.。,，:：;；/\\()（）\[\]{}]/g,'');
const v19Esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const v19Num=v=>{const n=parseFloat(String(v??'').replace(/[%％,]/g,'').trim());return Number.isFinite(n)?n:0};
function v19Pct(row){return v19Num(Array.isArray(row)?row[1]:(row?.pct??row?.percentage_value??row?.percentage??0));}
function v19RawName(row){return String(Array.isArray(row)?row[0]:(row?.name??row?.label??''));}
function v19Name(cat,row){const raw=v19RawName(row);try{return displayEnvTerm(cat,raw)||raw}catch(e){return raw}}
function v19Rows(mon,key,cat=key){
 const d=envData(mon)||{},rows=Array.isArray(d[key])?d[key]:[];
 return rows.map((row,i)=>({raw:v19RawName(row),name:v19Name(cat,row),pct:v19Pct(row),rank:Number(row?.rank)||i+1,row})).filter(x=>x.name).sort((a,b)=>(b.pct-a.pct)||(a.rank-b.rank));
}
function v19BaseStats(m){
 const b=m?.baseStats||{};if(Number.isFinite(Number(b.spe)))return b;
 try{return getBulkStats(m)||{}}catch(e){return {}}
}
const V19_SPEED_UP=new Set(['jolly','timid','hasty','naive','ようき','おくびょう','せっかち','むじゃき']);
const V19_SPEED_DOWN=new Set(['brave','relaxed','quiet','sassy','ゆうかん','のんき','れいせい','なまいき']);
function v19NatureMul(name){const k=v19Norm(name);for(const x of V19_SPEED_UP)if(k===v19Norm(x))return 1.1;for(const x of V19_SPEED_DOWN)if(k===v19Norm(x))return .9;return 1;}
function v19SpreadPoints(name){
 const s=String(name||'');let nums=[];
 const labelled={hp:null,atk:null,def:null,spa:null,spd:null,spe:null};
 const aliases={hp:['hp','h'],atk:['atk','attack','a','こうげき'],def:['def','defense','b','ぼうぎょ'],spa:['spa','spatk','c','とくこう'],spd:['spd','spdef','d','とくぼう'],spe:['spe','speed','s','すばやさ']};
 for(const [k,arr] of Object.entries(aliases)){
   for(const a of arr){const re=new RegExp('(?:^|[\\s/|,])'+a.replace(/[.*+?^${}()|[\\]\\]/g,'\\$&')+'\\s*[:=]?\\s*(\\d{1,2})(?=$|[\\s/|,])','i');const m=s.match(re);if(m){labelled[k]=Number(m[1]);break;}}
 }
 if(labelled.spe!==null)return labelled;
 nums=(s.match(/\d{1,2}/g)||[]).map(Number);
 if(nums.length>=6){const a=nums.slice(0,6);return {hp:a[0],atk:a[1],def:a[2],spa:a[3],spd:a[4],spe:a[5]};}
 return labelled;
}
function v19WeightedSpeedPoints(m){
 const rows=v19Rows(m,'spreads','spreads').slice(0,8);if(!rows.length)return 0;
 let w=0,sum=0;for(const r of rows){const sp=v19SpreadPoints(r.raw||r.name).spe;if(!Number.isFinite(sp))continue;const wt=r.pct>0?r.pct:(r.rank===1?1:0);sum+=sp*wt;w+=wt;}
 if(w>0)return Math.max(0,Math.min(32,sum/w));
 const sp=v19SpreadPoints(rows[0]?.raw||rows[0]?.name).spe;return Number.isFinite(sp)?sp:0;
}
function v19WeightedNatureMul(m){
 const rows=v19Rows(m,'natures','natures').slice(0,8);if(!rows.length)return 1;
 let w=0,sum=0;for(const r of rows){const wt=r.pct>0?r.pct:(r.rank===1?1:0);sum+=v19NatureMul(r.name)*wt;w+=wt;}return w?sum/w:1;
}
function v19FindPct(m,key,names){
 const wanted=names.map(v19Norm);let best=0;for(const r of v19Rows(m,key,key))if(wanted.some(x=>v19Norm(r.name).includes(x)||v19Norm(r.raw).includes(x)))best=Math.max(best,r.pct);return best;
}
function v19Speed(m){
 const bs=Number(v19BaseStats(m)?.spe)||Number(m?.baseStats?.spe)||0;
 const points=v19WeightedSpeedPoints(m),nat=v19WeightedNatureMul(m);
 const neutral0=bs+20,neutral32=bs+52,max32=Math.floor((bs+52)*1.1),min0=Math.floor((bs+20)*.9);
 const expected=Math.floor((bs+20+points)*nat);
 const scarfPct=v19FindPct(m,'items',['こだわりスカーフ','choicescarf']);
 return {base:bs,points,nat,expected,neutral0,neutral32,max32,min0,scarf:Math.floor(expected*1.5),scarfPct,scarfMax:Math.floor(max32*1.5)};
}
function v19SpeedWinProb(a,b){
 const A=v19Speed(a),B=v19Speed(b),pa=Math.max(0,Math.min(.9,A.scarfPct/100)),pb=Math.max(0,Math.min(.9,B.scarfPct/100));
 const win=(x,y)=>x>y?1:x===y?.5:0;
 return (1-pa)*(1-pb)*win(A.expected,B.expected)+pa*(1-pb)*win(A.scarf,B.expected)+(1-pa)*pb*win(A.expected,B.scarf)+pa*pb*win(A.scarf,B.scarf);
}
function v19TopNature(m){return v19Rows(m,'natures','natures')[0]||null}
function v19TopSpread(m){return v19Rows(m,'spreads','spreads')[0]||null}

const V19_SETUP=new Set(['つるぎのまい','りゅうのまい','わるだくみ','めいそう','ビルドアップ','ちょうのまい','てっぺき','からをやぶる','のろい']);
const V19_RECOVERY=new Set(['じこさいせい','なまける','はねやすめ','こうごうせい','あさのひざし','つきのひかり','ねむる','ちからをすいとる']);
const V19_PRIORITY=new Set(['かげうち','しんそく','ふいうち','マッハパンチ','アクアジェット','こおりのつぶて','バレットパンチ','でんこうせっか','フェイント']);
const V19_DISRUPT=new Set(['おにび','でんじは','あくび','ちょうはつ','アンコール','トリック','すりかえ','ほえる','ふきとばし','クリアスモッグ','くろいきり']);
const V19_PIVOT=new Set(['とんぼがえり','ボルトチェンジ','クイックターン','すてゼリフ']);
const V19_MULTI=new Set(['つららばり','タネマシンガン','ロックブラスト','スケイルショット','トリプルアクセル','ダブルウイング','ネズミざん','ミサイルばり']);
function v19MoveRate(m,set){let best=0;for(const r of v19Rows(m,'moves','moves'))if(set.has(r.name))best=Math.max(best,r.pct);return best;}
function v19AbilityPct(m,names){return v19FindPct(m,'abilities',names)}
function v19Archetype(m){
 const scarf=v19FindPct(m,'items',['こだわりスカーフ','choicescarf']),sash=v19FindPct(m,'items',['きあいのタスキ','focussash']),left=v19FindPct(m,'items',['たべのこし','leftovers']),orb=v19FindPct(m,'items',['いのちのたま','lifeorb']),lum=v19FindPct(m,'items',['ラムのみ','lumberry']);
 const setup=v19MoveRate(m,V19_SETUP),recovery=v19MoveRate(m,V19_RECOVERY),priority=v19MoveRate(m,V19_PRIORITY),disrupt=v19MoveRate(m,V19_DISRUPT),pivot=v19MoveRate(m,V19_PIVOT),multi=v19MoveRate(m,V19_MULTI);
 const disguise=v19AbilityPct(m,['ばけのかわ','disguise']),unaware=v19AbilityPct(m,['てんねん','unaware']),sturdy=v19AbilityPct(m,['がんじょう','sturdy']),speedBoost=v19AbilityPct(m,['かそく','speedboost']);
 const sp=v19TopSpread(m),pts=v19SpreadPoints(sp?.raw||sp?.name||''),bulkPts=(Number(pts.hp)||0)+(Number(pts.def)||0)+(Number(pts.spd)||0);
 const tags=[];if(scarf>=15)tags.push(`スカーフ ${scarf.toFixed(0)}%`);if(sash>=15)tags.push(`タスキ ${sash.toFixed(0)}%`);if(setup>=15)tags.push(`積み ${setup.toFixed(0)}%`);if(recovery>=15)tags.push(`回復 ${recovery.toFixed(0)}%`);if(priority>=15)tags.push(`先制技 ${priority.toFixed(0)}%`);if(disrupt>=15)tags.push(`妨害 ${disrupt.toFixed(0)}%`);if(pivot>=15)tags.push(`対面操作 ${pivot.toFixed(0)}%`);if(bulkPts>=45)tags.push('耐久振り多め');if(orb>=20)tags.push(`珠 ${orb.toFixed(0)}%`);
 return {scarf,sash,left,orb,lum,setup,recovery,priority,disrupt,pivot,multi,disguise,unaware,sturdy,speedBoost,bulkPts,tags};
}
function v19HasMove(m,names,min=0){const set=new Set(names);return v19Rows(m,'moves','moves').some(r=>set.has(r.name)&&r.pct>=min);}

// Real speed estimate replaces the old rough speed tier while retaining priority/control behavior.
if(typeof v12SpeedEdge==='function'){
 const _v19OldSpeedEdge=v12SpeedEdge;
 v12SpeedEdge=function(a,b){
   try{
     const p=v19SpeedWinProb(a,b),ap=v12Profile(a);
     let out=.12+.88*p;
     if((ap?.priority||0)>=25)out=Math.max(out,.77);
     if((ap?.speedControl||0)>=25)out=Math.max(out,.65);
     return Math.max(.08,Math.min(1,out));
   }catch(e){return _v19OldSpeedEdge(a,b)}
 };
}

// Model common set archetypes when judging a counter, rather than treating every opponent as one generic set.
if(typeof v14CounterScore==='function'){
 const _v19CounterScore=v14CounterScore;
 v14CounterScore=function(m,threat){
   const base=_v19CounterScore(m,threat);if(!base)return base;
   try{
     const ta=v19Archetype(threat),ca=v19Archetype(m),sp=v19SpeedWinProb(m,threat),p=v12Profile(m);let delta=0,cap=98;const rs=[];
     const hasPriority=(p?.priority||0)>=18||ca.priority>=12;
     const hasDisrupt=(p?.disrupt||0)>=18||ca.disrupt>=12;
     const hasMulti=ca.multi>=10;
     const hasPhaze=v19HasMove(m,['ほえる','ふきとばし','クリアスモッグ','くろいきり'],8);
     const candUnaware=ca.unaware>=15;
     if(ta.sash>=25&&!hasPriority&&!hasMulti){delta-=5;cap=Math.min(cap,78);rs.push(`相手はタスキ${Math.round(ta.sash)}%で1回の攻撃だけでは止めにくい`);}
     else if(ta.sash>=25&&(hasPriority||hasMulti)){delta+=4;rs.push('タスキ型にも先制技/連続技で詰めやすい');}
     if(ta.disguise>=25&&!hasMulti&&!hasPriority){delta-=6;cap=Math.min(cap,72);rs.push('ばけのかわ込みの2手処理が必要');}
     if(ta.scarf>=18&&sp<.42&&!hasPriority){delta-=6;cap=Math.min(cap,72);rs.push(`スカーフ型${Math.round(ta.scarf)}%まで含めると上を取られやすい`);}
     else if(ta.scarf>=18&&sp>.62){delta+=3;rs.push('スカーフ型まで含めても速度勝ちしやすい');}
     if(ta.setup>=18){if(candUnaware||hasPhaze||hasDisrupt||hasPriority){delta+=5;rs.push('積み型への切り返し手段がある');}else{delta-=5;cap=Math.min(cap,80);rs.push(`積み技${Math.round(ta.setup)}%への切り返しが弱い`);}}
     if(ta.recovery>=20){if(v19HasMove(m,['ちょうはつ','トリック','すりかえ'],8)){delta+=4;rs.push('回復型をちょうはつ/トリック系で崩せる');}else if((p?.offense||0)<.55){delta-=3;rs.push('回復型を押し切りにくい');}}
     if(ta.priority>=20&&sp>.55&&Number(p?.bulk||0)<86){delta-=3;rs.push('先制技まで含めると高速低耐久で安定しにくい');}
     const score=Math.max(0,Number(base.score||base.pct||0)+delta),pct=Math.min(cap,Math.max(30,Math.round(score)));
     return {...base,score,pct,styleIntel:{threat:ta,candidate:ca,speedWin:sp,delta,cap},reasons:[...new Set([...rs,...(base.reasons||[])])].slice(0,6)};
   }catch(e){console.warn('v19 counter style',e);return base;}
 };
}

// Small recommendation enhancement: current form usage + co-use + real speed, without overpowering the core matchup score.
function v19TeammateRank(a,b){
 const rows=v19Rows(a,'teammates','teammates'),targets=[b?.name,b?.championsId].map(v19Norm).filter(Boolean);
 for(let i=0;i<rows.length;i++){const r=rows[i],rk=r.rank||i+1,k=v19Norm(r.raw+' '+r.name);if(targets.some(t=>k.includes(t)))return rk;}return null;
}
function v19BestPairRank(c){let best=null;for(const m of buildTeam){const a=v19TeammateRank(m,c),b=v19TeammateRank(c,m),r=Math.min(a||999,b||999);if(r<999)best=best===null?r:Math.min(best,r);}return best;}
if(typeof v12CandidateScore==='function'){
 const _v19Candidate=v12CandidateScore;
 v12CandidateScore=function(c,ctx){
   const x=_v19Candidate(c,ctx);try{const pair=v19BestPairRank(c),sp=v19Speed(c),r=[...(x.r||[])];let add=0;if(pair&&pair<=3){add=1.5;r.push(`既存メンバーとの共起上位（最高${pair}位）`);}else if(pair&&pair<=8){add=.7;r.push(`共起実績あり（最高${pair}位）`);}if(sp.scarfPct>=25)r.push(`スカーフ${Math.round(sp.scarfPct)}%で速度補強が現実的`);const s=Math.min(100,x.s+add);return {...x,s,p:Math.round(s),r:[...new Set(r)].slice(0,6),v19:{pair,speed:sp}};}catch(e){return x;}
 };
}

// Current-rank snapshots: mirror the usage-trend idea with the machine-readable live API.
function v19LoadSnapshots(){try{return JSON.parse(localStorage.getItem('champ_v19_rank_snapshots')||'{}')}catch(e){return {}}}
function v19SaveSnapshots(o){try{localStorage.setItem('champ_v19_rank_snapshots',JSON.stringify(o))}catch(e){}}
function v19Today(){return new Date().toISOString().slice(0,10)}
function v19SnapshotRanks(){const o=v19LoadSnapshots(),day=v19Today();o[day]=Object.fromEntries(mons.filter(m=>Number(m.usageRank)>0&&Number(m.usageRank)<999).map(m=>[m.name,Number(m.usageRank)]));const keys=Object.keys(o).sort().slice(-14),next={};for(const k of keys)next[k]=o[k];v19SaveSnapshots(next);return next;}
function v19Trend(m){const o=v19LoadSnapshots(),today=v19Today(),days=Object.keys(o).sort().filter(d=>d<today);if(!days.length)return {delta:null,label:'基準作成済み',cls:'v19TrendFlat'};const prev=o[days[days.length-1]]?.[m.name],now=Number(m.usageRank);if(!prev||!now||now>=999)return {delta:null,label:'—',cls:'v19TrendFlat'};const d=prev-now;if(d>0)return {delta:d,label:`↑ ${d}位上昇`,cls:'v19TrendUp'};if(d<0)return {delta:d,label:`↓ ${Math.abs(d)}位低下`,cls:'v19TrendDown'};return {delta:0,label:'→ 変化なし',cls:'v19TrendFlat'};}
function v19RankFromEntry(e){
 const candidates=[e?.singlesRank,e?.rankSingles,e?.summary?.Singles?.rank,e?.summary?.singles?.rank,e?.summaries?.Singles?.rank,e?.formats?.Singles?.rank,e?.battleSummary?.Singles?.rank,e?.summary?.rank];
 for(const v of candidates){const n=Number(v);if(Number.isFinite(n)&&n>0&&n<999)return n;}
 // Last resort: shallow recursive search for a rank inside a Singles-shaped object.
 for(const [k,v] of Object.entries(e||{})){if(/single/i.test(k)&&v&&typeof v==='object'){const n=Number(v.rank);if(Number.isFinite(n)&&n>0&&n<999)return n;}}
 return null;
}
function v19ShowdownId(m){
 try{if(typeof championsBattleSlug==='function'){const x=championsBattleSlug(m);if(x)return v19Norm(x)}}catch(e){}
 const ov=(typeof championsSpeciesOverrides!=='undefined'?championsSpeciesOverrides[m.name]:null);if(ov)return v19Norm(ov);
 return v19Norm(String(m.championsId||m.name).replace(/mega\s*/ig,'mega').replace(/forme|form/ig,''));
}
function v19ApplyIndex(data){
 const entries=Array.isArray(data?.pokemon)?data.pokemon:(Array.isArray(data)?data:[]);if(!entries.length)return 0;let n=0;
 for(const m of mons){const id=v19ShowdownId(m),entry=entries.find(e=>v19Norm(e.showdownId)===id||v19Norm(e.name)===v19Norm(m.championsId)||v19Norm(e.name)===v19Norm(m.name));if(!entry)continue;const rank=v19RankFromEntry(entry);if(rank){m.usageRank=rank;n++;}}
 if(n){try{rebuildEnvDb();V12_PROFILE_CACHE.clear()}catch(e){}v19SnapshotRanks();}
 return n;
}
async function v19RefreshLiveIndex(){
 const key='champ_v19_index_cache';try{const c=JSON.parse(localStorage.getItem(key)||'null');if(c&&Date.now()-c.ts<6*60*60*1000&&c.data){v19ApplyIndex(c.data);return c.data;}}catch(e){}
 try{const r=await fetch(`${V19_API}/api`,{headers:{Accept:'application/json'}});if(!r.ok)throw new Error('HTTP '+r.status);const data=await r.json();try{localStorage.setItem(key,JSON.stringify({ts:Date.now(),data}))}catch(e){}v19ApplyIndex(data);return data;}catch(e){console.warn('v19 live index',e);v19SnapshotRanks();return null;}
}

// Daily move/item trend for the selected Pokemon.
const V19_DAILY_MEM=new Map();
function v19DailyTop(day,cat){const rows=(day?.rows||[]).filter(r=>String(r.category||'').toLowerCase()===cat).sort((a,b)=>(Number(a.rank)||999)-(Number(b.rank)||999));return rows[0]||null}
function v19DailyDelta(dayNew,dayOld,cat){const top=v19DailyTop(dayNew,cat);if(!top)return null;const name=top.name,old=(dayOld?.rows||[]).find(r=>String(r.category||'').toLowerCase()===cat&&v19Norm(r.name)===v19Norm(name));const a=v19Num(top.percentage_value??top.percentage),b=v19Num(old?.percentage_value??old?.percentage);return {name,now:a,old:b,delta:a-b};}
async function v19DailyIntel(m){
 const id=v19ShowdownId(m);if(!id)return null;if(V19_DAILY_MEM.has(id))return V19_DAILY_MEM.get(id);
 const prom=(async()=>{try{const r=await fetch(`${V19_API}/api/battle/${V19_FMT}/${encodeURIComponent(id)}?days=7`);if(!r.ok)throw new Error('HTTP '+r.status);const d=await r.json(),days=Array.isArray(d.daily)?d.daily:[];if(days.length<2)return {days:days.length};const newest=days[0],oldest=days[days.length-1];return {days:days.length,newest:newest.date,oldest:oldest.date,move:v19DailyDelta(newest,oldest,'move'),item:v19DailyDelta(newest,oldest,'item')};}catch(e){return {error:String(e?.message||e)}}})();V19_DAILY_MEM.set(id,prom);return prom;
}
function v19DeltaHtml(x,cat){if(!x)return `<div class="v19Muted">${cat}：データ不足</div>`;const cls=x.delta>1?'up':x.delta<-1?'down':'',sign=x.delta>0?'+':'';return `<div class="v19DailyLine"><span>${cat}：<b>${v19Esc((typeof displayEnvTerm==='function'?displayEnvTerm(cat==='技'?'moves':'items',x.name):x.name)||x.name)}</b> ${x.now.toFixed(1)}%</span><span class="v19DailyDelta ${cls}">${sign}${x.delta.toFixed(1)}pt</span></div>`;}

function v19PokeId(m){const d=Number(m?.dex);return Number.isFinite(d)&&d>0?String(d).padStart(4,'0')+'-00':''}
function v19ArticleUrl(team){const q=new URLSearchParams({rule:'0',season_start:'1',season_end:'5',trainer_mode:'and',article_title:'',title_mode:'and',sort:'default',per_page:'30'});team.slice(0,6).forEach((m,i)=>{const id=v19PokeId(m);if(id)q.set(`pokemon_${i+1}`,id)});return `${V19_POKEDB}/article/search?${q.toString()}`;}
window.v19OpenArticles=function(names){const team=(Array.isArray(names)?names:[]).map(n=>mons.find(m=>m.name===n)).filter(Boolean);window.open(v19ArticleUrl(team),'_blank','noopener,noreferrer')};
window.v19OpenChart=function(){window.open(`${V19_POKEDB}/pokemon/chart`,'_blank','noopener,noreferrer')};
window.v19OpenPokeDb=function(){window.open(`${V19_POKEDB}/?rule=0#pokemon`,'_blank','noopener,noreferrer')};

function v19SpeedHtml(m){const s=v19Speed(m),nat=v19TopNature(m),spr=v19TopSpread(m);return `<div class="v19SpeedList"><span class="v19Speed">無振 <strong>${s.neutral0}</strong></span><span class="v19Speed">準速32 <strong>${s.neutral32}</strong></span><span class="v19Speed">最速32 <strong>${s.max32}</strong></span><span class="v19Speed">環境目安 <strong>${s.expected}</strong></span>${s.scarfPct>0?`<span class="v19Speed">スカーフ ${s.scarfPct.toFixed(1)}% → <strong>${s.scarf}</strong></span>`:''}</div><div class="v19Muted" style="font-size:9px;margin-top:4px">${nat?`性格上位：${v19Esc(nat.name)} ${nat.pct?nat.pct.toFixed(1)+'%':''}`:'性格データなし'}${spr?` ｜ 能力ポイント上位：${v19Esc(spr.name)}`:''}</div>`;}
function v19TopDataHtml(m){const pick=(key,cat)=>v19Rows(m,key,cat)[0];const mv=pick('moves','moves'),it=pick('items','items'),ab=pick('abilities','abilities'),na=pick('natures','natures');return `<div class="v19ChipRow">${mv?`<span class="v19Chip">技 <strong>${v19Esc(mv.name)}</strong> ${mv.pct.toFixed(1)}%</span>`:''}${it?`<span class="v19Chip">持物 <strong>${v19Esc(it.name)}</strong> ${it.pct.toFixed(1)}%</span>`:''}${ab?`<span class="v19Chip">特性 <strong>${v19Esc(ab.name)}</strong> ${ab.pct.toFixed(1)}%</span>`:''}${na?`<span class="v19Chip">性格 <strong>${v19Esc(na.name)}</strong> ${na.pct.toFixed(1)}%</span>`:''}</div>`;}
function v19EnvMon(){const name=document.querySelector('#envDetail .profile h3')?.textContent?.trim()||document.querySelector('#envDetail h3')?.textContent?.trim();return mons.find(m=>m.name===name)||null}
async function v19RenderEnvIntel(mon){
 if(!mon||!document.getElementById('envDetail'))return;const root=document.getElementById('envDetail');let card=root.querySelector('#v19EnvIntel');if(card&&card.dataset.mon===mon.name)return;if(card)card.remove();card=document.createElement('div');card.id='v19EnvIntel';card.dataset.mon=mon.name;card.className='v19IntelCard';const tr=v19Trend(mon),arch=v19Archetype(mon),rank=Number(mon.usageRank)<999?'#'+mon.usageRank:'圏外';
 card.innerHTML=`<div class="v19IntelHead"><b>実戦インテリジェンス</b><span class="v19Source">PokeDBの見せ方を参考 / Battle Data API</span></div><div class="v19ChipRow"><span class="v19Chip">現在順位 <strong>${rank}</strong></span><span class="v19Chip ${tr.cls}">${tr.label}</span>${arch.tags.slice(0,5).map(x=>`<span class="v19Chip">${v19Esc(x)}</span>`).join('')}</div>${v19TopDataHtml(mon)}<div class="v19Grid"><div class="v19Mini"><b>すばやさライン</b>${v19SpeedHtml(mon)}</div><div class="v19Mini"><b>直近7日・型の変化</b><div id="v19DailyIntel" class="v19Muted">読み込み中…</div></div></div><div class="v19Btns"><button class="v19PokeDbBtn" onclick="v19OpenArticles(['${String(mon.name).replace(/'/g,"\\'")}'])">PokeDBでこのポケモン入り上位構築</button><button class="v19PokeDbBtn" onclick="v19OpenChart()">PokeDB使用率推移</button><button class="v19DataBtn" onclick="v19OpenPokeDb()">PokeDBを開く</button></div>`;root.appendChild(card);
 const d=await v19DailyIntel(mon),box=card.querySelector('#v19DailyIntel');if(!box||card.dataset.mon!==mon.name)return;if(d?.error)box.textContent='直近データを取得できませんでした';else if((d?.days||0)<2)box.textContent='比較できる日次データがまだありません';else box.innerHTML=`<div class="v19Muted">${v19Esc(d.oldest)} → ${v19Esc(d.newest)}</div>${v19DeltaHtml(d.move,'技')}${v19DeltaHtml(d.item,'持ち物')}`;
}

function v19BuildPairs(){let strong=0,known=0,best=[];for(let i=0;i<buildTeam.length;i++)for(let j=i+1;j<buildTeam.length;j++){const a=v19TeammateRank(buildTeam[i],buildTeam[j]),b=v19TeammateRank(buildTeam[j],buildTeam[i]),r=Math.min(a||999,b||999);if(r<999){known++;if(r<=10)strong++;best.push({a:buildTeam[i].name,b:buildTeam[j].name,r});}}best.sort((x,y)=>x.r-y.r);return {known,strong,best:best.slice(0,3)}}
function v19RenderBuildIntel(){
 if(!document.getElementById('buildCurrent'))return;let card=document.getElementById('v19BuildIntel');if(!card){card=document.createElement('div');card.id='v19BuildIntel';card.className='v19IntelCard v19BuildIntel';document.getElementById('buildCurrent').insertAdjacentElement('afterend',card);}if(!buildTeam.length){card.innerHTML='<div class="v19Muted">ポケモンを入れると、Sライン・型・上位構築検索をまとめて表示します。</div>';return;}
 const pairs=v19BuildPairs(),names=JSON.stringify(buildTeam.map(m=>m.name)).replace(/'/g,'&#39;');const teamTags=[];if(buildTeam.some(m=>v19Archetype(m).scarf>=20))teamTags.push('スカーフ採用候補あり');if(buildTeam.some(m=>v19Archetype(m).setup>=20))teamTags.push('積み勝ち筋あり');if(buildTeam.some(m=>v19Archetype(m).pivot>=20))teamTags.push('対面操作あり');
 card.innerHTML=`<div class="v19IntelHead"><b>構築インテリジェンス</b><span class="v19Source">${buildTeam.length}/6体</span></div><div class="v19ChipRow"><span class="v19Chip">共起データ確認ペア <strong>${pairs.known}</strong></span><span class="v19Chip">共起10位以内 <strong>${pairs.strong}</strong></span>${teamTags.map(x=>`<span class="v19Chip">${x}</span>`).join('')}</div><div class="v19TeamSpeeds">${buildTeam.map(m=>{const s=v19Speed(m),a=v19Archetype(m);return `<div class="v19TeamSpeed"><b>${v19Esc(m.name)}</b>S目安 ${s.expected}${s.scarfPct>=10?` / 🧣${s.scarf}`:''}<div class="v19Muted">${a.tags.slice(0,2).map(v19Esc).join('・')||'標準型'}</div></div>`}).join('')}</div>${pairs.best.length?`<div class="v19Muted" style="font-size:9px;margin-top:6px">共起上位：${pairs.best.map(x=>`${v19Esc(x.a)}×${v19Esc(x.b)} ${x.r}位`).join(' / ')}</div>`:''}<div class="v19Btns"><button class="v19PokeDbBtn" id="v19TeamArticleBtn">この並びをPokeDB上位構築で検索</button><button class="v19PokeDbBtn" onclick="v19OpenChart()">使用率推移を見る</button></div>`;
 card.querySelector('#v19TeamArticleBtn')?.addEventListener('click',()=>v19OpenArticles(buildTeam.map(m=>m.name)));
}

// Add compact set/speed labels to recommendation cards after the existing renderer.
if(typeof v12RenderBuildCandidates==='function'){
 const _v19RenderCandidates=v12RenderBuildCandidates;
 v12RenderBuildCandidates=function(scored,ctx,metaLoad){_v19RenderCandidates(scored,ctx,metaLoad);const cards=[...document.querySelectorAll('#buildSuggestions .v12BuildPick')];cards.forEach((card,i)=>{const x=scored[i];if(!x?.m)return;const old=card.querySelector('.v19CandidateTags');if(old)old.remove();const s=v19Speed(x.m),a=v19Archetype(x.m),pair=v19BestPairRank(x.m),tags=[`S目安 ${s.expected}`];if(s.scarfPct>=10)tags.push(`スカーフ ${Math.round(s.scarfPct)}%`);if(a.sash>=15)tags.push(`タスキ ${Math.round(a.sash)}%`);if(a.setup>=15)tags.push(`積み ${Math.round(a.setup)}%`);if(pair)tags.push(`共起最高 ${pair}位`);const el=document.createElement('div');el.className='v19CandidateTags';el.innerHTML=tags.slice(0,4).map(t=>`<span class="v19CandidateTag">${v19Esc(t)}</span>`).join('');const btn=card.querySelector('.buildAddBtn');if(btn)btn.insertAdjacentElement('beforebegin',el);else card.appendChild(el);});};
}

// Keep our panels alive after the app re-renders.
if(typeof renderBuildCurrent==='function'){
 const _v19RenderBuildCurrent=renderBuildCurrent;renderBuildCurrent=function(){const r=_v19RenderBuildCurrent.apply(this,arguments);setTimeout(v19RenderBuildIntel,0);return r;};
}
const envRoot=document.getElementById('envDetail');if(envRoot){new MutationObserver(()=>{const m=v19EnvMon();if(m&&!envRoot.querySelector(`#v19EnvIntel[data-mon="${CSS.escape(m.name)}"]`))setTimeout(()=>v19RenderEnvIntel(m),0)}).observe(envRoot,{childList:true,subtree:false});}

function v19RefreshVisible(){try{renderHomeV18()}catch(e){}try{renderBuildRoster()}catch(e){}try{renderBuildCurrent()}catch(e){}try{renderEnvList()}catch(e){}const m=v19EnvMon();if(m)v19RenderEnvIntel(m);}

// Bootstrap: save a baseline immediately, then replace stale static ranks with current API ranks when available.
v19SnapshotRanks();v19RenderBuildIntel();const m0=v19EnvMon();if(m0)v19RenderEnvIntel(m0);
v19RefreshLiveIndex().then(()=>v19RefreshVisible());

window.__V19_INTEL__={speed:v19Speed,archetype:v19Archetype,trend:v19Trend,articleUrl:v19ArticleUrl,daily:v19DailyIntel,refresh:v19RefreshLiveIndex};
window.__V19_SELFTEST__={speed:typeof v19Speed==='function',counter:typeof v14CounterScore==='function',articles:v19ArticleUrl([mons[0]||{}]).includes('article/search'),snapshots:typeof v19Trend==='function'};
document.documentElement.setAttribute('data-v19-selftest',Object.values(window.__V19_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('body close marker not found')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
