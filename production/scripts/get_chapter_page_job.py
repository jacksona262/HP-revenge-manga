import hashlib
import json
import sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
ch=root/'episodes/episode-01/chapter-01'
n=int(sys.argv[1])
m=json.loads((ch/'manifest.json').read_text())
p=next(p for p in m['pages'] if p['page']==n)
refs=[]
test=root/'episodes/tests/non-canon/fight-test-01-v1.png'
child=ch/'references/child-pair.png'
cast=ch/'references/supporting-cast.png'
extras=ch/'references/school-extras.png'
jackson=root/'characters/sheets/C001-jackson-anderson-hp-v2.png'
jack=root/'characters/sheets/C002-jack-davenport-hp-v2.png'
locs=json.loads((root/'canon/reference-manifest.json').read_text())['locations']
def loc(i):
    return root/next(s['output'] for s in locs if s['id']==i)
if n<=3:
    refs=[child,loc('L01'),test]
    era='FIVE YEARS EARLIER: Jackson and Jack are ten-year-old children. Use CHILD-PAIR reference for age, faces and plain fixed outfits. NO gang jackets/crests. Jackson dark tee/light trousers; Jack light tee/dark shorts and muddy shoes. Same tree, book, twig and bags. Jackson taller but no numerical child heights.'
elif n<=6:
    refs=[jackson,jack,loc('L03'),test]
    era='PRESENT DAY: Jackson age15, 6ft0, darker messy hair/observant eyes; Jack age15, 5ft8, distinct brown curls/lively softer face. Fixed opening HP varsity jackets, cream sleeves, white shirts, dark trousers and sneakers from individual references. No injuries. Two convenience-store drink cans remain the same designs.'
else:
    refs=[jackson,jack,cast]
    location='L04' if n<=12 else 'L05' if n<=14 else 'L06' if n<=18 else 'L07' if n==19 else 'L09' if n==21 else 'L08'
    refs.append(loc(location))
    if n in [13,14,17,18,22,23,24,25]: refs.append(extras)
    if n==12: refs.extend([child,loc('L01')])
    refs.append(test)
    # Imagegen accepts at most five local references. Prioritize actor identity.
    if n in [12,13,14]: refs.remove(cast)
    if len(refs)>5: refs.remove(test)
    assert len(refs)<=5
    era='PRESENT DAY: preserve Jackson (6ft0) and Jack (5ft8) identities/outfits from their individual sheets. Supporting cast guide controls Luke (light wavy hair/5ft10), Jason (younger eighth-grader/5ft2/dark curls), Ethan (brown fringe/folder) and Chris (darker swept hair/phone), in HP opening outfits. Include only the cast needed by THIS page. Teacher appears only on pages13–14. The same Student A/B pair appears only on pages17–18 and22–25; they are older students with unfamiliar abstract jacket marks, NOT HP or a named rival gang. No teacher/older bullies at other scenes. Background extras may vary from supplied ordinary faces; never clone named leads.'
    if n==12: era+=' The memory panel alone shows seven younger children: young Jackson/Jack plus five unnamed childhood friends sharing snacks, all ordinary clothing and NO gang uniforms. Other panels are present day.'
