"""Verify the actual HTTPS development preview (Pixel 5 emulation, not a device)."""
import argparse,json,re,os
from urllib.parse import urljoin,urlsplit,unquote
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url',required=True)
parser.add_argument('--commit',help='Expected source commit or prefix')
args=parser.parse_args();base=args.url.rstrip('/')+'/'
if urlsplit(base).scheme!='https':raise SystemExit('The deployed preview must use HTTPS')
# Browser/API requests must use the managed environment's normal HTTPS proxy.
# Preserve TLS verification and inherit the configured CA rather than bypassing it.
if not os.environ.get('NODE_EXTRA_CA_CERTS') and os.environ.get('SSL_CERT_FILE'):
 os.environ['NODE_EXTRA_CA_CERTS']=os.environ['SSL_CERT_FILE']
proxy_url=os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
network_options={}
if proxy_url:
 proxy=urlsplit(proxy_url)
 config={'server':f'{proxy.scheme}://{proxy.hostname}:{proxy.port or 80}'}
 if proxy.username:config['username']=unquote(proxy.username)
 if proxy.password:config['password']=unquote(proxy.password)
 network_options['proxy']=config
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(**p.devices['Pixel 5'],**network_options);page=context.new_page();errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)));page.on('dialog',lambda dialog:dialog.accept())
 response=page.request.get(base+'preview-build.json');assert response.status==200,('Preview metadata unavailable',response.status)
 metadata=response.json();assert metadata['channel']=='development-preview' and metadata['storage_namespace']=='sl-dev-preview'
 if args.commit:assert metadata['source_commit'].startswith(args.commit),'Stale deployed source commit'
 response=page.goto(base);assert response.status==200
 page.wait_for_function('storageReady && storageWritable')
 assert page.evaluate('KEY')=='sl-dev-preview-data-v33'
 assert metadata['source_commit'][:7] in page.locator('#development-preview').inner_text()
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),'Horizontal overflow at Android-sized viewport'
 manifest=page.request.get(base+'manifest.webmanifest').json();assert manifest['name']=='Strength Lab Development Preview' and urljoin(base,manifest['id'])==base
 worker=page.request.get(base+'sw.js');assert worker.status==200
 assets=json.loads(re.search(r'const FILES=(\[.*?\]);',worker.text(),re.S)[1])
 for asset in assets:
  url=urljoin(base,asset);assert url.startswith(base),'Asset escapes preview scope'
  r=page.request.get(url);assert r.status==200,(asset,r.status)
 page.locator('[data-tab="settings"]').click();page.locator('#program-block').select_option('hingePractice')
 page.get_by_text('Prerequisite skills',exact=True).click();page.locator('[data-skill="hingePattern"]').check();page.locator('#save-programming').click()
 page.locator('[data-tab="today"]').click();page.locator('#today-minutes').select_option('15');page.locator('#start').click()
 page.get_by_role('button',name=re.compile(r'Start \d+-minute warmup')).click();page.get_by_role('button',name='Pause',exact=True).click();page.get_by_role('button',name='Resume',exact=True).click()
 page.get_by_role('button',name='Warmup complete · start work').click();assert page.locator('#workout-overview').count()==1
 for _ in range(2):page.get_by_role('button',name='Complete next set').click()
 page.get_by_role('button',name='Finish main work · cooldown').click();page.locator('#save-workout').click()
 assert page.evaluate('state.sessions.length')==1 and page.get_by_text('Movement cycles',exact=True).count()==1
 page.locator('[data-tab="learn"]').click();assert page.locator('details').count()>20
 page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.wait_for_function('(base)=>navigator.serviceWorker.controller?.scriptURL===base+"sw.js"',arg=base)
 context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable');assert page.evaluate('state.sessions.length')==1
 page.locator('[data-tab="learn"]').click();movement=page.locator('details').filter(has=page.get_by_text('Unloaded hip-hinge practice',exact=True));movement.locator('summary').click();movement.locator('[data-open-source="704"]').first.click();page.locator('#transcript-dialog').wait_for(state='visible')
 assert 'two hand deadlift' in page.locator('#transcript-body').inner_text().lower()
 assert not errors,errors
 print(json.dumps({'result':'PASS','verified_https_url':base,'source_commit':metadata['source_commit'],'assets_verified':len(assets),'mobile_testing':'Pixel 5 Chromium emulation, not physical Android','checks':['manifest/identity','isolated data/lock','mobile layout','full overview','timers/logging','progress/settings/library','offline reload/source reader']},indent=2))
 browser.close()
