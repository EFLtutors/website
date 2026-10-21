const isPreview = document.body.dataset.preview === 'true';
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.getElementById('navigation');
function closeMenu() {
 menuButton.setAttribute('aria-expanded', 'false');
 navigation.classList.remove('open');
}
menuButton.addEventListener('click', () => {
 const open = menuButton.getAttribute('aria-expanded') !== 'true';
 menuButton.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open);
});
document.addEventListener('keydown',event=>{if(event.key==='Escape' && menuButton.getAttribute('aria-expanded')==='true'){closeMenu();menuButton.focus();}});
const pageNames = {home:'Home', 'booster-classes':'Booster Classes', tutoring:'1:1 Tutoring', 'schools-partners':'Schools & Partners', 'our-approach':'Our Approach', 'quick-checks':'Quick Checks'};
let currentPage = document.body.dataset.startPage || 'home';
function renderPage(page, anchor = '', moveFocus = true) {
 const panel = document.querySelector('[data-page="' + page + '"]');
 if (!panel) return;
 currentPage = page;
 window.dispatchEvent(new CustomEvent('efl-page-change', {detail:{page}}));
 document.querySelectorAll('.site-page').forEach(item => item.hidden = item !== panel);
 document.querySelectorAll('.nav-link').forEach(link => {
  if (link.dataset.route === page) link.setAttribute('aria-current', 'page');
  else link.removeAttribute('aria-current');
 });
 if (isPreview) {
  const metadata=JSON.parse(document.getElementById('page-metadata').textContent)[page];
  document.title=metadata.title;document.querySelector('meta[name="description"]').content=metadata.description;
 }
 closeMenu();
 if (moveFocus) {
  const target = anchor ? document.getElementById(anchor) : panel.querySelector('h1');
  if (target) {
   target.setAttribute('tabindex', '-1'); target.focus({preventScroll:true});
   if (anchor) target.scrollIntoView({block:'start'}); else window.scrollTo(0,0);
  }
 }
}
function routeFromLocation(moveFocus) {
 if (location.hash.startsWith('#/')) {
  const [requestedPage, anchor = ''] = location.hash.slice(2).split('/');
  const page = requestedPage === 'resources' ? 'quick-checks' : requestedPage;
  renderPage(pageNames[page] ? page : 'home', anchor, moveFocus);
 } else renderPage(currentPage, '', false);
}
if (isPreview) {
 document.addEventListener('click', event => {
  const link = event.target.closest('a[data-route]');
  if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();
  const page = link.dataset.route, anchor = link.dataset.anchor || '';
  history.pushState(null, '', '#/' + page + (anchor ? '/' + anchor : ''));
  renderPage(page, anchor);
 });
 window.addEventListener('popstate', () => routeFromLocation(true));
 window.addEventListener('hashchange', () => routeFromLocation(true));
 routeFromLocation(location.hash.startsWith('#/'));
} else renderPage(currentPage, '', false);
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));

// School-stage selector on the homepage.
const stages = {
 early:['A stronger start to secondary.','Build understanding, develop learning habits and get help with topics that aren’t clicking yet.',['Revisit the foundations','Feel more comfortable asking questions','Build confidence for what comes next']],
 middle:['Make the next step feel achievable.','Strengthen understanding as the work becomes more demanding, with S3–S6 at the heart of our specialism.',['Work through tricky topics','Connect understanding with practice','Prepare for National 5 assessments']],
 senior:['Prepare with purpose.','Deepen understanding and approach Higher and Advanced Higher study with greater confidence.',['Identify gaps in understanding','Practise applying knowledge','Develop exam preparation habits']]
};
const tabs = [...document.querySelectorAll('[data-stage]')];
function activateStage(tab) {
 tabs.forEach(button => { button.setAttribute('aria-selected', String(button === tab)); button.tabIndex = button === tab ? 0 : -1; });
 const [title, copy, items] = stages[tab.dataset.stage];
 document.getElementById('stage-title').textContent = title; document.getElementById('stage-copy').textContent = copy;
 document.getElementById('stage-list').replaceChildren(...items.map(text => {const li = document.createElement('li'); li.textContent = text; return li;}));
 document.getElementById('stage-panel').setAttribute('aria-labelledby', tab.id);
}
tabs.forEach((tab,i) => {
 tab.addEventListener('click', () => activateStage(tab));
 tab.addEventListener('keydown', event => {
  let next;
  if (event.key === 'ArrowRight') next = (i+1)%tabs.length;
  if (event.key === 'ArrowLeft') next = (i+tabs.length-1)%tabs.length;
  if (event.key === 'Home') next = 0;
  if (event.key === 'End') next = tabs.length-1;
  if (next !== undefined) {event.preventDefault();activateStage(tabs[next]);tabs[next].focus();}
 });
});