layouts={1:'Exactly ONE full-page splash: huge oak and school environment with two younger boys beneath it, quiet breathing room. Caption Five years earlier. Jack asks the sole scripted question. No response, no montage.',5:'Exactly FIVE panels. A tall introductory Jackson portrait on the right; panels2–4 stacked to its left; panel5 wide below with enough room for its four short dialogue turns.',6:'Exactly FIVE panels. Tall Jack introduction on right, dialogue/actions2–4 on left, final panel5 wide below. Generous room for the three dialogue turns in panel2.',9:'Exactly FIVE panels. Make panel4 a generous wide negotiation panel with ALL FIVE alternating short speech turns; keep the final quiet observation panel distinct.',20:'Exactly EIGHT panels: establish court first, preserve each play/pass/shot/miss/silent comedic beat separately. Final silent reaction with Jason line. No omitted or merged panels.',25:'Exactly FIVE panels. Four short escalating beat panels above, final panel5 LARGE at bottom: Jack protects Jason between himself and the older boys, Jackson approaches to intervene. No punch or resolution yet. This is the chapter cliffhanger.'}
grids={5:'TOP wide panel1; second row panel2 on RIGHT and panel3 on LEFT; third row panel4 on RIGHT and panel5 on LEFT.',6:'Top row panel1 RIGHT / panel2 LEFT; middle row panel3 RIGHT / panel4 LEFT; bottom row panel5 RIGHT / panel6 LEFT.',7:'TOP wide panel1; row2 panel2 RIGHT / panel3 LEFT; row3 panel4 RIGHT / panel5 LEFT; row4 panel6 RIGHT / panel7 LEFT.',8:'TOP wide panel1; row2 panel2 RIGHT / panel3 LEFT; row3 panel4 RIGHT / panel5 LEFT; bottom row panel6 RIGHT / panel7 MIDDLE / panel8 LEFT.'}
layout=layouts.get(n,f'Exactly {p["panels"]} separate bordered panels. '+grids.get(p['panels'],'Use explicit right-to-left order.')+' Do not rearrange the sequence by speaker position. Give crowded dialogue panels more space; no merged or extra panels.')
layout += ' CRITICAL DIALOGUE STAGING: in each conversational panel, place the FIRST speaking person on the RIGHT when feasible, with their first balloon at upper RIGHT; the response follows to LEFT or clearly BELOW. For alternating turns, use separate right-to-left rows: first right, second left, third on a lower right, fourth lower left. Never put a response at upper right before its question. A change of camera angle is allowed; physical setting/clothing stay consistent. Tails must identify the correct speaker, not the person nearest an incorrectly positioned balloon.'
prompt=f'''Use case: illustration-story. Create ONE fully finished original HP: REVENGE manga PAGE {n:03d}, Chapter 1 — The Boys Under the Tree. Portrait 2:3, maximum detail/quality, clean publication-ready black/white/grayscale inks, crisp line weights, controlled screentones, expressive subtle facial acting, rich detailed environments with readable visual hierarchy, clean white gutters. Match the APPROVED FIGHT TEST's drawing finish only; do NOT copy its combat, layout, panel numbers, header or NON-CANON footer. This page is the actual quiet Chapter 1 story. Jackson and Jack are friends: they DO NOT fight each other here. No wounds, bandages, supernatural effects or future betrayal. Neither story outcome nor dialogue may be invented.
REFERENCE ROLES: individual actor sheets/continuity boards control exact faces, hair, builds, outfits and props; location board controls geography/architecture; fight test is visual STYLE ONLY. Never reproduce reference board labels, grids or browser UI. {era}
LAYOUT: {layout} Reading order RIGHT TO LEFT, TOP TO BOTTOM; dialogue balloons within each panel follow that order and tails unmistakably point to the correct speaker. Keep stable staging, perspective, light, clothing, props and character geography. Small script panel numbers below are instructions only: DO NOT print panel numbers. Put only tiny page number {n:03d} in bottom outer margin. No decorative page titles; only page1 may add discreet chapter title without obscuring artwork.
LETTERING: Render EVERY quoted scripted dialogue line VERBATIM exactly once, using clean highly legible comic uppercase lettering (capitalization may change, words and punctuation must not). Remove quotation marks and attribution labels such as '- said Jack' / '- whispered Jackson' from printed balloons; those are speaker instructions, not page text. Whispered lines use smaller quiet/dashed balloons, readable. Unattributed short responses follow the alternating conversation context; no dropped lines. Captions only where the script explicitly requires them. No extra dialogue, narration, SFX or speech. Place balloons with generous white space before composing art; no microscopic type, clipped text, crossed tails or hidden faces. Reserve enough panel area for ALL required lines. Page must be readable as finished manga, not a thumbnail storyboard.
APPROVED SCRIPT FOR THIS PAGE — each panel and all dialogue required:
{p['script']}
FINAL CHECK REQUIREMENTS: exactly {p['panels']} panels, correct actors and temporal ages, complete accurate dialogue, legible lettering, clear reading order, plausible anatomy/hands, consistent uniforms and location. Do not skip beats or draw an unrelated fight. One page only.'''
payload={'page':n,'title':p['title'],'panels':p['panels'],'prompt':prompt,'refs':[str(r) for r in refs]}
for r in refs:
    if not r.is_file(): raise SystemExit('Missing reference '+str(r))
payload['input_hashes']={str(r):hashlib.sha256(r.read_bytes()).hexdigest() for r in refs}
(ch/'prompts'/f'page-{n:03d}.txt').write_text(prompt+'\n')
(ch/'prompts'/f'page-{n:03d}-inputs.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload))
