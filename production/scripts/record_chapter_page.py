import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
ch=root/'episodes/episode-01/chapter-01'
parser=argparse.ArgumentParser();parser.add_argument('page',type=int);parser.add_argument('image');parser.add_argument('--review',required=True);parser.add_argument('--status',default='visually_reviewed');args=parser.parse_args()
out=ch/'pages'/f'page-{args.page:03d}.png'
if out.exists():
    history=ch/'pages/versions';history.mkdir(exist_ok=True)
    v=1
    while (history/f'page-{args.page:03d}-v{v}.png').exists():v+=1
    shutil.copy2(out,history/f'page-{args.page:03d}-v{v}.png')
shutil.copy2(args.image,out)
data={'page':args.page,'status':args.status,'review':args.review,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'tool':'built-in imagegen'}
(ch/'qa'/f'page-{args.page:03d}.json').write_text(json.dumps(data,indent=2)+'\n')
m=json.loads((ch/'manifest.json').read_text());p=next(p for p in m['pages'] if p['page']==args.page);p.update(status=args.status,sha256=data['sha256']);m['generated_pages']=sum((ch/p['output']).exists() for p in m['pages']);m['reviewed_pages']=sum(p['status']=='visually_reviewed' for p in m['pages']);(ch/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
subprocess.run(['git','add','episodes/episode-01/chapter-01','production/scripts','AGENTS.md'],cwd=root,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['git','commit','-m',f'Create Chapter 1 page {args.page:03d}'],cwd=root,check=True,stdout=subprocess.DEVNULL)
print(json.dumps({'page':args.page,'output':str(out),'generated':m['generated_pages'],'reviewed':m['reviewed_pages']}))
