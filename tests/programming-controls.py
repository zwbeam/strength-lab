"""Exercise heavy/light, matched-pair and club programming via real application UI."""
from datetime import datetime,timedelta,timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':390,'height':844});errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)));page.on('dialog',lambda dialog:dialog.accept())
    epoch=datetime(2026,7,1,12,tzinfo=timezone.utc);page.clock.install(time=epoch)
    page.goto(f'http://127.0.0.1:{server.server_port}/')
    def settings():page.locator('[data-tab="settings"]').click()
    def train():page.locator('[data-tab="today"]').click()
    def details_for(selector):
        details=page.locator('details').filter(has=page.locator(selector))
        if details.get_attribute('open') is None:details.locator(':scope > summary').click()
    def save_program():page.locator('#save-programming').click()
    def perform():
        page.locator('#start').click();page.get_by_role('button',name='Warmup complete · start work').click();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
        page.evaluate('''()=>{
          const indexes=Array.from(document.querySelectorAll('[data-check]')).map(button=>button.dataset.check);
          for(const index of indexes){
            for(const field of ['timingValid','bothSides']){const el=document.querySelector(`[data-set="${index}:${field}"]`);if(el){el.checked=true;el.dispatchEvent(new Event('change',{bubbles:true}));}}
            document.querySelector(`[data-check="${index}"]`).click();
          }
        }''')
        page.get_by_role('button',name='Finish main work · cooldown').click();(page.locator('#finish-kind').select_option('partial') if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
        assert page.evaluate('state.sessions.at(-1).items.every(item=>item.completed)')
    settings()
    for field in page.locator('[data-weight]').all():
        movement=field.get_attribute('data-weight');
        if field.get_attribute('readonly') is not None:continue
        field.fill('5' if movement in ['front','cast','circles'] else '8' if movement=='press' else '12')
    page.locator('#save-weights').click()
    details_for('[data-program-profile="press"]')
    page.locator('[data-program-profile="press"]').select_option('wave');page.locator('[data-wave-light="press"]').fill('8');page.locator('[data-wave-heavy="press"]').fill('12');page.locator('[data-wave-reps="press"]').fill('2')
    save_program()
    for n in range(6):
        page.clock.set_system_time(epoch+timedelta(days=2*n));train()
        if n in [0,3]:
            text=page.locator('.list-item').filter(has_text='Single-arm strict press').inner_text()
            assert ('2 × 5' in text and '8 kg' in text) if n==0 else ('3 × 2' in text and '12 kg' in text),text
        perform()
    settings();page.locator('#program-block').select_option('double');save_program();train()
    assert page.locator('#start').count()==0
    settings();details_for('[data-skill="rack"]')
    for skill in ['rack','doublePress','doubleSquat']:page.locator(f'[data-skill="{skill}"]').check()
    save_program();train();assert page.locator('#start').count()==0 # pair still unconfirmed
    settings();page.locator('[data-equipment="pairs"]').fill('12');page.locator('#save-equipment').click()
    train();page.locator('#today-minutes').select_option('20')
    assert page.locator('.list-item').count()==1
    assert 'Double clean and press' in page.locator('.list-item').inner_text()
    perform();train()
    assert 'Double front squat' in page.locator('.list-item').first.inner_text()
    perform()
    settings();page.locator('#program-block').select_option('club')
    for movement in ['front','cast','circles']:
        details_for(f'[data-program-profile="{movement}"]')
        page.locator(f'[data-program-profile="{movement}"]').select_option('club')
        page.locator(f'[data-program-seconds="{movement}"]').select_option('15')
        page.locator(f'[data-club-start="{movement}"]').fill('1');page.locator(f'[data-club-end="{movement}"]').fill('4');page.locator(f'[data-club-rest="{movement}"]').select_option('90')
    save_program();train()
    assert all('1 × 15 sec' in text for text in page.locator('.list-item').all_text_contents())
    perform();page.reload()
    assert page.evaluate('state.sessions.at(-1).items.every(item=>item.profile==="club"&&item.sourceParameters===null)')
    before=page.evaluate('JSON.stringify(state)')
    train();page.locator('#start').click();settings()
    page.locator('#program-block').select_option('snatch');save_program()
    page.locator('#save-weights').click();page.locator('#save-equipment').click()
    assert page.evaluate('JSON.stringify(state)')==before
    assert page.evaluate('draft !== null')
    train();page.locator('#discard').click();settings()
    page.locator('[data-equipment="pairs"]').fill('99');page.locator('#save-equipment').click()
    assert page.evaluate('JSON.stringify(state)')==before
    assert not errors,errors
    print('PASS: six real ABC workouts with light/heavy prescriptions; skill/pair gates; 20-minute whole-movement carryover; saved timed club block')
    browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
