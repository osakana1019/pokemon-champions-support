from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.9 solid nav + transparent art ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v20.8','Pokémon Champions Support — v20.9')
s=s.replace('<div class="badge">v20.8</div>','<div class="badge">v20.9</div>',1)
css=r'''<style id="v209-solid-nav">
/* ===== v20.9 solid nav + transparent art ===== */
#v205Rail{display:none!important}
@media(min-width:1080px){
 body.v209NavOn .wrap{width:auto!important;max-width:none!important;margin:0!important;padding:14px 24px 34px 126px!important}
 body.v209NavOn>.wrap>.appnav{display:none!important}
 #v209Nav{position:fixed;left:12px;top:12px;bottom:12px;z-index:800;width:98px;padding:10px 8px;display:flex;flex-direction:column;gap:7px;border:1px solid var(--xline);border-radius:20px;background:color-mix(in srgb,var(--xcard) 96%,transparent);box-shadow:0 14px 38px #0003;backdrop-filter:blur(14px);overflow:hidden;color:var(--xtext)}
 .v209Brand{height:42px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:var(--xaccent);color:var(--xaccenttext);font-weight:950;font-size:12px;letter-spacing:.08em;margin-bottom:3px;flex:none}
 .v209Sep{height:1px;background:var(--xline);margin:0 6px 3px;flex:none}
 #v209Nav button{position:relative!important;width:100%!important;min-height:58px!important;padding:6px 4px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:4px!important;border-radius:13px!important;background:transparent!important;color:var(--xmuted)!important;box-shadow:none!important;border:0!important;overflow:hidden!important;line-height:1!important}
 #v209Nav button:hover{background:var(--xsoft)!important;color:var(--xtext)!important}
 #v209Nav button.active{background:var(--xaccent)!important;color:var(--xaccenttext)!important}
 .v209Ico{width:23px;height:23px;display:grid;place-items:center;font-size:19px!important;line-height:23px!important;font-weight:900!important;color:currentColor!important;flex:none;overflow:visible!important}
 .v209Lbl{display:block!important;width:100%;font-size:9px!important;line-height:1.1!important;font-weight:900!important;letter-spacing:0!important;text-align:center!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:clip!important;color:currentColor!important}
 .v209Count{position:absolute;right:4px;top:4px;min-width:16px;height:16px;padding:0 4px;border-radius:999px;display:grid;place-items:center;font-size:8px!important;font-weight:950!important;line-height:16px!important;background:var(--xtext);color:var(--xbg);border:2px solid var(--xcard)}
 .v209Bottom{margin-top:auto;display:grid;gap:7px;flex:none}
}
@media(max-width:1079px){#v209Nav{display:none!important}}
/* Zukan artwork must sit directly on the UI, never inside a white image tile. */
.mon img,.sel img,.rankRow img,.oppQuickMon img,.profile img,.pick img,.metaRec img,.savedHead img,.homePartyMon img,.homeMetaMon img,.variantChoice img,.v206SourceMon img,.buildSlot img{
 background:transparent!important;border:0!important;outline:0!important;box-shadow:none!important;border-radius:0!important;padding:0!important;filter:none!important;image-rendering:auto!important
}
</style>'''
s=s.replace('</body>',css+'\n</body>',1)
p.write_text(s,encoding='utf-8')
