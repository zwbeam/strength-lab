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
            context = browser.new_context()
            try:
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                response = page.goto(f'http://127.0.0.1:{server.server_port}{path}')
                assert response.status == 200
                page.wait_for_function('document.querySelector("#view").innerHTML.length > 100')
                # Deliberately no second online navigation: test a fresh installation.
                page.evaluate('navigator.serviceWorker.ready.then(() => true)')
                page.wait_for_function('navigator.serviceWorker.controller !== null')
                context.set_offline(True)
                page.reload()
                page.wait_for_function('document.querySelector("#view").innerHTML.length > 100')
                for name in ['Program', 'Workout', 'Learn', 'Log', 'Atlas', 'Settings']:
                    page.get_by_role('button', name=name, exact=True).click()
                    assert len(page.locator('#view').inner_text()) > 50, name
                page.get_by_role('button', name='Atlas', exact=True).click()
                page.wait_for_function('libraryReady === true')
                assert not errors, errors
                assert page.evaluate('document.styleSheets[0].cssRules.length > 0')
                print(f'PASS {path}: first-visit offline reload, six tabs, Atlas data, CSS, no JS errors')
            finally:
                context.close()
                server.shutdown()
                server.server_close()
                thread.join()
    finally:
        browser.close()
