from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v18.13: canonical species + visible Mega recommendations ===== */'
if marker in s:
    raise SystemExit(0)

s=s.replace('Pokémon Champions Support — v18.12','Pokémon Champions Support — v18.13')
patch=r'''
<script>
/* ===== v18.13: canonical species + visible Mega recommendations ===== */
(function(){
  // Treat alternate formes as the same species. National Dex number is the most reliable key
  // in this app, and fixes Rotom -> Heat/Wash/Frost/Fan/Mow recommendations in particular.
  const oldSpeciesKey=speciesKey;
  speciesKey=function(m){
    if(!m)return '';
    const dex=Number(m.dex);
    if(Number.isFinite(dex)&&dex>0)return `dex:${dex}`;
    let n=String(m.name||'');
    if(/ロトム/.test(n))return 'species:ロトム';
    if(n.startsWith('メガ'))n=n.replace(/^メガ/,'').replace(/[XY]$/,'');
    return n||oldSpeciesKey(m);
  };
  sameSpecies=function(a,b){return !!a&&!!b&&speciesKey(a)===speciesKey(b);};

  // Re-evaluate Mega forms with the canonical species grouping.
  v14MegaFormsFor=function(m){
    if(!m)return [];
    const k=speciesKey(m);
    return mons.filter(x=>x.mega&&speciesKey(x)===k);
  };
  if(typeof v15BaseFor==='function'){
    v15BaseFor=function(m){return mons.find(x=>!x.mega&&speciesKey(x)===speciesKey(m))||null;};
  }

  // A team with one Mega should visibly receive another Mega option, not one buried at the end.
  // Zero Megas -> at least two Mega options in the first 8; one Mega -> at least one in the first 6.
  v15EnsureMegaSuggestions=function(scored,allMega,target,limit=16){
    let out=scored.slice(0,limit);
    const buildKeys=new Set(buildTeam.map(speciesKey));
    const megaPool=allMega
      .filter(x=>x?.m?.mega&&!buildKeys.has(speciesKey(x.m)))
      .sort((a,b)=>b.s-a.s||((v12Profile(a.m)?.rank||999)-(v12Profile(b.m)?.rank||999)));
    const wanted=Math.max(0,Math.min(target,megaPool.length));
    const zone=wanted>=2?8:6;
    const zoneMegaCount=()=>out.slice(0,zone).filter(x=>x.m?.mega).length;
    const usedKeys=new Set(out.map(x=>speciesKey(x.m)));

    for(const mg of megaPool){
      if(zoneMegaCount()>=wanted)break;
      const key=speciesKey(mg.m);
      // If the same species is present as a normal forme in recommendations, replace it.
      let sameIdx=out.findIndex(x=>speciesKey(x.m)===key);
      if(sameIdx>=0){
        out.splice(sameIdx,1);
        usedKeys.delete(key);
      }
      if(usedKeys.has(key))continue;
      const insertAt=Math.min(zone-1,out.length);
      out.splice(insertAt,0,mg);
      usedKeys.add(key);
      if(out.length>limit)out.pop();
    }
    return out.slice(0,limit);
  };

  // Self-check Rotom family grouping if the forms exist in the data.
  const rotoms=mons.filter(m=>/ロトム/.test(m.name||''));
  const rotomOK=rotoms.length<2||rotoms.every(m=>speciesKey(m)===speciesKey(rotoms[0]));
  window.__V1813_SELFTEST__={species:typeof sameSpecies==='function',rotom:rotomOK,megaEnsure:typeof v15EnsureMegaSuggestions==='function'};
  document.documentElement.setAttribute('data-v1813-selftest',Object.values(window.__V1813_SELFTEST__).every(Boolean)?'ok':'fail');

  try{renderBuildRoster();}catch(e){}
})();
</script>
'''
if '</body>' not in s:
    raise SystemExit('body close marker not found')
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
