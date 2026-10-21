"""Functional checks for parent navigation, review loading and contained founder photos."""
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','booster-classes.html','tutoring.html','schools-partners.html','our-approach.html','resources.html']
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8778),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p, TemporaryDirectory(prefix='efl-review-') as temp:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce')
  errors=[];external=[];bad=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
  page.on('request',lambda r:external.append(r.url) if r.url.startswith('http') and not r.url.startswith('http://127.0.0.1:8778/') else None)
  for width in [360,390,768,1024,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   for filename in PAGES:
    page.goto('http://127.0.0.1:8778/'+filename,wait_until='networkidle')
    assert page.locator('h1:visible').count()==1,filename
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,filename)
    assert page.locator('.nav-link[aria-current="page"]').count()==1
    if page.locator('.menu-toggle').is_visible():
     page.locator('.menu-toggle').click()
     assert page.locator('#navigation').is_visible()
     page.locator('.menu-toggle').click()
  assert not external,external
  print('PASS: all six pages fit five widths; current-page and mobile navigation work; no unsolicited Google requests.',flush=True)
  page.goto('http://127.0.0.1:8778/booster-classes.html')
  assert page.locator('.timetable tbody tr:visible').count()==6
  page.locator('#filter-subject').select_option(label='Maths')
  assert page.locator('.timetable tbody tr:visible').count()==2
  page.locator('#reset-timetable').click()
  page.locator('.timetable tbody tr').first.locator('[data-enquiry]').click()
  assert page.locator('#enquiry').is_visible()
  assert '£75' in page.locator('#class-choice').inner_text()
  page.locator('.close-dialog').click()
  page.goto('http://127.0.0.1:8778/preview.html',wait_until='networkidle')
  page.evaluate('Promise.all([...document.images].filter(i=>i.classList.contains("founder-image")).map(i=>i.decode()))')
  # Both upload slots keep their fixed dimensions after full-resolution replacements.
  for kind,frame in [('hero','.hero-photo'),('portrait','.founder-photo')]:
   before=page.locator(frame).bounding_box()
   page.locator('#'+kind+'-file').set_input_files(ROOT/('assets/founder-'+('hero' if kind=='hero' else 'professional')+'.jpg'))
   page.wait_for_function('(kind)=>document.querySelector("[data-photo="+kind+"]").src.startsWith("data:image/")',arg=kind)
   after=page.locator(frame).bounding_box()
   assert before['width']==after['width'] and before['height']==after['height']
   assert page.locator(frame).evaluate('(e)=>getComputedStyle(e).overflow')=='hidden'
  assert page.locator('.founder-image').count()==2
  profile=page.locator('#google-profile')
  assert profile.is_hidden() and profile.locator('iframe').get_attribute('src') is None
  # Intercept the explicit third-party request so this check is deterministic and offline.
  page.route('https://www.google.com/**',lambda r:r.fulfill(body='<p>EFL Google profile test fixture</p>',content_type='text/html'))
  page.locator('#load-google-profile').click()
  assert profile.is_visible()
  assert 'cid=12299693131977025457' in profile.locator('iframe').get_attribute('src')
  assert page.locator('#load-google-profile').get_attribute('aria-expanded')=='true'
  with page.expect_download() as download:
   page.locator('#save-website').click()
  saved=Path(temp)/'saved.html';download.value.save_as(saved)
  saved_text=saved.read_text()
  assert '<div class="google-profile" id="google-profile" hidden' in saved_text
  assert not re.search(r'<iframe[^>]*\ssrc=',saved_text)
  page.locator('#navigation a[data-route="our-approach"]').click()
  assert page.locator('[data-page="our-approach"]').is_visible()
  assert profile.is_hidden() and profile.locator('iframe').get_attribute('src') is None
  # Review anchor remains reachable after navigating to a different page.
  page.locator('footer a[data-anchor="testimonials"]').click()
  assert page.locator('#testimonials').is_visible()
  assert not errors,errors
  assert not bad,bad
  print('PASS: timetable enquiries, original-photo uploads, review opt-in/reset and saved offline copy work; no failed local assets or JavaScript errors.',flush=True)
  page.set_viewport_size({'width':1440,'height':1000});page.goto('http://127.0.0.1:8778/index.html',wait_until='networkidle')
  page.evaluate('Promise.all([...document.images].filter(i=>i.classList.contains("founder-image")).map(i=>i.decode()))')
  page.screenshot(path='/tmp/efl-home-desktop.png')
  page.locator('#testimonials').scroll_into_view_if_needed();page.screenshot(path='/tmp/efl-reviews-desktop.png')
  page.locator('#founder').scroll_into_view_if_needed();page.screenshot(path='/tmp/efl-founder-desktop.png')
  page.set_viewport_size({'width':390,'height':844});page.goto('http://127.0.0.1:8778/index.html',wait_until='networkidle');page.screenshot(path='/tmp/efl-home-mobile.png')
  browser.close()
finally:server.shutdown()
