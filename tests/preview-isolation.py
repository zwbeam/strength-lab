"""Android-sized preview at a repo subpath alongside the unchanged main app."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import importlib.util
import io,json,re,shutil,subprocess,tarfile,tempfile
from pathlib import Path
from threading import Thread
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
def open_hinge_source(page):
 if page.locator('[data-learn-move="deadlift"]').count():
  page.locator('[data-learn-move="deadlift"]').first.click()
  page.locator('.source-coverage summary').click()
  page.locator('#movement-instruction [data-open-source="704"]').first.click()
 else:
  movement=page.locator('details').filter(has=page.get_by_text('Unloaded hip-hinge practice',exact=True))
  movement.locator('summary').click();movement.locator('[data-open-source="704"]').first.click()

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('preview_builder',ROOT/'scripts/build-preview.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
with tempfile.TemporaryDirectory(prefix='strength-preview-test-') as tmp:
 site=Path(tmp)/'site';live=site/'strength-lab';live.mkdir(parents=True)
 archive=subprocess.check_output(['git','archive','origin/main'],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(live,filter='data')
 originals={str(p.relative_to(live)):p.read_bytes() for p in live.rglob('*') if p.is_file()}
 metadata=builder.build(live/'dev-preview','7e4a049')
 assert all((live/name).read_bytes()==data for name,data in originals.items())
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(site)))
 thread=Thread(target=server.serve_forever,daemon=True);thread.start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   context=browser.new_context(**p.devices['Pixel 5']);errors=[]
   root=context.new_page();root.on('dialog',lambda d:d.accept());root.goto(f'http://127.0.0.1:{server.server_port}/strength-lab/')
   root.evaluate('navigator.serviceWorker.ready.then(()=>true)');root.wait_for_function('navigator.serviceWorker.controller!==null')
   root.evaluate('''async()=>{localStorage.setItem('strengthlab-data-v31',JSON.stringify({version:1,sessions:[],drafts:{},marker:'live-only'}));localStorage.setItem('strengthlab-data-v33','live-history-sentinel');localStorage.setItem('strengthlab-draft-v33','live-draft-sentinel');localStorage.setItem('strengthlab-transaction-v33','live-journal-sentinel');await caches.open('strength-lab-live-sentinel');window.liveLock=navigator.locks.request('strengthlab-v33-writer',()=>new Promise(()=>{}));}''')
   before=root.evaluate('Object.fromEntries(Object.keys(localStorage).map(k=>[k,localStorage.getItem(k)]))')
   page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
   base=f'http://127.0.0.1:{server.server_port}/strength-lab/dev-preview/'
   page.goto(base);page.wait_for_function('storageReady && storageWritable')
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),'Preview overflows Android-sized viewport'
   assert 'Development preview' in page.locator('#development-preview').inner_text()
   assert metadata['source_commit'][:7] in page.locator('#development-preview').inner_text()
   assert page.evaluate('KEY')=='sl-dev-preview-data-v33' and page.evaluate('state.sessions.length')==0
   assert page.evaluate('navigator.serviceWorker.ready.then(r=>r.scope)')==base
   page.wait_for_function('(base)=>navigator.serviceWorker.controller?.scriptURL===base+"sw.js"',arg=base)
   worker=(live/'dev-preview/sw.js').read_text();assets=json.loads(re.search(r'const FILES=(\[.*?\]);',worker,re.S)[1])
   for asset in assets:
    response=page.request.get(urljoin(base,asset));assert response.status==200,(asset,response.status)
   manifest=page.request.get(base+'manifest.webmanifest').json()
   assert manifest['name']=='Strength Lab Development Preview' and urljoin(base,manifest['id'])==base
   assert page.request.get(base+'preview-build.json').json()==metadata
   assert 'sl-dev-preview-legacy-data-v31' in page.request.get(base+'legacy/app.js').text()
   assert 'strengthlab-data-v31' not in page.request.get(base+'legacy/app.js').text()
   keys=page.evaluate('caches.keys()');assert 'strength-lab-live-sentinel' in keys
   assert any(k.startswith('sl-dev-preview-cache-') for k in keys)
   page.locator('[data-tab="settings"]').click();page.locator('#program-block').select_option('hingePractice')
   page.get_by_text('Prerequisite skills',exact=True).click();page.locator('[data-skill="hingePattern"]').check();page.locator('#save-programming').click()
   page.locator('[data-tab="today"]').click();page.locator('#today-minutes').select_option('15');page.locator('#start').click()
   page.get_by_role('button',name=re.compile(r'Start \d+-minute warmup')).click();page.get_by_role('button',name='Pause',exact=True).click();assert page.get_by_role('button',name='Resume',exact=True).count()==1
   page.get_by_role('button',name='Warmup complete · start work').click();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)');assert page.locator('#workout-overview').count()==1
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),'Workout overview overflows viewport'
   page.locator('#workout-focus').evaluate('(el)=>el.open=true');page.get_by_role('button',name='Complete next set').click();assert page.locator('[data-check="0:0"]').inner_text()=='✓'
   page.locator('#workout-focus').evaluate('(el)=>el.open=true');page.get_by_role('button',name='Complete next set').click();page.get_by_role('button',name='Finish main work · cooldown').click();(page.locator('#finish-kind').select_option('partial') if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
   assert page.evaluate('state.sessions.length')==1
   page.locator('[data-tab="learn"]').click();open_hinge_source(page);page.locator('#transcript-dialog').wait_for(state='visible')
   assert 'two hand deadlift' in page.locator('#transcript-body').inner_text().lower();page.get_by_role('button',name='Close',exact=True).click()
   # Update only the generated preview; saved preview data and the live cache survive.
   updated=Path(tmp)/'updated-preview';new_metadata=builder.build(updated)
   assert new_metadata['source_commit']!=metadata['source_commit']
   shutil.copytree(updated,live/'dev-preview',dirs_exist_ok=True)
   page.evaluate('navigator.serviceWorker.getRegistration().then(r=>r.update()).then(()=>true)')
   page.wait_for_function('(commit)=>caches.keys().then(keys=>keys.includes("sl-dev-preview-cache-"+commit)&&keys.filter(k=>k.startsWith("sl-dev-preview-cache-")).length===1)',arg=new_metadata['source_commit'])
   page.reload();page.wait_for_function('storageReady && storageWritable')
   assert page.evaluate('state.sessions.length')==1
   assert new_metadata['source_commit'][:7] in page.locator('#development-preview').inner_text()
   assert page.evaluate('caches.keys().then(keys=>keys.includes("strength-lab-live-sentinel"))')
   # A live-site worker upgrade also must not delete the differently named preview cache.
   root.evaluate('navigator.serviceWorker.register("./sw.js?preview-coexistence=2").then(()=>true)')
   root.wait_for_function('navigator.serviceWorker.controller?.scriptURL.includes("preview-coexistence=2")')
   assert page.evaluate('caches.keys().then(keys=>keys.some(k=>k.startsWith("sl-dev-preview-cache-")))')
   context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable')
   assert page.evaluate('state.sessions.length')==1 and page.locator('#development-preview').count()==1
   page.locator('[data-tab="learn"]').click();open_hinge_source(page);page.locator('#transcript-dialog').wait_for(state='visible')
   assert 'two hand deadlift' in page.locator('#transcript-body').inner_text().lower()
   root.reload();assert 'Development Preview' not in root.title()
   after=root.evaluate('Object.fromEntries(Object.keys(localStorage).map(k=>[k,localStorage.getItem(k)]))')
   assert all(after.get(k)==v for k,v in before.items()),'Preview changed live storage'
   assert not errors,errors
   print(f'PASS: Pixel 5 emulation at /strength-lab/dev-preview/; {len(assets)} assets; manifest/version; separate live/preview keys, lock, scopes/caches and live upgrade; full overview, timers, logging, progression, source reader and offline reload')
   browser.close()
 finally:server.shutdown();server.server_close();thread.join()
