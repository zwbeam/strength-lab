"""Run with python3 tests/browser-smoke.py (requires Playwright and Chromium)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        executable_path='/usr/bin/chromium', args=['--no-sandbox']
    )
    try:
        for directory, path in [(ROOT, '/'), (ROOT.parent, f'/{ROOT.name}/')]:
            server = ThreadingHTTPServer(
                ('127.0.0.1', 0), partial(QuietHandler, directory=str(directory))
            )
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            context = browser.new_context(viewport={'width':390,'height':844})
            try:
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                response = page.goto(f'http://127.0.0.1:{server.server_port}{path}')
                assert response.status == 200
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.wait_for_function('document.querySelector("#app").innerHTML.length > 100')
                # Deliberately no second online navigation: test a fresh installation.
                page.evaluate('navigator.serviceWorker.ready.then(() => true)')
                page.wait_for_function('navigator.serviceWorker.controller !== null')
                context.set_offline(True)
                page.reload()
                page.wait_for_function('document.querySelector("#app").innerHTML.length > 100')
                page.on('dialog', lambda dialog: dialog.accept())
                for tab in ['today', 'progress', 'learn', 'settings']:
                    page.locator(f'[data-tab="{tab}"]').click()
                    assert len(page.locator('#app').inner_text()) > 50, tab
                # The corpus remains available behind instruction evidence, not a primary archive.
                page.locator('[data-tab="learn"]').click()
                page.locator('[data-learn-move="deadlift"]').click()
                page.locator('.source-coverage summary').click()
                page.locator('#movement-instruction [data-open-source="704"]').first.click()
                page.locator('#transcript-dialog').wait_for(state='visible')
                assert 'two hand deadlift' in page.locator('#transcript-body').inner_text().lower()
                page.get_by_role('button', name='Close', exact=True).click()
                # Internal full-text corpus search remains usable for research verification.
                assert page.evaluate("""async()=>{await loadSources();search='old idea an absolutely savage';await searchTranscriptBodies();return fullMatches.has(0);}""")
                page.locator('[data-tab="settings"]').click();(page.locator('#advanced-settings').evaluate('(el)=>el.open=true') if page.locator('#advanced-settings').count() else None)
                page.locator('#timer-mode').select_option('automatic');page.locator('#save-timer-mode').click()
                for move, weight in [('squat','12'),('press','8'),('row','12')]:
                    page.locator(f'[data-weight="{move}"]').fill(weight)
                page.locator('#save-weights').click()
                page.locator('[data-tab="today"]').click()
                page.locator('#toggle-pause').click()
                assert page.locator('#start').count() == 0
                page.locator('#toggle-pause').click()
                page.locator('#start').click()
                page.locator('[data-stage="work"]').click();page.locator('[data-editor],.partial-set,.method-fields,.notebook-exercise details').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
                page.evaluate('()=>{const b=[...document.querySelectorAll("[data-check]")].find(x=>{const [i,j]=x.dataset.check.split(":").map(Number);return !draft.items[i].sets[j].done});if(b)b.click();}')
                assert page.evaluate('draft.items.flatMap(x=>x.sets).filter(s=>s.done).length')==1
                page.reload()
                assert page.locator('[data-check="0:0"]').text_content() == '✓'
                page.get_by_role('button', name='Pause', exact=True).click()
                page.reload()
                assert page.get_by_role('button', name='Resume', exact=True).count() == 1
                page.locator('[data-editor]').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
                for checkbox in page.locator('[data-set$=":bothSides"]').all():
                    checkbox.check()
                for button in page.locator('[data-check]').all():
                    if button.inner_text() != '✓':
                        button.click()
                page.locator('[data-stage="cooldown"]').click()
                (page.locator('#finish-kind').evaluate("el=>{el.closest('details').open=true;el.value='partial';el.dispatchEvent(new Event('change',{bubbles:true}))}") if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
                assert page.evaluate('state.sessions.length') == 1
                assert page.evaluate('state.sessions[0].items.every(x=>x.completed)')
                page.reload()
                assert page.evaluate('state.sessions.length') == 1
                assert page.evaluate('draft === null')
                page.locator('#start').click()
                page.locator('[data-stage="work"]').click();page.locator('[data-editor],.partial-set,.method-fields,.notebook-exercise details').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
                page.locator('[data-set="0:0:weight"]').fill('12')
                page.locator('[data-set="0:0:weight"]').dispatch_event('change')
                page.locator('[data-check="0:0"]').evaluate('el=>el.click()')
                page.locator('[data-pain="0"]').check()
                page.locator('[data-stage="cooldown"]').click()
                (page.locator('#finish-kind').evaluate("el=>{el.closest('details').open=true;el.value='partial';el.dispatchEvent(new Event('change',{bubbles:true}))}") if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
                assert page.evaluate('E.prescription(state,"swing").mode') == 'review'
                review = page.locator('details').filter(has=page.locator('[data-resolve-pain="swing"]')).last
                page.locator('#movement-progress,#working-loads').evaluate_all('(els)=>els.forEach(el=>el.open=true)');review.locator('summary').click()
                page.locator('[data-resolve-pain="swing"]').click()
                assert page.evaluate('E.prescription(state,"swing").mode') == 'reentry'
                page.reload()
                assert page.evaluate('E.prescription(state,"swing").mode') == 'reentry'
                # The old interface remains functional, with separate untouched data.
                legacy = '{"version":1,"sessions":[],"drafts":{}}'
                page.evaluate('(v)=>localStorage.setItem("strengthlab-data-v31",v)', legacy)
                page.goto(f'http://127.0.0.1:{server.server_port}{path}legacy/index.html')
                page.wait_for_function('document.querySelector("#view").innerHTML.length > 100')
                assert page.evaluate('localStorage.getItem("strengthlab-data-v31")') == legacy
                assert not errors, errors
                assert page.evaluate('document.styleSheets[0].cssRules.length > 0')
                print(f'PASS {path}: first offline visit, reader/search, workout persistence, rest pause, bilateral completion, pain review, legacy data; no JS errors')
            finally:
                context.close()
                server.shutdown()
                server.server_close()
                thread.join()
    finally:
        browser.close()
