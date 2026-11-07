"""Real HTTP application histories: no engine calls are used to fabricate sessions.
Workout input is self-reported via the application's DOM event handlers.
"""
from datetime import datetime, timedelta, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':390,'height':844})
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('dialog',lambda dialog:dialog.accept('16') if dialog.type=='prompt' else dialog.accept())
        epoch=datetime(2026,1,1,12,tzinfo=timezone.utc)
        page.clock.install(time=epoch)
        page.goto(f'http://127.0.0.1:{server.server_port}/')
        page.locator('[data-tab="settings"]').click()
        page.locator('[data-weight="snatch"]').fill('12');page.locator('#save-weights').click()
        page.locator('#program-block').select_option('snatch')
        page.get_by_text('Prerequisite skills',exact=True).click()
        for skill in ['swing','clean','overhead']:page.locator(f'[data-skill="{skill}"]').check()
        page.locator('#save-programming').click()
        n=0
        def next_day(gap=3):
            global n
            n+=gap;page.clock.set_system_time(epoch+timedelta(days=n))
            page.locator('[data-tab="today"]').click()
        def record(quality='clean',partial=False,imbalance=False,pain=False):
            page.locator('#start').click()
            page.get_by_role('button',name='Warmup complete · start work').click();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
            # Dispatch actual input/button events. Every event rerenders, so query afresh.
            page.evaluate('''({partial,imbalance,pain,quality})=>{
              const count=document.querySelectorAll('[data-check]').length;
              for(let j=0;j<count-(partial?1:0);j++){
                for(const field of ['timingValid','bothSides']){
                  const input=document.querySelector(`[data-set="0:${j}:${field}"]`);
                  if(input){input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));}
                }
                document.querySelector(`[data-check="0:${j}"]`).click();
              }
              if(imbalance){const input=document.querySelector('[data-set="0:0:rightReps"]');input.value='4';input.dispatchEvent(new Event('change',{bubbles:true}));}
              const select=document.querySelector('[data-quality="0"]');select.value=quality;select.dispatchEvent(new Event('change',{bubbles:true}));
              if(pain){const input=document.querySelector('[data-pain="0"]');input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));}
            }''',dict(partial=partial,imbalance=imbalance,pain=pain,quality=quality))
            page.get_by_role('button',name='Finish main work · cooldown').click()
            (page.locator('#finish-kind').select_option('partial') if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
            return page.evaluate('state.sessions.at(-1).items[0]')
        def prescription(sets,reps):
            page.locator('[data-tab="today"]').click()
            text=page.locator('.list-item').first.inner_text()
            assert f'{sets} × {reps}' in text,text
        for sets in range(4,21):
            for repeat in range(2):
                next_day();prescription(sets,5)
                if sets==20 and repeat==0:
                    page.locator('#today-minutes').select_option('15');assert page.locator('#start').count()==0
                    page.locator('#today-minutes').select_option('30');assert page.locator('#start').count()==1
                    page.locator('#today-minutes').select_option('45')
                saved=record();assert saved['completed'] and saved['targetSets']==sets and saved['sourceParameters']==411
        cycle=page.locator('details').filter(has=page.locator('[data-cycle-for="snatch"]'))
        cycle.locator('summary').click();page.locator('[data-cycle-for="snatch"]').click()
        for sets,reps in [(16,6),(14,7),(12,8),(11,9),(10,10)]:
            for repeat in range(2):
                next_day();prescription(sets,reps);saved=record();assert saved['completed'] and saved['sourceParameters']==410
        assert page.evaluate('state.sessions.length')==44
        page.reload();assert page.evaluate('state.sessions.length')==44
        page.locator('[data-tab="settings"]').click()
        page.get_by_text('Recovery and scheduling defaults',exact=True).click()
        page.locator('#training-maxLoadJump').select_option('0.5');page.locator('#save-programming').click()
        page.locator('[data-tab="progress"]').click()
        movement=page.locator('details').filter(has=page.locator('[data-weight-for="snatch"]'))
        movement.locator('summary').click();page.locator('[data-weight-for="snatch"]').click()
        next_day();prescription(4,5)
        assert '16 kg' in page.locator('.list-item').first.inner_text()
        assert not record(partial=True)['completed']
        next_day();prescription(4,5);assert not record(quality='breakdown')['completed']
        next_day();prescription(3,5);saved=record();assert saved['performed'] and not saved['completed']
        next_day();prescription(4,5);saved=record(imbalance=True);assert not saved['completed'] and saved['actualReps']==4
        next_day();record(pain=True)
        page.locator('[data-tab="today"]').click();assert page.locator('#start').count()==0
        page.locator('[data-tab="progress"]').click()
        review=page.locator('details').filter(has=page.locator('[data-resolve-pain="snatch"]'))
        review.locator('summary').click();page.locator('[data-resolve-pain="snatch"]').click()
        next_day(28);prescription(2,5);saved=record();assert saved['mode']=='reentry' and not saved['completed'] and saved['sourceParameters'] is None
        next_day();prescription(4,5)
        # Scheduling must change the actual visible next workout, and survive refresh.
        page.locator('[data-tab="settings"]').click()
        page.get_by_text('Recovery and scheduling defaults',exact=True).click()
        page.locator('#training-minGapDays').select_option('3');page.locator('#save-programming').click()
        # Last training was three days ago: two days would still be held.
        page.clock.set_system_time(epoch+timedelta(days=n-1));page.reload()
        assert page.locator('#start').count()==0
        page.clock.set_system_time(epoch+timedelta(days=n));page.reload()
        assert page.locator('#start').count()==1
        assert not errors,errors
        print('PASS: 44 source-cycle sessions across 19 weeks, explicit density/load choices, partial/technique/imbalance/pain/re-entry histories, duration and calendar scheduling in the persisted HTTP application',flush=True)
        browser.close()
finally:
    server.shutdown();server.server_close();thread.join()
