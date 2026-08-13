from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v19.2: elite adoption frequency + single power sanity ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v19.1','Pokémon Champions Support — v19.2')
patch=r'''
<style>
.v192EvidenceLow{font-size:9px;padding:3px 6px;border:1px solid #5b3e45;background:#26171b;border-radius:999px;color:#efb5c0}
.v192EvidenceHigh{font-size:9px;padding:3px 6px;border:1px solid #3b5a4c;background:#14261f;border-radius:999px;color:#a9e8c5}
</style>
<script>
/* ===== v19.2: elite adoption frequency + single power sanity ===== */
(function(){
'use strict';
// Current singles strength tiers (small sanity signal only; recommendation remains matchup-first).
const V192_TIER={
 'ブリジュラス':'SS','カバルドン':'SS','ガブリアス':'SS',
 'ヒスイダイケンキ':'S','マスカーニャ':'S','ニンフィア':'S','アシレーヌ':'S','イダイトウ(オス)':'S','ミミッキュ':'S','ギルガルド(シールドフォルム)':'S','キラフロル':'S','ハラバリー':'S',
 'ギャラドス':'A','エルフーン':'A','ハッサム':'A','アーマーガア':'A','ブラッキー':'A','ウォッシュロトム':'A','ゲンガー':'A','クエスパトラ':'A','サザンドラ':'A','ドドゲザン':'A','ドラパルト':'A','ウルガモス':'A','ゲッコウガ':'A','オーロンゲ':'A','サーフゴー':'A',
 'ピクシー':'B','ソウブレイズ':'B','ビビヨン':'B','アローラキュウコン':'B','ラウドボーン':'B','オオニューラ':'B','カイリュー':'B','ヒートロトム':'B','ドリュウズ':'B','マンムー':'B','ドヒドイデ':'B','バイバニラ':'B','バシャーモ':'B',
 'ペンドラー':'C','ラグラージ':'C','エンペルト':'C','ミロカロス':'C','ヤバソチャ(ボンサクのすがた)':'C','ペリッパー':'C','マリルリ':'C','メタモン':'C','ジャローダ':'C','エルレイド':'C','シャワーズ':'C','カビゴン':'C','バンギラス':'C','エアームド':'C','ブリムオン':'C','ヒスイゾロアーク':'C','オニシズクモ':'C','ガラルヤドキング':'C','ミミズズ':'C','ポットデス(がんさくフォルム)':'C','ハリーマン':'C','ハカドッグ':'C','コノヨザル':'C','スコヴィラン':'C','ランクルス':'C',
 'コータス':'D','ユキノオー':'D','ヒスイジュナイパー':'D','ガラルヤドラン':'D','エレザード':'D','イッカネズミ(3びきかぞく)':'D','カットロトム':'D','ガオガエン':'D','デカヌチャン':'D','エーフィ':'D','バサギリ':'D','ホルード':'D','ヒスイヌメルゴン':'D','ヒスイウインディ':'D','ローブシン':'D','グレンアルマ':'D','ヒスイバクフーン':'D','ドデカバシ':'D','ラフレシア':'D','オニゴーリ':'D','イダイトウ(メス)':'D','ワルビアル':'D'
};
const V192_TIER_VALUE={SS:4,S:3,A:2,B:1,C:0,D:-1};
function v192EliteAppearances(c){
 const builds=Array.isArray(window.V191_ELITE_BUILDS)?window.V191_ELITE_BUILDS:[];
 let count=0,weighted=0,best=null;
 for(const b of builds){
  const found=b.team.some(name=>{
   const m=mons.find(x=>x.name===name);if(!m)return name===c.name;
   if(m.mega||c.mega)return m.name===c.name;
   return sameSpecies(m,c);
  });
  if(found){count++;weighted+=Number(b.weight)||1;if(!best||Number(b.weight)>Number(best.weight))best=b;}
 }
 return {count,weighted,total:builds.length,best};
}
function v192Evidence(c){
 const elite=v192EliteAppearances(c),tier=V192_TIER[c.name]||null,tierVal=tier?V192_TIER_VALUE[tier]:null,rank=Number(envData(c)?.rank||c.usageRank||999);
 let delta=0;const reasons=[];
 // Elite appearances are a global viability signal, separate from pair-specific v19.1 evidence.
 if(elite.count>=3){delta+=2.6;reasons.push(`上位構築で複数回採用（${elite.count}件）`);}
 else if(elite.count===2){delta+=1.6;reasons.push('上位構築で複数採用');}
 else if(elite.count===1){delta+=.6;}
 // Absence is meaningful only when combined with mediocre tier/rank; never hard-exclude on sparse samples.
 if(elite.count===0){
   if(tierVal!==null&&tierVal<=1&&rank>45){delta-=4.4;reasons.push('上位構築実績が薄く、単体評価も高くない');}
   else if(tierVal!==null&&tierVal<=1&&rank>30){delta-=3.1;reasons.push('上位構築での採用根拠が薄い');}
   else if(tierVal!==null&&tierVal<=0){delta-=3.6;reasons.push('上位実績・単体性能ともに補完枠寄り');}
   else if(rank>70){delta-=2.2;reasons.push('環境順位と上位採用の両方が低め');}
 }
 // Strong intrinsic mons should not be punished just because the curated elite sample misses them.
 if(tierVal!==null&&tierVal>=3)delta+=.8;
 return {elite,tier,tierVal,rank,delta,reasons};
}
window.v192Evidence=v192Evidence;

if(typeof v12CandidateScore==='function'){
 const _v192Candidate=v12CandidateScore;
 v12CandidateScore=function(c,ctx){
   const x=_v192Candidate(c,ctx);if(!x)return x;
   try{
    const ev=v192Evidence(c),s=Math.max(0,Math.min(100,Number(x.s||0)+ev.delta));
    const rs=[...(x.r||[])];
    if(ev.reasons.length)rs.unshift(...ev.reasons);
    return {...x,s,p:Math.round(s),r:[...new Set(rs)].slice(0,7),v192:ev};
   }catch(e){return x;}
 };
}

// Ensure the rendered cards expose why a theoretically neat but low-evidence pick was demoted.
if(typeof v12RenderBuildCandidates==='function'){
 const _v192Render=v12RenderBuildCandidates;
 v12RenderBuildCandidates=function(scored,ctx,metaLoad){
   _v192Render(scored,ctx,metaLoad);
   const cards=[...document.querySelectorAll('#buildSuggestions .v12BuildPick')];
   cards.forEach((card,i)=>{
     const ev=scored[i]?.v192;if(!ev)return;
     let row=card.querySelector('.v19CandidateTags');
     if(!row){row=document.createElement('div');row.className='v19CandidateTags';const btn=card.querySelector('.buildAddBtn');if(btn)btn.insertAdjacentElement('beforebegin',row);else card.appendChild(row);}
     if(ev.elite.count>=2){const t=document.createElement('span');t.className='v192EvidenceHigh';t.textContent=`上位構築採用 ${ev.elite.count}件`;row.prepend(t);}
     else if(ev.elite.count===0&&ev.delta<=-3){const t=document.createElement('span');t.className='v192EvidenceLow';t.textContent=`上位実績薄め${ev.tier?' / '+ev.tier:''}`;row.prepend(t);}
   });
 };
}
window.__V192_SELFTEST__={evidence:typeof v192Evidence==='function',heat:!!mons.find(m=>m.name==='ヒートロトム'),tier:V192_TIER['ヒートロトム']==='B'};
document.documentElement.setAttribute('data-v192-selftest',Object.values(window.__V192_SELFTEST__).every(Boolean)?'ok':'fail');
})();
</script>
'''
if '</body>' not in s: raise SystemExit('no body close')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
