from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.8 labeled rail ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v20.7','Pokémon Champions Support — v20.8')
s=s.replace('<div class="badge">v20.7</div>','<div class="badge">v20.8</div>',1)
css=r'''<style id="v208-labeled-rail">
/* ===== v20.8 labeled rail ===== */
@media(min-width:1080px){
 body.v205RailOn .wrap{padding-left:112px!important}
 #v205Rail{width:78px!important;padding:9px 7px!important;align-items:center!important;overflow:visible!important}
 .v205Logo{width:48px!important;height:40px!important;margin-bottom:6px!important;font-size:11px!important;border-radius:12px!important}
 #v205Rail .v205RailBtn{width:62px!important;height:56px!important;min-height:56px!important;max-width:62px!important;padding:5px 3px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:3px!important;overflow:visible!important;font-size:inherit!important;line-height:1!important;border-radius:13px!important}
 #v205Rail .v205RailBtn svg,#v205Rail .v207Glyph{display:none!important}
 .v208RailIcon{display:block!important;height:22px;line-height:22px;font-size:20px!important;font-family:system-ui,-apple-system,"Segoe UI Symbol","Noto Sans Symbols 2",sans-serif!important;font-weight:700!important;color:currentColor!important;pointer-events:none!important}
 .v208RailLabel{display:block!important;max-width:56px;font-size:8.5px!important;line-height:1.05!important;letter-spacing:0!important;font-weight:850!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:clip!important;color:currentColor!important;pointer-events:none!important}
 .v205Tip{display:none!important}
 .v205Count{right:-1px!important;top:-1px!important;z-index:3!important}
 #v205Rail .v205RailBtn.active .v208RailIcon,#v205Rail .v205RailBtn.active .v208RailLabel{color:var(--xaccenttext)!important}
 #v205Rail .v205RailBtn:not(.active) .v208RailLabel{color:var(--xmuted)!important}
 #v205Rail .v205RailBtn:hover .v208RailLabel{color:var(--xtext)!important}
}
</style>'''
s=s.replace('</body>',css+'\n</body>',1);p.write_text(s,encoding='utf-8')
