"""Check the resource hierarchy, Google attribution and current class labels.
All requests stay local; no reviews, messages or applications are submitted.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8792),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
  requests=[];errors=[]
  page.on('request',lambda r:requests.append(r.url));page.on('pageerror',lambda e:errors.append(str(e)))
  for start in ['index.html','preview.html#/home']:
   page.goto('http://127.0.0.1:8792/'+start,wait_until='networkidle')
   for width in [390,1440]:
    page.set_viewport_size({'width':width,'height':1000})
    for route in ['more-resources','quick-checks','blog','founder-story','become-a-tutor']:
     if page.locator('.menu-toggle').is_visible():page.locator('.menu-toggle').click()
     summary=page.locator('.nav-resource-menu summary');summary.focus();page.keyboard.press('Enter')
     assert page.locator('.nav-resource-links').is_visible()
     page.keyboard.press('Escape')
     assert not page.locator('.nav-resource-menu').evaluate('(e)=>e.open')
     # Escape may close the whole menu on mobile; reopen it to choose a child page.
     if page.locator('.menu-toggle').is_visible() and page.locator('#navigation').is_hidden():page.locator('.menu-toggle').click()
     page.locator('.nav-resource-menu summary').click()
     page.locator('header a[data-route="'+route+'"]').click()
     assert page.locator('.site-page:visible').get_attribute('data-page')==route
     assert not page.locator('.nav-resource-menu').evaluate('(e)=>e.open')
     assert page.locator('header a[aria-current="page"]').get_attribute('data-route')==route
   # Both the standalone and static copies show actual Google text without a remote widget request.
   page.goto('http://127.0.0.1:8792/'+('preview.html#/reviews' if start.startswith('preview') else 'reviews.html'),wait_until='networkidle')
   assert page.locator('.site-page:visible .google-review-card').count()==4
   for review in json.loads((ROOT/'draft-source/google-reviews.json').read_text()):
    card=page.locator('.site-page:visible .google-review-card').filter(has=page.get_by_role('link',name=review['name']+' (Google profile, opens in a new tab)',exact=True))
    assert card.count()==1
    assert card.locator('blockquote').text_content()==review['quote']
    assert card.locator('figcaption a').get_attribute('href')==review['author_url']
    assert card.get_by_role('link',name='Read on Google',exact=False).get_attribute('href')==review['source_url']
  page.goto('http://127.0.0.1:8792/index.html',wait_until='networkidle')
  assert page.locator('.google-review-card').count()==3
  page.get_by_text('How do I know that EFL Tutors is a reputable company and ensures quality private tuition?',exact=True).click()
  assert 'full refund for the lesson' in page.locator('.reputation-faq').inner_text()
  page.goto('http://127.0.0.1:8792/preview.html#/booster-classes',wait_until='networkidle')
  page.locator('#booster-value a[href="#class-timetable"]').click()
  assert page.url.endswith('#/booster-classes/class-timetable')
  page.locator('#booster-value a[data-route="quick-checks"]').click()
  assert page.locator('.site-page:visible').get_attribute('data-page')=='quick-checks'
  page.go_back()
  assert page.locator('.site-page:visible').get_attribute('data-page')=='booster-classes'
  page.goto('http://127.0.0.1:8792/booster-classes.html')
  page.locator('#filter-availability').select_option('open')
  statuses=page.locator('.timetable tbody tr:visible .availability')
  assert statuses.count()==5
  assert statuses.all_text_contents()==['Spaces available']*5
  assert statuses.first.evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(229, 243, 233)'
  assert page.locator('#booster-value .booster-benefits article').count()==6
  page.goto('http://127.0.0.1:8792/quick-checks.html')
  assert not page.locator('.resource-symbol').count()
  assert page.locator('.resource-level').all_text_contents()==['National 5']*12
  assert all(subject['level']=='National 5' for subject in json.loads((ROOT/'draft-source/assessments.json').read_text()))
  page.locator('[data-start-assessment="maths"]').click()
  assert page.locator('#assessment-title').inner_text()=='National 5 Maths Quick Check'
  assert not errors,errors
  assert all(url.startswith('http://127.0.0.1:8792/') for url in requests if url.startswith('http')),requests
  browser.close()
 sys.path.insert(0,str(ROOT/'draft-source'));from content import render_social_links
 icons=render_social_links({'social_links':{'facebook':'https://www.facebook.com/example','linkedin':'https://www.linkedin.com/company/example'}})
 assert icons.count('target="_blank"')==2 and 'social-pending' not in icons
 print('PASS: resource navigation with keyboard/mobile and standalone routes; attributed Google review text; green space labels; National 5 assessment levels; configurable social icons; no external requests or submissions.',flush=True)
finally:server.shutdown()
