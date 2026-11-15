import json,sys
p=sys.argv[1]; d=json.load(open(p))
G3='#4e66d8,#b2378d 55%,#cb325b'          # nebula gradient
CUR='[aria-current]:not([aria-current="false"])'
W=f':root:has([data-sidebar-row]{CUR}[aria-busy="true"])'   # current thread is working
r=[]
# --- base (unchanged values, minified) ---
r+=['@keyframes nebula-drift{0%,100%{background-position:35vw -25vh,-40vw 10vh,45vw 45vh,-20vw 60vh,0 0}50%{background-position:-35vw -10vh,35vw 35vh,-35vw 50vh,40vw 35vh,0 0}}',
'@keyframes nebula-glow{0%,100%{border-color:#5d70ce80;box-shadow:0 0 20px #4056ef2b}33%{border-color:#b0408a90;box-shadow:0 0 22px #c52f9030}66%{border-color:#c0395590;box-shadow:0 0 22px #d9305130}85%{border-color:#be885390;box-shadow:0 0 20px #dc9f4326}}',
'@keyframes nebula-send{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}',
'@keyframes nebula-breath{0%,100%{box-shadow:0 0 18px #b2378d40,0 0 0 1px #cb4fa060}50%{box-shadow:0 0 34px #4e66d866,0 0 0 1px #6d82ffa0}}',
'.dark :is([data-workspace-area="conversation"],[data-workspace-area="settings"],:has(>div>header[class*="usage-header"])){background-color:#120a18!important;background-image:radial-gradient(ellipse at center,#364ecb81 0%,#2b3b9f30 38%,transparent 69%),radial-gradient(ellipse at center,#95137775 0%,#72135630 38%,transparent 70%),radial-gradient(ellipse at center,#cf1a4785 0%,#7c184430 38%,transparent 70%),radial-gradient(ellipse at center,#ca8c426b 0%,#89513025 38%,transparent 70%),radial-gradient(circle,#f2d1f60c .65px,transparent .9px)!important;background-size:100% 110%,100% 120%,100% 110%,90% 100%,4px 4px!important;background-repeat:no-repeat,no-repeat,no-repeat,no-repeat,repeat!important;animation:nebula-drift 28s ease-in-out infinite!important}',
'.dark .messages-timeline-scroll{background:transparent!important}',
'.dark [data-chat-header]{background:#120b1ad9!important;border-bottom:1px solid #be86ce14!important;backdrop-filter:blur(16px)}',
'.dark [data-slot="sidebar-inner"]{background:#1a0d22ea!important}',
'.dark [data-slot="sidebar"]{border-color:#bc66b71c!important}',
'.dark [data-thread-item]{border-radius:6px}',
'.dark [data-user-message-bubble]{background:#cf9ecb1a!important;border:1px solid #f4c7f812;box-shadow:0 2px 12px #12091a18}',
'.dark [data-slot="composer-host"]{background:#220d23e8!important;border:1px solid #86407770!important;border-radius:18px!important;backdrop-filter:blur(18px);animation:nebula-glow 16s linear infinite}',
f'.dark [data-chat-composer-form] button[type="submit"]{{background:linear-gradient(120deg,#4e66d8,#b2378d,#cb325b,#cf9555,#4e66d8)!important;background-size:300% 300%!important;color:#fff!important;animation:nebula-send 9s ease infinite!important}}',
'.dark [data-chat-composer-form] button[type="submit"]:disabled{opacity:.5!important}',
# composer with attached drawer (questions, approvals): glow goes to the outer surface, inner host stays flat
'.dark [data-chat-composer-surface]:has([data-composer-banner-surface="attached"],[data-chat-composer-top-drawer]){background:#220d23e8!important;border:1px solid #86407770!important;border-radius:18px!important;backdrop-filter:blur(18px);animation:nebula-glow 16s linear infinite}',
'.dark [data-chat-composer-surface]:has([data-composer-banner-surface="attached"],[data-chat-composer-top-drawer]) [data-slot="composer-host"]{background:transparent!important;border-color:transparent!important;box-shadow:none!important;animation:none!important;backdrop-filter:none}',
'.dark [data-thread-details-card]{background:#261229ce!important;border:1px solid #ba77af25!important;backdrop-filter:blur(16px)}',
'.dark .chat-markdown-codeblock{background:#150f24e8!important;border:1px solid #b993c826}',
]
# --- 4. working state: faster glow + breathing composer, send button spins faster ---
r+=[f'.dark{W} [data-slot="composer-host"]{{animation:nebula-glow 3s linear infinite,nebula-breath 2.4s ease-in-out infinite!important}}',
f'.dark{W} [data-chat-composer-form] button[type="submit"]{{animation:nebula-send 2s ease infinite!important}}',
f'.dark [data-sidebar-row][aria-busy="true"]{{background:linear-gradient(90deg,#4e66d81f,#b2378d2e,#4e66d81f) 0 0/200% 100%!important;animation:nebula-send 2.4s linear infinite}}']
# --- 10. selection, focus, caret, scrollbar ---
r+=['.dark ::selection{background:#b2378d70;color:#fff}',
'.dark :focus-visible{outline-color:#d65bb0!important}',
'.dark [data-slot="composer-host"] [contenteditable],.dark [data-slot="composer-host"] textarea{caret-color:#e77cc3}',
f'.dark [data-slot="scroll-area-thumb"]{{background:linear-gradient(180deg,{G3})!important;opacity:.45}}',
'.dark [data-slot="scroll-area-thumb"]:hover{opacity:.8}']
# --- usage & settings pages: transparent inner layers, glass header ---
r+=['.dark :is([data-workspace-area="settings"],:has(>div>header[class*="usage-header"])) :is([data-settings-page-scroll],.bg-background){background:transparent!important}',
'.dark header[class*="usage-header"]{background:#120b1ad9!important;border-bottom:1px solid #be86ce14!important;backdrop-filter:blur(16px)}']
# --- usage: used instead of left ---
C='.dark .p-4:has(>div>div>[aria-label*="% left"])'
B='.dark button[aria-label*="% left"]'
R='.dark [class*="grid-cols-subgrid"][aria-label$="% left"]'
r+=[C+'{background:#261229ce!important;border:1px solid #ba77af2e!important;border-radius:14px!important;backdrop-filter:blur(16px);box-shadow:0 4px 24px #0c061226}',
f'{C} .text-3xl,{C} .text-3xl+span>span:first-child,{R}>span:last-child{{font-size:0!important}}',
C+' .text-3xl::after{content:counter(nu) "%";font-size:1.875rem;line-height:2.25rem}',
C+' .text-3xl+span>span:first-child::after{content:"used";font-size:.875rem}',
R+'>span:last-child::after{content:counter(nu) "%";font-size:.75rem}',
B+'{transform:scaleX(-1);background:#1c0f23!important}',
f'{B}>span:not([class~="w-0.5"]),{B}>div:last-child{{transform:scaleX(-1)}}',
B+f'>div:first-child>div{{background:repeating-linear-gradient(135deg,#ffffff24 0 1px,transparent 1px 6px),linear-gradient(270deg,{G3})!important;opacity:.8}}',
B+' [class~="left-0"]{background:#1c0f23!important;opacity:1!important}',
B+' [class~="right-0"]{display:none!important}',
B+'>[class~="w-0.5"]{box-shadow:0 0 6px #f2c6ffcc}',
R+f'>span.relative{{transform:scaleX(-1);height:4px;background:linear-gradient(270deg,{G3})!important;box-shadow:0 0 8px #b2378d40}}',
R+'>span.relative>span[class~="left-0"]{background:#3a2643!important}']
# counters: " N% left" can't collide (" 5%" never matches "95%")
r+=[f':has(>*>*>[aria-label*=" {n}% left"]),[aria-label$=" {n}% left"]{{counter-reset:nu {100-n}}}' for n in range(101)]
d['css']="\n".join(r)
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
print(len(d['css']))
