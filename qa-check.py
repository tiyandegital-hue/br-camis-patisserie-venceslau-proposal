#!/usr/bin/env python3
"""QA gate for CAMIS Patisserie demo site.
Checks every page at 1440px and 390px: horizontal overflow, console
errors, failed requests, internal links, and interactive elements."""
import json, subprocess, sys, threading, time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("/home/hatch/workspace/lead-builds/br-camis-patisserie-venceslau")
PAGES = ["index.html", "cardapio.html", "ensaio.html", "conteudo.html",
         "encomendas.html", "historia.html"]
PORT = 8731

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *a):
        pass

server = ThreadingHTTPServer(("127.0.0.1", PORT), H)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.5)

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for page_file in PAGES:
        url = f"http://127.0.0.1:{PORT}/{page_file}"
        entry = {"url": url, "viewports": {}, "links": {}, "interactions": {}}
        for label, (w, h) in {"desktop": (1440, 900), "mobile": (390, 844)}.items():
            ctx = browser.new_context(viewport={"width": w, "height": h})
            pg = ctx.new_page()
            errors, failed = [], []
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("requestfailed", lambda r: failed.append(f"{r.url} :: {r.failure}"))
            pg.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 else None)
            pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(600)
            overflow = pg.evaluate(
                "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            title = pg.title()
            biz = pg.evaluate(
                "() => document.body.innerText.includes('CAMIS')")
            entry["viewports"][label] = {
                "overflow_px": overflow,
                "console_errors": errors,
                "failed_requests": failed,
                "title": title,
                "business_name_rendered": biz,
            }
            if label == "mobile":
                # burger nav
                burger = pg.query_selector(".burger")
                if burger and burger.is_visible():
                    burger.click()
                    pg.wait_for_timeout(300)
                    entry["interactions"]["burger_opens_nav"] = pg.evaluate(
                        "() => document.querySelector('.nav-links').classList.contains('open')")
                    burger.click()
            if label == "desktop":
                # internal links resolve
                hrefs = pg.evaluate(
                    "() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")
                internal = sorted({h.split('#')[0] for h in hrefs
                                   if h and not h.startswith(('http', 'mailto:', 'tel:', '#')) and h.endswith('.html')})
                link_status = {}
                for h in internal:
                    r = pg.request.get(f"http://127.0.0.1:{PORT}/{h}")
                    link_status[h] = r.status
                entry["links"] = link_status
                # page-specific interactions
                if page_file == "ensaio.html":
                    slider = pg.query_selector(".ba-slider")
                    if slider:
                        pg.evaluate(
                            "() => { const s = document.querySelector('.ba-slider');"
                            " s.value = 25; s.dispatchEvent(new Event('input', {bubbles:true})); }")
                        pg.wait_for_timeout(200)
                        entry["interactions"]["ba_slider_sets_clip"] = pg.evaluate(
                            "() => document.querySelector('.ba-after').style.clipPath")
                        entry["interactions"]["ba_slider_visible"] = pg.evaluate(
                            "() => { const r = document.querySelector('.ba-slider').getBoundingClientRect();"
                            " return r.width > 0 && r.height > 0; }")
                if page_file == "encomendas.html":
                    pg.click(".occasion[data-occasion='Casamento']")
                    pg.wait_for_timeout(200)
                    entry["interactions"]["occasion_updates_preview"] = pg.evaluate(
                        "() => document.querySelector('#msg-preview').textContent.includes('Casamento')")
                    pg.fill("#f-name", "Ana")
                    pg.wait_for_timeout(200)
                    entry["interactions"]["form_updates_preview"] = pg.evaluate(
                        "() => document.querySelector('#msg-preview').textContent.includes('Ana')")
                    faq = pg.query_selector("details summary")
                    if faq:
                        faq.click()
                        pg.wait_for_timeout(200)
                        entry["interactions"]["faq_opens"] = pg.evaluate(
                            "() => document.querySelector('details').open")
            ctx.close()
        results[page_file] = entry
    browser.close()
server.shutdown()

print(json.dumps(results, indent=2, ensure_ascii=False))
Path("/tmp/camis-qa.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