// Timetable filters use the published class rows, including confirmed science classes.
const subjectFilter = document.getElementById('filter-subject');
if (subjectFilter) {
 const dayFilter = document.getElementById('filter-day'), availabilityFilter = document.getElementById('filter-availability');
 const rows = [...document.querySelectorAll('.timetable tbody tr')];
 function filterClasses() {
  let count = 0;
  rows.forEach(row => {
   const show = (subjectFilter.value === 'all' || row.dataset.subject === subjectFilter.value) &&
    (dayFilter.value === 'all' || row.dataset.day === dayFilter.value) &&
    (availabilityFilter.value === 'all' || row.dataset.availability === availabilityFilter.value);
   row.hidden = !show; if (show) count++;
  });
  document.getElementById('class-count').textContent = count + (count === 1 ? ' class shown' : ' classes shown');
  document.getElementById('no-classes').hidden = count !== 0;
 }
 [subjectFilter,dayFilter,availabilityFilter].forEach(select => select.addEventListener('change', filterClasses));
 document.getElementById('reset-timetable').addEventListener('click', () => {
  [subjectFilter,dayFilter,availabilityFilter].forEach(select => select.value = 'all');filterClasses();
 });
}

// Enquiry handoff: existing WhatsApp and email routes, never a fake delivery receipt.
const dialog = document.getElementById('enquiry');
const form = document.getElementById('enquiry-form');
const status = document.getElementById('enquiry-status');
const ready = document.getElementById('enquiry-ready');
const emailLink = document.getElementById('enquiry-email-link');
let enquiryContext = '';
function clearEnquiryDraft() {
 ready.hidden=true;document.getElementById('enquiry-preview').value='';
 emailLink.href='mailto:hello@edinburghfifeandlothianstutors.co.uk';status.textContent='';
}
document.querySelectorAll('[data-enquiry]').forEach(button => button.addEventListener('click', () => {
 form.reset();clearEnquiryDraft();enquiryContext=button.dataset.enquiry;
 document.getElementById('enquiry-title').textContent = enquiryContext;
 const school = enquiryContext === 'School Partnership';
 document.getElementById('enquiry-intro').textContent=school?'Tell us about your learners, subject priorities and proposed support. Please avoid identifiable pupil information.':'Ask about the subject, year group and support your child needs. We’ll discuss suitable options and availability.';
 document.getElementById('school-fields').hidden = !school;document.getElementById('parent-fields').hidden = school;
 document.getElementById('school-name').required = school;
 document.getElementById('enquiry-stage').value = school ? 'School or education partner' : '';
 const choice = document.getElementById('class-choice');
 choice.textContent = button.dataset.classSlot || '';choice.hidden = !button.dataset.classSlot;
 if (button.dataset.classSlot) document.getElementById('enquiry-stage').value = 'S4';
 document.getElementById('enquiry-whatsapp').href='https://wa.me/447803375101?text='+encodeURIComponent('Hello EFL Tutors, I would like to ask about '+(button.dataset.classSlot || enquiryContext)+'.');
 dialog.showModal();document.getElementById('enquiry-title').focus();
}));
document.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('close',()=>{form.reset();clearEnquiryDraft();});
form.addEventListener('input',clearEnquiryDraft);
form.addEventListener('submit', event => {
 event.preventDefault();
 if(!form.reportValidity())return;
 const value=id=>document.getElementById(id).value.trim();
 const lines=['Hello EFL Tutors,','',enquiryContext];
 const slot=document.getElementById('class-choice');if(!slot.hidden)lines.push(slot.textContent);
 lines.push('Name: '+value('contact-name'));
 if(value('contact-email'))lines.push('Reply email: '+value('contact-email'));
 if(!document.getElementById('school-fields').hidden){
  lines.push('Organisation: '+value('school-name'));
  if(value('school-role'))lines.push('Role: '+value('school-role'));
  if(value('school-pupils'))lines.push('Approximate students: '+value('school-pupils'));
 }else if(value('enquiry-stage'))lines.push('Year group: '+value('enquiry-stage'));
 lines.push('',value('message'));
 const body=lines.join('\n');
 document.getElementById('enquiry-preview').value=body;
 emailLink.href='mailto:hello@edinburghfifeandlothianstutors.co.uk?subject='+encodeURIComponent('EFL Tutors enquiry — '+enquiryContext)+'&body='+encodeURIComponent(body);
 ready.hidden=false;
 status.textContent='Your draft is ready. Open it in your email app, or copy it and email us. Nothing has been sent.';
 emailLink.focus();
});
document.getElementById('copy-enquiry').addEventListener('click',async()=>{
 const text=document.getElementById('enquiry-preview').value;
 try{
  if(!navigator.clipboard)throw new Error('Clipboard unavailable');
  await navigator.clipboard.writeText(text);
  status.textContent='Enquiry copied. Paste it into an email to hello@edinburghfifeandlothianstutors.co.uk. Nothing has been sent.';
 }catch{
  const preview=document.getElementById('enquiry-preview');preview.focus();preview.select();
  status.textContent='Automatic copying is unavailable. Your draft is selected; copy it using your keyboard or device menu.';
 }
});

