"""Build an isolated static development preview from a committed Git tree.

Does not deploy, change Pages settings or write into the original application.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
NAMESPACE='sl-dev-preview'

def git(*args):
 return subprocess.check_output(['git',*args],cwd=ROOT)

def build(output,ref='HEAD'):
 output=Path(output).resolve()
 if output==ROOT or ROOT in output.parents:
  raise ValueError('Use an empty output directory outside the repository')
 if output.exists() and any(output.iterdir()):
  raise ValueError('Output directory must be empty; existing files are never overwritten')
 commit=git('rev-parse',ref+'^{commit}').decode().strip()
 def blob(name):return git('show',f'{commit}:{name}')
 original_worker=blob('sw.js').decode()
 match=re.search(r'const FILES=(\[.*?\]);',original_worker,re.S)
 if not match:raise ValueError('Unsupported service-worker asset inventory')
 assets=json.loads(match[1])
 paths=set()
 for asset in assets:
  path=urlsplit(asset).path.removeprefix('./') or 'index.html'
  if path.startswith('/') or '..' in Path(path).parts:raise ValueError('Unsafe asset path')
  paths.add(path)
 paths.update(['index.html','app.js','engine.js','manifest.webmanifest','sw.js'])
 output.mkdir(parents=True,exist_ok=True)
 for path in sorted(paths):
  destination=output/path;destination.parent.mkdir(parents=True,exist_ok=True)
  destination.write_bytes(blob(path))
 # Keep live V31/V33 data and the live writer lock completely independent.
 replacements={
  'strengthlab-data-v33':NAMESPACE+'-data-v33',
  'strengthlab-draft-v33':NAMESPACE+'-draft-v33',
  'strengthlab-transaction-v33':NAMESPACE+'-transaction-v33',
  'strengthlab-v33-writer':NAMESPACE+'-v33-writer',
  'strengthlab-data-v31':NAMESPACE+'-legacy-data-v31',
 }
 for path in [output/'app.js',output/'legacy/app.js']:
  text=path.read_text()
  required=list(replacements)[:4] if path.name=='app.js' and path.parent==output else ['strengthlab-data-v31']
  if not all(key in text for key in required):raise ValueError('Storage contract changed; review preview isolation before publishing')
  for original,replacement in replacements.items():text=text.replace(original,replacement)
  path.write_text(text)
 manifest=json.loads((output/'manifest.webmanifest').read_text())
 manifest.update(id='./',name='Strength Lab Development Preview',short_name='Strength Lab DEV',
  description='Development preview with separate test data. Not a finished release.',start_url='./',scope='./')
 (output/'manifest.webmanifest').write_text(json.dumps(manifest,indent=2)+'\n')
 html=(output/'index.html').read_text().replace('<title>Strength Lab</title>','<title>Strength Lab · Development Preview</title>')
 banner=f'<aside id="development-preview" style="padding:12px 16px;background:#503300;color:#fff;font:600 14px/1.5 system-ui;text-align:center">Development preview · {commit[:7]}<br><small>Separate test data · not a finished release</small></aside>'
 if '<body>' not in html:raise ValueError('HTML layout changed; review development banner placement')
 html=html.replace('<body>','<body>'+banner)
 (output/'index.html').write_text(html)
 legacy=(output/'legacy/index.html').read_text().replace('<title>Strength Lab V32</title>','<title>Strength Lab DEV · Previous interface</title>')
 legacy=re.sub(r'<body([^>]*)>',lambda m:'<body'+m[1]+'>'+banner,legacy,count=1)
 (output/'legacy/index.html').write_text(legacy)
 metadata={'channel':'development-preview','source_commit':commit,'storage_namespace':NAMESPACE,
  'identity':'Strength Lab Development Preview','production_modified':False}
 (output/'preview-build.json').write_text(json.dumps(metadata,indent=2)+'\n')
 files=list(dict.fromkeys(assets+['./preview-build.json']))
 # Cache names deliberately do NOT start with strength-lab-: the live worker
 # deletes that prefix during upgrades. Preview only reads/deletes its own cache.
 worker=f'''const PREFIX={json.dumps(NAMESPACE+'-cache-')};
const CACHE=PREFIX+{json.dumps(commit)};
const FILES={json.dumps(files)};
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith(PREFIX)&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{{
 const request=event.request,url=new URL(request.url),scope=new URL(self.registration.scope);
 if(request.method!=='GET'||url.origin!==scope.origin||!url.pathname.startsWith(scope.pathname))return;
 event.respondWith(fetch(request,{{cache:'no-store'}}).then(response=>{{
  if(response.ok){{const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)));}}
  return response;
 }}).catch(async()=>{{const cache=await caches.open(CACHE);return await cache.match(request)||(request.mode==='navigate'?await cache.match('./index.html'):Response.error());}}));
}});
'''
 (output/'sw.js').write_text(worker)
 return metadata

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',required=True)
 parser.add_argument('--ref',default='HEAD',help='Committed source tree; working edits are not included')
 args=parser.parse_args()
 print(json.dumps(build(args.output,args.ref),indent=2))
