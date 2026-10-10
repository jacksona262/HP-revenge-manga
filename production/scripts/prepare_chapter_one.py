import json
import re
from pathlib import Path
root=Path(__file__).resolve().parents[2]
chapter=root/'episodes/episode-01/chapter-01'
for d in ['pages','prompts','references','qa']: (chapter/d).mkdir(parents=True,exist_ok=True)
source=(root/'canon/sources/04-volume-one-outline.md').read_text()
section=source[source.index('CHAPTER 1 —'):source.index('CHAPTER 2 —')]
(chapter/'approved-script.md').write_text(section)
chunks=re.split(r'(?m)^Page (\d+) — ',section)[1:]
pages=[]
for i in range(0,len(chunks),2):
    number=int(chunks[i]);text=chunks[i+1].replace('END OF CHAPTER 1','').strip()
    title=text.split('\n')[0]
    panel_numbers=[int(n) for n in re.findall(r'(?m)^Panel (\d+)',text)]
    panels=max(panel_numbers) if panel_numbers else 1
    pages.append({'page':number,'title':title,'script':text,'panels':panels,'status':'pending','output':f'pages/page-{number:03d}.png'})
assert [p['page'] for p in pages]==list(range(1,26))
manifest={'episode':1,'chapter':1,'title':'The Boys Under the Tree','page_count':25,'scripted_panel_count':sum(p['panels'] for p in pages),'style':'User-approved non-canon fight test; finished black/white manga','source':'canon/sources/04-volume-one-outline.md','scope':'Only pages 1–25. Test fight excluded. Chapter 2 not authorized in this run.','cast_bindings':{'Jackson':'C001 reviewed reference','Jack':'C002 reviewed reference','Luke':'HP poster / chapter continuity reference','Jason':'Detailed requested script: eighth grader, 5ft2. Youthful face and opening HP outfit recorded separately.','Ethan':'HP poster / chapter continuity reference','Chris':'The requested script explicitly uses Chris Harding; chapter-specific binding, global roster conflict retained.','Teacher':'Unnamed adult extra','Student A / Student B':'Same unnamed older pair in cafeteria and court'},'pages':pages}
(chapter/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'pages':len(pages),'panels':manifest['scripted_panel_count']}))