// The configured TutorCruncher widget is available only from its allowed live origin.
// A same-origin frame isolates provider state and is discarded when the dialog closes.
(() => {
 const option=document.getElementById('online-enquiry-option');if(!option)return;
 const button=document.getElementById('load-online-enquiry');
 const frame=document.getElementById('online-enquiry-frame');
 const note=document.getElementById('online-enquiry-status');
 const eligible=!isPreview && location.origin===option.dataset.origin;
 function updateAvailability(){option.hidden=!eligible || document.getElementById('enquiry-title').textContent==='School Partnership';}
 function reset(){frame.removeAttribute('src');frame.hidden=true;button.disabled=false;note.textContent='';}
 button.addEventListener('click',()=>{
  if(!eligible)return;
  button.disabled=true;frame.hidden=false;frame.src=frame.dataset.src;note.textContent='Loading the online enquiry form…';
 });
 document.querySelectorAll('[data-enquiry]').forEach(trigger=>trigger.addEventListener('click',updateAvailability));
 dialog.addEventListener('close',()=>{reset();option.hidden=true;});
 window.addEventListener('message',event=>{
  if(event.origin!==location.origin || event.source!==frame.contentWindow || !event.data)return;
  if(event.data.type==='efl-enquiry-height' && Number.isFinite(event.data.height))frame.style.height=Math.min(1800,Math.max(350,event.data.height))+'px';
  if(event.data.type==='efl-enquiry-status'){
   const states={ready:'Online form ready. Please include an email or phone number.',submitted:'Your enquiry has been submitted to EFL Tutors.',unavailable:'The online form is unavailable. Please use WhatsApp or prepare an email below.'};
   if(states[event.data.state])note.textContent=states[event.data.state];
   if(event.data.state==='unavailable')button.disabled=false;
  }
 });
})();

