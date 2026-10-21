"""Validate contact handoff, truthful proof, public metadata and sensitive-data export.
No messages are sent and no third-party services are contacted.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from tempfile import TemporaryDirectory
from urllib.parse import urlparse,parse_qs
import json
import re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8779),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p,TemporaryDirectory(prefix='efl-contact-') as temp:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce',accept_downloads=True)
  requests=[];errors=[]
  page.on('request',lambda r:requests.append((r.method,r.url)))
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8779/booster-classes.html',wait_until='networkidle')
  page.locator('.timetable tbody tr').first.locator('[data-enquiry]').click()
  whatsapp=page.locator('#enquiry-whatsapp').get_attribute('href')
  assert parse_qs(urlparse(whatsapp).query)['text'][0].endswith('National 5 English · Sunday 2:30 pm UK time · £75/month.')
  page.locator('.email-enquiry-details summary').click()
  page.locator('#enquiry-form button[type="submit"]').click()
  assert page.locator('#enquiry-ready').is_hidden()
  page.locator('#contact-name').fill('Parent & example')
  page.locator('#contact-email').fill('invalid-email')
  page.locator('#message').fill('We would like help understanding algebra & preparing for National 5.')
  page.locator('#enquiry-form button[type="submit"]').click()
  assert page.locator('#enquiry-ready').is_hidden()
  page.locator('#contact-email').fill('')  # An email is optional when opening an email app.
  page.locator('#enquiry-form button[type="submit"]').click()
  assert page.locator('#enquiry-ready').is_visible()
  draft=urlparse(page.locator('#enquiry-email-link').get_attribute('href'));query=parse_qs(draft.query)
  assert draft.scheme=='mailto' and draft.path=='hello@edinburghfifeandlothianstutors.co.uk'
  assert 'Parent & example' in query['body'][0]
  assert 'Year group: S4' in query['body'][0]
  assert '£75/month' in query['body'][0] and 'Sunday 2:30 pm' in query['body'][0]
  assert 'Nothing has been sent' in page.locator('#enquiry-status').inner_text()
  # Force the clipboard failure path and preserve a usable manual-copy fallback.
  page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined})")
  page.locator('#copy-enquiry').click()
  assert 'Automatic copying is unavailable' in page.locator('#enquiry-status').inner_text()
  page.keyboard.press('Escape');assert not page.locator('#enquiry').is_visible()
  page.goto('http://127.0.0.1:8779/schools-partners.html')
  page.locator('[data-enquiry="School Partnership"]').first.click();page.locator('.email-enquiry-details summary').click()
  page.locator('#contact-name').fill('School contact');page.locator('#message').fill('National 5 cohort support, without pupil identifiers.')
  page.locator('#enquiry-form button[type="submit"]').click();assert page.locator('#enquiry-ready').is_hidden()
  page.locator('#school-name').fill('Example school');page.locator('#school-role').fill('Learning support');page.locator('#school-pupils').fill('12')
  page.locator('#enquiry-form button[type="submit"]').click()
  body=parse_qs(urlparse(page.locator('#enquiry-email-link').get_attribute('href')).query)['body'][0]
  assert 'Organisation: Example school' in body and 'Approximate students: 12' in body
  assert all(method=='GET' for method,url in requests)
  assert all(url.startswith('http://127.0.0.1:8779/') for method,url in requests if url.startswith('http'))
  print('PASS: parent/class and school enquiry validation, contextual WhatsApp links, encoded email drafts and manual-copy fallback; no messages submitted.',flush=True)
  page.goto('http://127.0.0.1:8779/preview.html#/home',wait_until='networkidle')
  page.locator('[data-enquiry="Help choosing tuition"]').click();page.locator('.email-enquiry-details summary').click()
  secret='PRIVATE_TEST_PARENT_94821';page.locator('#contact-name').fill(secret);page.locator('#message').fill(secret)
  page.locator('#enquiry-form button[type="submit"]').click()
  with page.expect_download() as d:page.evaluate("document.getElementById('save-website').click()")
  saved=Path(temp)/'saved.html';d.value.save_as(saved);assert secret not in saved.read_text()
  assert re.search(r'<a id="enquiry-email-link"[^>]*href="([^"]+)"',saved.read_text())[1]=='mailto:hello@edinburghfifeandlothianstutors.co.uk'
  for filename in ['index','booster-classes','tutoring','schools-partners','our-approach','quick-checks']:
   page.goto('http://127.0.0.1:8779/'+filename+'.html',wait_until='networkidle')
   assert page.title().endswith('| EFL Tutors')
   assert page.locator('link[rel="canonical"]').count()==1
   assert page.locator('meta[property="og:image"]').get_attribute('content').endswith('/assets/social-preview.png')
   assert page.locator('meta[name="robots"]').get_attribute('content')=='noindex,follow'
   assert page.locator('h1:visible').count()==1
   assert not page.locator('.editor-only').count()
   if filename=='index':
    assert '95%' not in page.locator('main').inner_text() and '65%' not in page.locator('main').inner_text()
    assert page.locator('.hero-image').get_attribute('srcset')
    assert page.locator('.portrait-image').get_attribute('loading')=='lazy'
   if filename=='our-approach':
    assert page.locator('#tutor-florence').get_by_role('heading',name='Florence',exact=True).count()==1
    assert page.locator('#tutor-michael').is_visible() and page.locator('#tutor-neel').is_visible()
  published=json.loads((ROOT/'draft-source/testimonials.json').read_text())
  assert [r['id'] for r in published]==['lauren','joanna','katie']
  for r in published:assert r['excerpt'] in r['quote']
  assert not errors,errors
  print('PASS: enquiry details excluded from saved copies; accurate profiles, verbatim evidence records, responsive images and unique public metadata remain intact.',flush=True)
  browser.close()
finally:server.shutdown()
