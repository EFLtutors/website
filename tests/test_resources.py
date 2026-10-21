"""Browser acceptance checks for the free Resources area.
Run: python tests/test_resources.py (requires Playwright and Chromium).
"""
from pathlib import Path
from threading import Thread
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from tempfile import TemporaryDirectory
from shutil import copyfile
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SUBJECTS = json.loads((ROOT / 'draft-source/assessments.json').read_text())
DIFFICULTIES = ['easy','easy','medium','medium','hard','hard']
GRADE_BANDS = ['C/D','C/D','B','B','A','A']
for subject in SUBJECTS:
 assert [q['difficulty'] for q in subject['questions']] == DIFFICULTIES
 assert [q['grade_band'] for q in subject['questions']] == GRADE_BANDS
maths_topics = [q['topic'] for q in SUBJECTS[0]['questions']]
assert 'Indices' in maths_topics and 'Circle geometry' in maths_topics
assert 'Averages' not in maths_topics and 'Probability' not in maths_topics
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self, *args): pass

def answer(page, question, right=True):
 index = question['correct'] if right else (question['correct'] + 1) % len(question['options'])
 page.get_by_role('radio').nth(index).check()
 page.locator('#assessment-next').click()

with TemporaryDirectory(prefix='efl-resources-') as isolated:
 isolated=Path(isolated)
 copyfile(ROOT/'preview.html',isolated/'preview.html')
 static_server=ThreadingHTTPServer(('127.0.0.1',8765),partial(Quiet,directory=str(ROOT)))
 preview_server=ThreadingHTTPServer(('127.0.0.1',8766),partial(Quiet,directory=str(isolated)))
 for server in [static_server,preview_server]:Thread(target=server.serve_forever,daemon=True).start()
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce',accept_downloads=True)
  errors=[];bad=[];requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:bad.append((r.url,r.status)) if r.status>=400 else None)
  page.on('request',lambda r:requests.append(r.url))
  page.goto('http://127.0.0.1:8765/quick-checks.html',wait_until='networkidle')
  assert page.locator('h1:visible').count()==1
  assert page.locator('[data-resource-category]').count()==12
  for category,count in [('Maths & Science',5),('English & Media',2),('Humanities',3),('Business & Social Sciences',2),('all',12)]:
   page.locator('#resource-category').select_option(category)
   assert page.locator('[data-resource-category]:visible').count()==count
  request_count=len(requests)
  for subject in SUBJECTS:
   page.locator('[data-start-assessment="'+subject['id']+'"]').click()
   assert page.locator('#assessment-next').is_disabled()
   assert page.locator('#assessment-back').is_disabled()
   for i,question in enumerate(subject['questions']):
    assert page.locator('#assessment-progress-label').inner_text()==f'Question {i+1} of 6'
    expected_label=question['difficulty'].title()+' · '+question['grade_band']+'-style'
    assert page.locator('#question-difficulty').inner_text()==expected_label
    if question.get('diagram')=='circle-chord':
     assert page.get_by_role('img',name='Circle and chord AB').is_visible()
    answer(page,question)
   assert page.locator('#assessment-score').inner_text()=='6 of 6 questions correct',subject['id']
   assert page.locator('.assessment-band-result p').all_text_contents()==['2 of 2 correct']*3
   assert page.locator('.answer-review-item').count()==6
   explanations=page.locator('.review-explanation').all_text_contents()
   assert explanations==[q['explanation'] for q in subject['questions']]
   assert page.locator('#assessment-support-link').get_attribute('data-route')==subject['support']
   page.locator('#choose-another-subject').click()
  assert all(url.startswith('http://127.0.0.1:8765/assets/fonts/') for url in requests[request_count:]),requests[request_count:]
  print('PASS: all 12 assessments completed; all 72 correct answers score correctly and expose the matching explanation, without answer submissions.',flush=True)
  maths=SUBJECTS[0]
  page.locator('[data-start-assessment="maths"]').click()
  for question in maths['questions']:answer(page,question,False)
  assert page.locator('#assessment-score').inner_text()=='0 of 6 questions correct'
  assert page.locator('.assessment-band-result p').all_text_contents()==['0 of 2 correct']*3
  assert page.locator('.topic-summary').nth(1).locator('li').count()==6
  page.locator('#assessment-restart').click()
  assert page.get_by_role('radio',checked=True).count()==0
  # Going back restores previous selections; changing an answer updates the final score.
  page.get_by_role('radio').nth(maths['questions'][0]['correct']).check();page.locator('#assessment-next').click()
  page.get_by_role('radio').nth((maths['questions'][1]['correct']+1)%4).check();page.locator('#assessment-back').click()
  assert page.get_by_role('radio').nth(maths['questions'][0]['correct']).is_checked()
  page.get_by_role('radio').nth((maths['questions'][0]['correct']+1)%4).check();page.locator('#assessment-next').click()
  assert page.get_by_role('radio').nth((maths['questions'][1]['correct']+1)%4).is_checked()
  page.locator('#assessment-next').click()
  for question in maths['questions'][2:]:answer(page,question)
  assert page.locator('#assessment-score').inner_text()=='4 of 6 questions correct'
  assert page.locator('.assessment-band-result p').all_text_contents()==['0 of 2 correct','2 of 2 correct','2 of 2 correct']
  page.locator('.answer-review-item').first.locator('summary').click()
  assert page.locator('.answer-review-item').first.locator('.review-correct').is_visible()
  print('PASS: zero and mixed scores, revisiting topics, back/change answers, review disclosures and restart.',flush=True)
  # The standalone copy needs no sibling files and includes the assessments when saved.
  requests.clear();page.goto('http://127.0.0.1:8766/preview.html#/quick-checks',wait_until='networkidle')
  assert requests==['http://127.0.0.1:8766/preview.html'],requests
  assert page.locator('.site-page:not([hidden])').get_attribute('data-page')=='quick-checks'
  page.locator('[data-start-assessment="english"]').click()
  for question in SUBJECTS[2]['questions']:answer(page,question)
  # Leaving a preview page clears the attempt.
  page.locator('header nav').get_by_role('link',name='Home',exact=True).click()
  page.locator('header nav').get_by_role('link',name='Quick Checks',exact=True).click()
  assert not page.locator('#free-assessment').is_visible()
  page.locator('[data-start-assessment="maths"]').click();answer(page,maths['questions'][0])
  with page.expect_download() as event:page.get_by_role('button',name='Save Website',exact=True).click()
  event.value.save_as(str(isolated/'saved.html'))
  saved_text=(isolated/'saved.html').read_text()
  assert 'assessment-data' in saved_text and 'Your answer:' not in saved_text.split('<script>',1)[0]
  page.goto('http://127.0.0.1:8766/saved.html',wait_until='networkidle')
  assert page.locator('.site-page').count()==6
  assert not page.locator('#free-assessment').is_visible()
  page.locator('[data-start-assessment="maths"]').click()
  assert page.locator('#assessment-progress-label').inner_text()=='Question 1 of 6'
  assert page.get_by_role('radio',checked=True).count()==0
  assert page.locator('.hero-image').evaluate('(e)=>e.complete && e.naturalWidth===4016')
  print('PASS: standalone resources, route reset, fresh saved attempts, all six pages and both original photos retained.',flush=True)
  for width in [360,390,768,1024,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   page.goto('http://127.0.0.1:8765/quick-checks.html',wait_until='networkidle')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('library',width)
   page.locator('[data-start-assessment="modern-studies"]').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('question',width)
   # Native radio keyboard interaction remains available.
   page.get_by_role('radio').first.focus();page.keyboard.press('Space')
   assert page.get_by_role('radio').first.is_checked()
   assert page.locator('#assessment-next').is_enabled()
   page.locator('#assessment-next').click()
   for question in SUBJECTS[8]['questions'][1:]:answer(page,question)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('feedback',width)
   assert page.locator('#assessment-results').is_visible()
   page.locator('[data-start-assessment="maths"]').click()
   for question in maths['questions'][:5]:answer(page,question)
   assert page.get_by_role('img',name='Circle and chord AB').is_visible()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('circle diagram',width)
   answer(page,maths['questions'][5])
   assert page.locator('.assessment-band-result p').all_text_contents()==['2 of 2 correct']*3
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('difficulty feedback',width)
  page.set_viewport_size({'width':390,'height':844});page.goto('http://127.0.0.1:8765/',wait_until='networkidle')
  page.get_by_role('button',name='Menu',exact=True).click();page.locator('header nav').get_by_role('link',name='Quick Checks',exact=True).click();page.wait_for_url('**/quick-checks.html')
  assert page.locator('.resource-card').count()==12
  assert not errors,errors
  assert not bad,bad
  print('PASS: library, questions and feedback fit five responsive widths; keyboard radio controls and mobile navigation work; no failed assets or JavaScript errors.',flush=True)
  browser.close()
 for server in [static_server,preview_server]:server.shutdown()