// Photo editing exists only in the standalone review copy.
const saveWebsite = document.getElementById('save-website');
const photoStatus = document.getElementById('photo-status');
function replacePhoto(config, image) {
 const frames = document.querySelectorAll(config.frameSelector);
 if (!frames.length) return;
 image.className = config.imageClass + (config.key === 'florence' ? ' tutor-portrait' : ' founder-image');image.dataset.photo = config.key;
 image.alt = config.alt;image.decoding = 'async';
 image.width = image.naturalWidth;image.height = image.naturalHeight;
 frames.forEach((frame,index) => {
  frame.querySelectorAll('.' + config.imageClass + ',.tutor-initial,.photo-number,.silhouette,.photo-label').forEach(node => node.remove());
  frame.prepend(index ? image.cloneNode(true) : image);frame.classList.add('has-photo');frame.removeAttribute('role');frame.removeAttribute('aria-label');
 });
 const button = document.getElementById(config.buttonId);if (button) button.textContent = config.changeLabel;
}
const photoConfigs = [
 {key:'hero',inputId:'hero-file',buttonId:'choose-hero',frameSelector:'.hero-photo',imageClass:'hero-image',alt:'Emily Mason, founder of EFL Tutors',changeLabel:'Change Hero Photo'},
 {key:'portrait',inputId:'portrait-file',buttonId:'choose-portrait',frameSelector:'.founder-photo',imageClass:'portrait-image',alt:'Professional portrait of Emily Mason',changeLabel:'Change Professional Portrait'},
 {key:'florence',inputId:'florence-file',buttonId:'choose-florence',frameSelector:'[data-tutor-photo="florence"]',imageClass:'florence-portrait',alt:'Florence, Lead Tutor',changeLabel:'Change Florence’s Portrait'}
];
async function photoFromFile(file) {
 const data = await new Promise((resolve,reject) => {const reader = new FileReader();reader.onload = () => resolve(reader.result);reader.onerror = reject;reader.readAsDataURL(file);});
 const image = new Image();image.src = data;await image.decode();return image;
}
if (isPreview && saveWebsite) {
 photoConfigs.forEach(config => {
  const input = document.getElementById(config.inputId),button = document.getElementById(config.buttonId);
  button.addEventListener('click', () => input.click());
  input.addEventListener('change', async () => {
   const file = input.files[0];if (!file) return;
   if (!['image/jpeg','image/png','image/webp','image/avif'].includes(file.type)) {photoStatus.textContent = 'Choose a JPG, PNG, WebP or AVIF photograph.';input.value='';return;}
   try {
    const image = await photoFromFile(file);replacePhoto(config,image);
    photoStatus.textContent = 'Photo added at its original resolution. Save Website to keep it.';
   } catch {photoStatus.textContent = 'That image could not be opened. Try a JPG or PNG.';} finally {input.value='';}
  });
 });
 const fit = document.getElementById('photo-fit');
 fit.addEventListener('change', () => document.querySelectorAll('.founder-image').forEach(image => image.style.objectFit = fit.value));
 document.getElementById('restore-photos').addEventListener('click', () => document.getElementById('restore-file').click());
 document.getElementById('restore-file').addEventListener('change', async event => {
  const file = event.target.files[0];if (!file) return;
  try {
   const incoming = new DOMParser().parseFromString(await file.text(),'text/html');let count=0;
   for (const config of photoConfigs) {
    const src = incoming.querySelector('.'+config.imageClass)?.getAttribute('src');
    if (!src || !/^data:image\/(jpeg|png|webp|avif);base64,[A-Za-z0-9+/=\s]+$/.test(src)) continue;
    const image = new Image();image.src=src;await image.decode();replacePhoto(config,image);count++;
   }
   photoStatus.textContent=count ? count+' photos restored. Save Website to keep them.' : 'No embedded team or founder photos were found in that file.';
  } catch {photoStatus.textContent='Unable to restore photos from that file.';} finally {event.target.value='';}
 });
 saveWebsite.addEventListener('click', () => {
  const copy=document.documentElement.cloneNode(true);
  copy.querySelector('#photo-status').textContent='';copy.querySelector('#enquiry').removeAttribute('open');copy.querySelector('#enquiry-status').textContent='';copy.querySelector('#enquiry-ready').hidden=true;copy.querySelector('#enquiry-email-link').href='mailto:hello@edinburghfifeandlothianstutors.co.uk';copy.querySelector('#enquiry-whatsapp').href='https://wa.me/447803375101';copy.querySelector('#class-choice').textContent='';copy.querySelector('#class-choice').hidden=true;
  const online=copy.querySelector('#online-enquiry-option');if(online){online.hidden=true;copy.querySelector('#online-enquiry-frame').removeAttribute('src');copy.querySelector('#online-enquiry-frame').hidden=true;copy.querySelector('#online-enquiry-status').textContent='';copy.querySelector('#load-online-enquiry').disabled=false;}
  const assessment=copy.querySelector('#free-assessment');if(assessment)assessment.hidden=true;
  ['question-options','assessment-answer-review','assessment-score','assessment-summary-copy','assessment-topics','assessment-band-results','assessment-announcement','question-prompt','question-diagram','question-difficulty'].forEach(id=>{const node=copy.querySelector('#'+id);if(node)node.textContent='';});
  const googleProfile=copy.querySelector('#google-profile');if(googleProfile){googleProfile.hidden=true;googleProfile.querySelector('iframe').removeAttribute('src');copy.querySelector('#load-google-profile').setAttribute('aria-expanded','false');copy.querySelector('#load-google-profile').textContent='Show Google Profile Here ↓';}
  copy.querySelector('#navigation').classList.remove('open');copy.querySelector('.menu-toggle').setAttribute('aria-expanded','false');
  copy.querySelectorAll('input,textarea').forEach(input=>{input.removeAttribute('value');if(input.tagName==='TEXTAREA')input.textContent='';});
  document.querySelectorAll('select[id]').forEach(select=>{const target=copy.querySelector('#'+select.id);if(target)[...target.options].forEach(option=>option.toggleAttribute('selected',option.value===(select.closest('#enquiry-form')?'':select.value)));});
  copy.querySelector('body').dataset.startPage=currentPage;
  const blob=new Blob(['<!doctype html>\n',copy.outerHTML],{type:'text/html;charset=utf-8'});
  const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='efl-tutors-complete-website.html';document.body.append(link);link.click();link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),10000);photoStatus.textContent='Complete website saved with your photos and all six pages.';
 });
}

