from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.6 rail polish + fit meters ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v20.5','Pokémon Champions Support — v20.6')
s=s.replace('<div class="badge">v20.5</div>','<div class="badge">v20.6</div>',1)
css=r'''<style id="v206-polish">
/* ===== v20.6 rail polish + fit meters ===== */
@media(min-width:1080px){
 body.v205RailOn .wrap{padding-left:96px!important}
 #v205Rail{width:60px!important;padding:8px 6px!important;border-radius:18px!important;overflow:visible!important}
 .v205Logo{width:40px!important;height:40px!important;border-radius:12px!important;font-size:12px!important;margin-bottom:8px!important}
 .v205RailBtn{width:44px!important;height:44px!important;min-height:44px!important;max-width:44px!important;overflow:visible!important;font-size:0!important;line-height:0!important;flex:none!important}
 .v205RailBtn svg{width:20px!important;height:20px!important;display:block!important;overflow:visible!important}
 .v205RailBtn>*:not(svg):not(.v205Tip):not(.v205Count){display:none!important}
 .v205Tip{left:52px!important;z-index:900!important;max-width:180px!important;overflow:hidden!important;text-overflow:ellipsis!important;font-size:10px!important;line-height:1.2!important;letter-spacing:0!important;border:1px solid var(--xline)!important;background:var(--xcard)!important;color:var(--xtext)!important;box-shadow:0 8px 24px #0004!important}
 .v205Count{right:-3px!important;top:-3px!important;min-width:17px!important;width:auto!important;height:17px!important;max-width:28px!important;padding:0 4px!important;font-size:8px!important;line-height:17px!important;overflow:hidden!important;white-space:nowrap!important;border:2px solid var(--xcard)!important;background:var(--xaccent)!important;color:var(--xaccenttext)!important}
}
/* Candidate fit meter: theme-safe, 1:1 with displayed percentage. */
#buildSuggestions .v12BuildPick .compatPct{display:flex!important;align-items:baseline!important;gap:5px!important;margin-top:8px!important;font-size:20px!important;color:var(--xtext)!important}
#buildSuggestions .v12BuildPick .compatPct:after{content:'適合度';font-size:9px;font-weight:800;color:var(--xmuted)!important;order:-1}
#buildSuggestions .v12BuildPick .compatBar{position:relative!important;height:8px!important;margin:5px 0 10px!important;border-radius:999px!important;overflow:hidden!important;background:var(--xsoft)!important;border:1px solid var(--xline)!important;box-shadow:none!important}
#buildSuggestions .v12BuildPick .compatBar>div{height:100%!important;max-width:100%!important;min-width:0!important;border-radius:999px!important;background:var(--xaccent)!important;box-shadow:none!important;transition:width .18s ease!important}
#buildSuggestions .v12BuildPick .compatBar:after{content:'';position:absolute;left:50%;top:-1px;bottom:-1px;width:1px;background:var(--xline);opacity:.7}
#v206PartySource{margin:0 0 12px;padding:11px 12px;border:1px solid var(--xline);border-radius:14px;background:var(--xcard2);color:var(--xtext)}
.v206SourceHead{display:flex;justify-content:space-between;gap:10px;align-items:baseline;margin-bottom:8px}.v206SourceHead b{font-size:12px}.v206SourceHead span{font-size:9px;color:var(--xmuted)}
.v206SourceMons{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px}.v206SourceMon{min-width:0;padding:6px 4px;border:1px solid var(--xline);border-radius:10px;background:var(--xcard);text-align:center}.v206SourceMon img{display:block;width:38px;height:38px;object-fit:contain;margin:0 auto 2px}.v206SourceMon span{display:block;font-size:8px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--xtext)}
.v206SourceEmpty{display:grid;place-items:center;min-height:50px;border:1px dashed var(--xline);border-radius:10px;color:var(--xmuted);font-size:9px}
.v206MeterNote{font-size:9px!important;color:var(--xmuted)!important;margin:-3px 0 9px!important}
@media(max-width:720px){.v206SourceMons{grid-template-columns:repeat(3,minmax(0,1fr))}}
</style>'''
s=s.replace('</body>',css+'\n</body>',1);p.write_text(s,encoding='utf-8')
