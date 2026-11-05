from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text().replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844}); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html)
 for css in ['styles.css','interface-polish.css']:page.add_style_tag(content=(base/css).read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 for js in ['engine.js','app.js']:page.add_script_tag(content=(base/js).read_text())
 page.locator('[data-tab="learn"]').first.click()
 for mode,expected in [('movements','Movement library'),('principles','Programming principles'),('atlas','Complete transcript library')]:
  page.locator(f'[data-learn="{mode}"]').click()
  assert page.get_by_text(expected,exact=True).count()==1,mode
  assert page.locator('[data-learn]').count()==3,mode
 assert not errors,errors
 print('PASS Learn navigation: Movements, Principles, Atlas; no JS errors')
 b.close()