// Free, local subject self-checks. No names, storage or network submission.
(() => {
 const dataElement = document.getElementById('assessment-data');
 if (!dataElement) return;
 const subjects = JSON.parse(dataElement.textContent);
 const difficultyNames = {easy:'Easy', medium:'Medium', hard:'Hard'};
 const difficultyLabel = question => difficultyNames[question.difficulty] + ' · ' + question.grade_band + '-style';
 const section = document.getElementById('free-assessment');
 const questionArea = document.getElementById('assessment-questions');
 const resultArea = document.getElementById('assessment-results');
 const assessmentForm = document.getElementById('assessment-form');
 const next = document.getElementById('assessment-next');
 const back = document.getElementById('assessment-back');
 const announcement = document.getElementById('assessment-announcement');
 let active = null;
 let questionIndex = 0;
 let answers = [];
 function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
 }
 function focusAndScroll(node) {
  node.setAttribute('tabindex', '-1');
  node.focus({preventScroll:true});
  node.scrollIntoView({block:'start'});
 }
 function showQuestion(moveFocus = true) {
  const question = active.questions[questionIndex];
  const label = 'Question ' + (questionIndex + 1) + ' of ' + active.questions.length;
  document.getElementById('assessment-progress-label').textContent = label;
  const difficultyBadge = document.getElementById('question-difficulty');
  difficultyBadge.className = 'difficulty-badge ' + question.difficulty;
  difficultyBadge.textContent = difficultyLabel(question);
  const progress = document.getElementById('assessment-progress');
  progress.max = active.questions.length; progress.value = questionIndex + 1;
  const prompt = document.getElementById('question-prompt');
  prompt.textContent = question.prompt;
  const diagram = document.getElementById('question-diagram');diagram.replaceChildren();
  if (question.diagram === 'circle-chord') diagram.innerHTML = '<figure class="maths-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-labelledby="circle-diagram-title circle-diagram-desc"><title id="circle-diagram-title">Circle and chord AB</title><desc id="circle-diagram-desc">Circle with centre O and radius 10 centimetres. Chord AB is 12 centimetres long. The perpendicular from O to AB is marked with a right angle. Triangle AOB is shaded.</desc><circle cx="200" cy="145" r="110" fill="#f6f8fb" stroke="#064280" stroke-width="2"/><path d="M200 145 L134 233 L266 233 Z" fill="#dce8f7" stroke="#064280" stroke-width="2"/><path d="M200 145 V233" stroke="#9b640d" stroke-width="2" stroke-dasharray="5 5"/><path d="M200 223 H210 V233" fill="none" stroke="#9b640d" stroke-width="1.5"/><circle cx="200" cy="145" r="3" fill="#064280"/><g fill="#064280" font-family="Arial,sans-serif" font-size="16"><text x="209" y="141">O</text><text x="117" y="250">A</text><text x="272" y="250">B</text><text x="115" y="180">10 cm</text><text x="178" y="278">12 cm</text></g></svg><figcaption>Diagram not to scale.</figcaption></figure>';
  const options = document.getElementById('question-options');
  options.replaceChildren();
  question.options.forEach((text, index) => {
   const choice = element('label', undefined, 'question-option');
   const radio = document.createElement('input');
   radio.type = 'radio';radio.name = 'assessment-answer';radio.value = String(index);
   radio.id = 'answer-' + active.id + '-' + questionIndex + '-' + index;
   radio.checked = answers[questionIndex] === index;
   choice.htmlFor = radio.id;
   const badge = element('span', String.fromCharCode(65 + index), 'option-letter');badge.setAttribute('aria-hidden','true');
   choice.append(radio, badge, element('span', text));
   options.append(choice);
  });
  back.disabled = questionIndex === 0;
  next.disabled = !Number.isInteger(answers[questionIndex]);
  next.textContent = questionIndex === active.questions.length - 1 ? 'See My Feedback →' : 'Next Question →';
  announcement.textContent = label;
  if (moveFocus) focusAndScroll(prompt);
 }
 function startAssessment(id) {
  const subject = subjects.find(item => item.id === id);
  if (!subject) return;
  active = subject; questionIndex = 0; answers = Array(subject.questions.length).fill(null);
  document.getElementById('assessment-title').textContent = subject.name + ' Quick Check';
  section.hidden = false;questionArea.hidden = false;resultArea.hidden = true;
  document.getElementById('assessment-answer-review').replaceChildren();
  showQuestion(false);
  focusAndScroll(document.getElementById('assessment-title'));
 }
 function showResults() {
  if (!active || answers.some(answer => !Number.isInteger(answer))) return;
  questionArea.hidden = true;resultArea.hidden = false;
  const total = active.questions.length;
  const correct = active.questions.filter((question,index) => answers[index] === question.correct).length;
  const score = document.getElementById('assessment-score');
  score.textContent = correct + ' of ' + total + ' questions correct';
  document.getElementById('assessment-summary-copy').textContent = correct === total
   ? 'All six answers were correct in this check. Explore the explanations, then consider more challenging questions with a teacher or tutor.'
   : 'Use the explanations to explore the questions that were tricky. One useful next step is to revisit a single topic together.';
  const bandResults = document.getElementById('assessment-band-results');bandResults.replaceChildren();
  for (const difficulty of ['easy','medium','hard']) {
   const indexes = active.questions.map((question,index)=>question.difficulty===difficulty?index:-1).filter(index=>index>=0);
   const bandCorrect = indexes.filter(index=>answers[index]===active.questions[index].correct).length;
   const card = element('div',undefined,'assessment-band-result '+difficulty);
   card.append(element('h4',difficultyLabel(active.questions[indexes[0]])),element('p',bandCorrect+' of '+indexes.length+' correct'));
   bandResults.append(card);
  }
  const topics = document.getElementById('assessment-topics');topics.replaceChildren();
  for (const [isCorrect, heading] of [[true,'Correct in this check'],[false,'Worth revisiting']]) {
   const box = element('div', undefined, 'topic-summary');
   box.append(element('h4',heading));
   const items = active.questions.filter((question,index) => (answers[index] === question.correct) === isCorrect);
   if (items.length) {
    const list = element('ul');items.forEach(question => list.append(element('li',question.topic)));box.append(list);
   } else box.append(element('p',isCorrect ? 'No correct answers in this short check. The explanations below are a place to start.' : 'No topics to revisit from these six questions. This does not assess the whole course.'));
   topics.append(box);
  }
  const review = document.getElementById('assessment-answer-review');review.replaceChildren();
  active.questions.forEach((question,index) => {
   const correctAnswer = answers[index] === question.correct;
   const details = element('details',undefined,'answer-review-item');
   const summary = element('summary');
   summary.append(element('span',(index+1)+'. '+question.topic+' · '+difficultyLabel(question)),element('span',correctAnswer?'Correct':'Review','answer-outcome '+(correctAnswer?'correct':'review')));
   details.append(summary,element('p',question.prompt,'review-question'));
   details.append(element('p','Your answer: '+question.options[answers[index]],'review-choice'));
   if (!correctAnswer) details.append(element('p','Correct answer: '+question.options[question.correct],'review-correct'));
   details.append(element('p',question.explanation,'review-explanation'));
   review.append(details);
  });
  const support = document.getElementById('assessment-support-link');
  const route = active.support;
  support.dataset.route = route;
  support.href = isPreview ? '#/'+route : route === 'tutoring' ? 'tutoring.html' : 'booster-classes.html';
  support.textContent = route === 'tutoring' ? 'Explore 1:1 Tutoring' : 'Explore Booster Classes';
  announcement.textContent = 'Quick Check complete. '+score.textContent+'. Feedback is ready.';
  focusAndScroll(score);
 }
 document.querySelectorAll('[data-start-assessment]').forEach(button => button.addEventListener('click',()=>startAssessment(button.dataset.startAssessment)));
 assessmentForm.addEventListener('change',event=>{
  if (event.target.name !== 'assessment-answer') return;
  answers[questionIndex] = Number(event.target.value);next.disabled = false;
 });
 assessmentForm.addEventListener('submit',event=>{
  event.preventDefault();
  if (!active || !Number.isInteger(answers[questionIndex])) return;
  if (questionIndex === active.questions.length - 1) showResults();
  else {questionIndex++;showQuestion();}
 });
 back.addEventListener('click',()=>{if (questionIndex > 0) {questionIndex--;showQuestion();}});
 document.getElementById('save-check-feedback').addEventListener('click',()=>{
  if(!active || answers.some(answer=>!Number.isInteger(answer)))return;
  const correct=active.questions.filter((q,i)=>answers[i]===q.correct).length;
  const revisit=active.questions.filter((q,i)=>answers[i]!==q.correct).map(q=>'• '+q.topic);
  const lines=[
   'EFL Tutors — '+active.name+' Quick Check',
   'Saved: '+new Date().toLocaleString('en-GB'),
   correct+' of '+active.questions.length+' questions correct',
   'This is a snapshot of these six questions, not an exam grade.',
   '', 'Topics worth revisiting:',
   ...(revisit.length?revisit:['No topics to revisit from these six questions. Try fresh questions with a tutor to explore further.']),
   '', 'Your answers and explanations:'
  ];
  active.questions.forEach((q,i)=>lines.push('',(i+1)+'. '+q.topic+' — '+(answers[i]===q.correct?'Correct':'Worth revisiting'),q.prompt,'Your answer: '+q.options[answers[i]],'Correct answer: '+q.options[q.correct],q.explanation));
  lines.push('','Next step: share this feedback with a tutor and choose a focus for practice. Review understanding with fresh questions and lesson work. Repeating this check uses the same questions.','Your answers have not been submitted to EFL Tutors. This file is your own copy.');
  const url=URL.createObjectURL(new Blob([lines.join('\n')],{type:'text/plain;charset=utf-8'}));
  const link=document.createElement('a');link.href=url;link.download='efl-'+active.id+'-quick-check-feedback.txt';document.body.append(link);link.click();link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),10000);
  announcement.textContent='Your Quick Check feedback file is ready to save. Nothing has been sent to EFL Tutors.';
 });
 document.getElementById('assessment-restart').addEventListener('click',()=>{if(active)startAssessment(active.id);});
 document.getElementById('choose-another-subject').addEventListener('click',()=>{
  active = null;answers = [];section.hidden = true;
  focusAndScroll(document.querySelector('#assessment-library h2'));
 });
 const category = document.getElementById('resource-category');
 category.addEventListener('change',()=>{
  let count = 0;
  document.querySelectorAll('[data-resource-category]').forEach(card=>{
   const show = category.value === 'all' || card.dataset.resourceCategory === category.value;
   card.hidden = !show;if(show)count++;
  });
  document.getElementById('resource-count').textContent = count + ' subject Quick Check' + (count === 1 ? '' : 's');
 });
 window.addEventListener('efl-page-change',event=>{
  if (event.detail.page !== 'quick-checks') {active = null;answers = [];section.hidden = true;}
 });
})();


// Load Google's official business profile only when a parent chooses to open it.
// Keep the source rating dated; this is not an automatic review feed.
(() => {
 const button=document.getElementById('load-google-profile');
 const profile=document.getElementById('google-profile');
 if(!button || !profile)return;
 const frame=profile.querySelector('iframe');
 function closeProfile(){
  frame.removeAttribute('src');profile.hidden=true;
  button.setAttribute('aria-expanded','false');button.textContent='Show Google Profile Here ↓';
 }
 button.addEventListener('click',()=>{
  if(!profile.hidden){closeProfile();return;}
  profile.hidden=false;frame.src=frame.dataset.src;
  button.setAttribute('aria-expanded','true');button.textContent='Hide Google Profile ↑';
 });
 window.addEventListener('efl-page-change',closeProfile);
})();
