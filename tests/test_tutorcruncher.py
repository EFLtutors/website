"""Exercise Socket wiring, lazy loading, fallback and frame isolation with a fake provider.
No real enquiries or CAPTCHA interactions occur. Real read-only loading is documented separately.
"""
from pathlib import Path
from urllib.parse import urlparse
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'draft-source/site.json').read_text())
ORIGIN=CONFIG['site_url'].rstrip('/')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 requests=[];provider=[];fail_script=False
 def route(r):
  global fail_script
  u=urlparse(r.request.url);requests.append((r.request.method,u.netloc,u.path))
  if r.request.method!='GET':raise AssertionError('Tests must not submit enquiries.')
  if u.netloc==urlparse(ORIGIN).netloc:
   path=ROOT/(u.path.lstrip('/') or 'index.html')
   if path.is_file():r.fulfill(path=str(path))
   else:r.fulfill(status=404,body='Not found')
  elif u.netloc=='cdn.tutorcruncher.com':
   provider.append(u.path)
   if fail_script:r.abort();return
   r.fulfill(content_type='application/javascript',body='''window.socket=async(key,options)=>{window.fixtureKey=key;window.fixtureConfig=options;document.querySelector(options.element).innerHTML='<form><label for="fixture-name">Name</label><input id="fixture-name" name="client_name" required><button type="submit">Submit Enquiry</button></form>';};''')
  else:raise AssertionError('Unexpected third-party request: '+u.netloc)
 page.route('**/*',route)
 page.goto(ORIGIN+'/booster-classes.html',wait_until='networkidle')
 assert not provider
 page.locator('.offering [data-enquiry]').first.click()
 assert page.locator('#online-enquiry-option').is_visible()
 assert page.locator('#online-enquiry-frame').get_attribute('src') is None
 page.locator('#load-online-enquiry').click()
 frame=page.frame_locator('#online-enquiry-frame')
 frame.get_by_role('textbox',name='Your name',exact=True).wait_for()
 page.wait_for_function("document.getElementById('online-enquiry-status').textContent.includes('Online form ready')")
 assert len(provider)==1
 inner=page.locator('#online-enquiry-frame').content_frame
 assert inner.locator('body').get_attribute('data-socket-key')==CONFIG['tutorcruncher_public_key']
 assert inner.locator('meta[http-equiv="Content-Security-Policy"]').count()==1
 assert inner.locator('meta[name="robots"]').get_attribute('content')=='noindex,nofollow'
 assert inner.locator('body').evaluate('()=>window.fixtureConfig.mode')=='enquiry'
 # A message from the parent window cannot impersonate a provider confirmation.
 page.evaluate("window.postMessage({type:'efl-enquiry-status',state:'submitted'},location.origin)")
 assert 'submitted' not in page.locator('#online-enquiry-status').inner_text()
 frame.locator('#fixture-name').fill('Disposable provider state')
 page.locator('.close-dialog').click()
 page.wait_for_function("document.getElementById('online-enquiry-frame').getAttribute('src')===null")
 page.locator('.offering [data-enquiry]').first.click()
 assert page.locator('#online-enquiry-frame').is_hidden()
 assert not page.locator('#load-online-enquiry').is_disabled()
 fail_script=True
 page.locator('#load-online-enquiry').click()
 page.wait_for_function("document.getElementById('online-enquiry-status').textContent.includes('unavailable')")
 assert not page.locator('#load-online-enquiry').is_disabled()
 assert page.locator('#enquiry-whatsapp').is_visible()
 assert page.locator('.email-enquiry-details summary').is_visible()
 page.keyboard.press('Escape')
 page.goto(ORIGIN+'/schools-partners.html')
 page.locator('[data-enquiry="School Partnership"]').first.click()
 assert page.locator('#online-enquiry-option').is_hidden()
 assert all(method=='GET' for method,host,path in requests)
 print('PASS: Socket loads only on request from the configured origin, uses the public key and enquiry mode, rejects spoofed status messages, clears provider state on close and keeps contact fallbacks after failure; school enquiries retain their own route.')
 browser.close()
