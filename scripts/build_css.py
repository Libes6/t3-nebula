"""Build t3-nebula.json = original Nebula (src/nebula-base.json) + extras.

usage: python3 scripts/build_css.py [out.json]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "t3-nebula.json")
d = json.load(open(os.path.join(ROOT, "src", "nebula-base.json")))
css = d["css"]

G = "#3f55e0,#a0309f 38%,#e0204f 68%,#e8a040"   # original Nebula gradient
USAGE = ':has(>div>header[class*="usage-header"])'
PAGES = f'[data-workspace-area="settings"],{USAGE}'

# 1. Nebula background on Settings and Usage too (same rule as the chat canvas)
css = css.replace("[data-chat-canvas]{background-image", f":is([data-chat-canvas],{PAGES}){{background-image", 1)
css = css.replace("@media (prefers-reduced-motion:reduce){[data-chat-canvas],",
                  f"@media (prefers-reduced-motion:reduce){{[data-chat-canvas],{PAGES},", 1)
# softer dot grid (fine, faint light dots instead of coarse dark ones)
for a, b in [("radial-gradient(rgba(0,0,0,.28) 1px,transparent 1.6px)", "radial-gradient(circle,rgba(242,209,246,.05) .65px,transparent .9px)"),
             ("background-size:7px 7px,", "background-size:4px 4px,")]:
    assert css.count(a) == 1, a
    css = css.replace(a, b)
# calmer, darker palette (our earlier look): deep blue core, magenta/red glow low, dark edges
for a, b in [("rgba(44,66,200,0.75),rgba(44,66,200,0.34)", "rgba(54,78,203,0.5),rgba(43,59,159,0.19)"),
             ("rgba(210,140,50,0.62),rgba(210,140,50,0.28)", "rgba(202,140,66,0.3),rgba(137,81,48,0.12)"),
             ("rgba(140,28,124,0.62),rgba(140,28,124,0.28)", "rgba(149,19,119,0.42),rgba(114,19,86,0.17)"),
             ("rgba(222,20,64,0.78),rgba(222,20,64,0.35)", "rgba(207,26,71,0.45),rgba(124,24,68,0.18)"),
             ("rgba(190,20,70,0.45),rgba(190,20,70,0.2)", "rgba(190,20,70,0.25),rgba(190,20,70,0.1)"),
             ("rgba(70,16,60,0.7),rgba(70,16,60,0.32)", "rgba(110,22,70,0.55),rgba(70,16,60,0.22)"),
             ("background-color:#0b060d", "background-color:#120a18")]:
    assert css.count(a) == 1, a
    css = css.replace(a, b)
assert css.count(PAGES) == 2, "base CSS changed, update the anchors"

x = []
x += [
 f':is({PAGES}) :is([data-settings-page-scroll],.bg-background){{background:transparent!important}}',
 'header[class*="usage-header"]{background:rgba(14,7,16,.55)!important;border-bottom:1px solid rgba(255,255,255,.07)!important}',
]
# 2. Composer with an attached drawer (questions, approvals): no double frame
x += ['[data-chat-composer-surface]:has([data-composer-banner-surface="attached"],[data-chat-composer-top-drawer]) [data-slot="composer-host"]{background:transparent!important;backdrop-filter:none;box-shadow:none!important;animation:none!important}']
# Warning banner has its own pseudo-element outline, independently of its parents.
x += [
 '[data-composer-banner-surface][data-variant="warning"]{background:transparent!important;border:0!important;outline:0!important;box-shadow:none!important}',
 '[data-composer-banner-surface][data-variant="warning"]::before,[data-composer-banner-surface][data-variant="warning"]::after{content:none!important;display:none!important;border:0!important;box-shadow:none!important;background:none!important}',
]
# With the banner backdrop removed, remove its deliberate overlap with the input.
x += [
 '[data-slot="composer-banner-attachment"]:has([data-composer-banner-surface][data-variant="warning"]){margin-bottom:0!important}',
 '[data-composer-banner-surface][data-variant="warning"]{--chat-composer-attachment-overlap:0px!important;padding-bottom:8px!important}',
]
# 3. Agent working: composer glow speeds up, running thread shimmers
W = ':root:has([data-sidebar-row][aria-current]:not([aria-current="false"])[aria-busy="true"])'
x += [
 f'{W} [data-slot="composer-host"]{{animation-duration:3s!important}}',
 f'{W} [data-slot="composer-host"]::after{{animation-duration:3s!important}}',
 '[data-sidebar-row][aria-busy="true"]{background:linear-gradient(90deg,rgba(63,85,224,.12),rgba(160,48,159,.2),rgba(63,85,224,.12)) 0 0/200% 100%!important;animation:nbBtn 1.2s ease-in-out infinite alternate}',
]
# 4. Caret and focus in Nebula colors
x += ['[data-slot="composer-host"] :is([contenteditable],textarea){caret-color:#e0559f}',
      ':focus-visible{outline-color:#c04aa0!important}']
# 5. Usage limits: show USED instead of LEFT, bars fill from the left with the used part
C = '.p-4:has(>div>div>[aria-label*="% left"])'          # limit card on the Usage page
B = 'button[aria-label*="% left"]'                        # its bar
R = '[class*="grid-cols-subgrid"][aria-label$="% left"]'  # row in the thread-details panel
x += [
 C + '{background:rgba(26,14,28,.72)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:16px!important;box-shadow:0 18px 50px rgba(0,0,0,.35)}',
 f'{C} .text-3xl,{C} .text-3xl+span>span:first-child,{R}>span:last-child{{font-size:0!important}}',
 C + ' .text-3xl::after{content:counter(nu) "%";font-size:1.875rem;line-height:2.25rem}',
 C + ' .text-3xl+span>span:first-child::after{content:"used";font-size:.875rem}',
 R + '>span:last-child::after{content:counter(nu) "%";font-size:.75rem}',
 B + '{transform:scaleX(-1);background:rgba(10,5,12,.6)!important}',
 f'{B}>span:not([class~="w-0.5"]),{B}>div:last-child{{transform:scaleX(-1)}}',
 B + f'>div:first-child>div{{background:repeating-linear-gradient(135deg,rgba(255,255,255,.14) 0 1px,transparent 1px 6px),linear-gradient(270deg,{G})!important;opacity:.85}}',
 B + ' [class~="left-0"]{background:rgba(10,5,12,.85)!important;opacity:1!important}',
 B + ' [class~="right-0"]{display:none!important}',
 B + '>[class~="w-0.5"]{box-shadow:0 0 6px rgba(255,200,240,.8)}',
 R + f'>span.relative{{transform:scaleX(-1);height:4px;background:linear-gradient(270deg,{G})!important;box-shadow:0 0 8px rgba(200,50,140,.3)}}',
 R + '>span.relative>span[class~="left-0"]{background:rgba(40,22,44,1)!important}',
]
# counter nu = 100 - left; " 5% left" never matches "95% left"
x += [f'.p-4:has(>div>div>[aria-label*=" {n}% left"]),[aria-label$=" {n}% left"]{{counter-reset:nu {100-n}}}' for n in range(101)]

d["css"] = css.rstrip() + "\n" + "\n".join(x) + "\n"
assert len(d["css"]) <= 50000, len(d["css"])
json.dump(d, open(out, "w"), ensure_ascii=False, indent=2)
print(len(d["css"]), "chars ->", out)
