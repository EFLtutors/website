"""Functional checks for parent navigation, review loading and contained founder photos."""
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','booster-classes.html','tutoring.html','schools-partners.html','our-approach.html','quick-checks.html']
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
    whatsapp=page.locator('.whatsapp-float')
    assert whatsapp.is_visible()
    assert whatsapp.get_attribute('href').startswith('https://wa.me/447803375101?text=')
    assert whatsapp.get_attribute('target')=='_blank'
    box=whatsapp.bounding_box();assert box['x']>=0 and box['x']+box['width']<=width
    if page.locator('.menu-toggle').is_visible():
     page.locator('.menu-toggle').click()
     assert page.locator('#navigation').is_visible()
     page.locator('.menu-toggle').click()
  assert not external,external
  print('PASS: all six pages fit five widths; current-page and mobile navigation work; no unsolicited Google requests.',flush=True)
  # Old bookmarks continue to open the renamed page.
  page.goto('http://127.0.0.1:8778/resources.html',wait_until='networkidle')
  assert page.locator('.site-page:visible').get_attribute('data-page')=='quick-checks'
  page.goto('http://127.0.0.1:8778/preview.html#/resources',wait_until='networkidle')
  assert page.locator('.site-page:visible').get_attribute('data-page')=='quick-checks'
  for mode in ['static','preview']:
   page.goto('http://127.0.0.1:8778/'+('booster-classes.html' if mode=='static' else 'preview.html#/booster-classes'),wait_until='networkidle')
   assert page.locator('.site-page:visible a[data-route="quick-checks"]').count()>=5
   for subject in ['maths','applications-of-maths','english','physics','chemistry']:
    page.locator('.offering-check-link[data-anchor="check-'+subject+'"]').click()
    card=page.locator('#check-'+subject);assert card.is_visible()
    assert page.locator('.site-page:visible').get_attribute('data-page')=='quick-checks'
    card.locator('[data-start-assessment]').click()
    assert page.locator('#assessment-title').inner_text().endswith('Quick Check')
    page.go_back()
  page.goto('http://127.0.0.1:8778/quick-checks.html',wait_until='networkidle')
  page.locator('[data-start-assessment="maths"]').click()
  import json
  questions=json.loads((ROOT/'draft-source/assessments.json').read_text())[0]['questions']
  for q in questions:
   page.get_by_role('radio').nth(q['correct']).check();page.locator('#assessment-next').click()
  with page.expect_download() as feedback:
   page.locator('#save-check-feedback').click()
  report=Path(temp)/'feedback.txt';feedback.value.save_as(report)
  text=report.read_text()
  assert feedback.value.suggested_filename=='efl-maths-quick-check-feedback.txt'
  assert '6 of 6 questions correct' in text and 'not an exam grade' in text
  assert 'Indices' in text and 'Circle geometry' in text
  assert all(q['explanation'] in text for q in questions)
  assert 'Your answers have not been submitted to EFL Tutors.' in text
  assert not external,external
  print('PASS: WhatsApp links use the approved number; all five class-specific Quick Check links work in static and standalone copies; legacy links and feedback download work without submission.',flush=True)

  page.goto('http://127.0.0.1:8778/booster-classes.html')
  assert page.locator('.timetable tbody tr:visible').count()==7
  page.locator('#filter-subject').select_option(label='Maths')
  assert page.locator('.timetable tbody tr:visible').count()==2
  page.locator('#reset-timetable').click()
  for subject,day,time in [('Physics','Monday','18:30'),('Chemistry','Tuesday','18:00')]:
   page.locator('#filter-subject').select_option(label=subject)
   row=page.locator('.timetable tbody tr:visible')
   assert row.count()==1,(subject,'must not duplicate existing Chemistry')
   assert row.get_attribute('data-day')==day
   assert row.get_attribute('data-availability')=='open'
   assert row.locator('time').get_attribute('datetime')==time
   assert row.locator('.availability').inner_text()=='Live class'
   row.locator('[data-enquiry]').click()
   assert subject in page.locator('#class-choice').inner_text()
   assert '£75' in page.locator('#class-choice').inner_text()
   assert subject in page.locator('#enquiry-whatsapp').get_attribute('href')
   page.locator('.close-dialog').click()
  page.locator('#reset-timetable').click()
  page.locator('.timetable tbody tr').first.locator('[data-enquiry]').click()
  assert page.locator('#enquiry').is_visible()
  assert '£75' in page.locator('#class-choice').inner_text()
  page.locator('.close-dialog').click()
  page.goto('http://127.0.0.1:8778/preview.html',wait_until='networkidle')
  page.evaluate('Promise.all([...document.images].filter(i=>i.classList.contains("founder-image")).map(i=>{i.loading="eager";return i.decode();}))')
  # Both upload slots keep their fixed dimensions after full-resolution replacements.
  for kind,frame in [('hero','.hero-photo'),('portrait','.founder-photo')]:
   before=page.locator(frame).bounding_box()
   page.locator('#'+kind+'-file').set_input_files(ROOT/('assets/founder-'+('hero' if kind=='hero' else 'professional')+'.jpg'))
   page.wait_for_function('(kind)=>document.querySelector("[data-photo="+kind+"]").src.startsWith("data:image/")',arg=kind)
   after=page.locator(frame).bounding_box()
   assert before['width']==after['width'] and before['height']==after['height']
   assert page.locator(frame).evaluate('(e)=>getComputedStyle(e).overflow')=='hidden'
  assert page.locator('.founder-image').count()==2
  # A portrait updates both Florence profiles, stays contained and survives export.
  from PIL import Image
  fixture=Path(temp)/'portrait-fixture.jpg'
  Image.new('RGB',(667,1000),'#7d9cba').save(fixture)
  page.locator('#florence-file').set_input_files(fixture)
  page.wait_for_function('document.querySelectorAll(".florence-portrait").length===2')
  assert page.locator('.founder-image').count()==2
  for width in [390,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   for target in ['home','our-approach']:
    page.evaluate('(target)=>renderPage(target,"",false)',target)
    portrait=page.locator('.site-page:visible .florence-portrait')
    assert portrait.evaluate('(i)=>getComputedStyle(i).objectFit')=='contain'
    frame=portrait.locator('..').bounding_box();box=portrait.bounding_box()
    assert box['width']<=frame['width'] and box['height']<=frame['height']
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.evaluate('renderPage("home","",false)')
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
  assert saved_text.count('class="florence-portrait tutor-portrait"')==2
  assert 'data-photo="florence"' in saved_text
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
  offline=browser.new_page()
  # This managed browser blocks file://; fulfil the saved HTML without asset requests.
  offline.route('**/*',lambda route:route.fulfill(body=saved_text,content_type='text/html') if route.request.url=='http://127.0.0.1:8778/saved-copy.html' else route.abort())
  offline.goto('http://127.0.0.1:8778/saved-copy.html',wait_until='networkidle')
  assert offline.locator('.florence-portrait').count()==2
  assert offline.locator('.florence-portrait').first.evaluate('(i)=>i.naturalWidth')==667
  offline.close()
  print('PASS: timetable enquiries, original-photo uploads, review opt-in/reset and saved offline copy work; no failed local assets or JavaScript errors.',flush=True)
  page.set_viewport_size({'width':1440,'height':1000});page.goto('http://127.0.0.1:8778/index.html',wait_until='networkidle')
  page.evaluate('Promise.all([...document.images].filter(i=>i.classList.contains("founder-image")).map(i=>{i.loading="eager";return i.decode();}))')
  page.screenshot(path='/tmp/efl-home-desktop.png')
  page.locator('#testimonials').scroll_into_view_if_needed();page.screenshot(path='/tmp/efl-reviews-desktop.png')
  page.locator('#founder').scroll_into_view_if_needed();page.screenshot(path='/tmp/efl-founder-desktop.png')
  page.set_viewport_size({'width':390,'height':844});page.goto('http://127.0.0.1:8778/index.html',wait_until='networkidle');page.screenshot(path='/tmp/efl-home-mobile.png')
  browser.close()
finally:server.shutdown()
