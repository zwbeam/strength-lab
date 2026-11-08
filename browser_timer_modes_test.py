from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text().replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','').replace('<script src="session-timer.js"></script>','').replace('<script src="movement-instruction.js"></script>','').replace('<script src="learning.js"></script>','').replace('<script src="notebook.js"></script>','').replace('<script src="rolling-calendar.js"></script>','').replace('<script src="programming-education.js"></script>','')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844}); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 # A localhost origin supplies real browser Web Locks; storage remains simulated.
 page.route('http://localhost:8765/**',lambda route:route.fulfill(status=200 if route.request.url.endswith('/') else 404,body=html if route.request.url.endswith('/') else '',content_type='text/html'))
 page.goto('http://localhost:8765/')
 for css in ['styles.css','interface-polish.css']:page.add_style_tag(content=(base/css).read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 for js in ['engine.js','rolling-calendar.js','programming-education.js','session-timer.js','movement-instruction.js','learning.js','notebook.js','app.js']:page.add_script_tag(content=(base/js).read_text())
 page.get_by_role('button',name='Start workout').click()
 assert page.locator('[data-timer-mode="warmup"]').count()==1
 page.locator('[data-stage="work"]').click();page.locator('[data-editor],.partial-set,.method-fields,.notebook-exercise details').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
 assert page.locator('[data-timer-mode="work"]').count()==1
 page.evaluate('() => {for(const item of draft.items)for(const set of item.sets)if(!set.weight)set.weight=8;saveDraft();render();}')
 page.evaluate('()=>{const b=[...document.querySelectorAll("[data-check]")].find(x=>{const [i,j]=x.dataset.check.split(":").map(Number);return !draft.items[i].sets[j].done});if(b)b.click();}')
 assert page.locator('[data-timer-mode="rest"]').count()==1
 assert page.locator('section.notebook-exercise').count()>0
 page.get_by_role('button',name='Skip / clear').click()
 assert page.locator('[data-timer-mode="work"]').count()==1
 assert not errors,errors
 print('PASS: warmup, work, rest, skip transitions; full workout overview retained; no JS errors')
 browser.close()
