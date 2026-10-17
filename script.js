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
const pageNames = {home:'Home', 'booster-classes':'Booster Classes', tutoring:'1:1 Tutoring', 'schools-partners':'Schools & Partners', 'our-approach':'Our Approach'};
let currentPage = document.body.dataset.startPage || 'home';
function renderPage(page, anchor = '', moveFocus = true) {
 const panel = document.querySelector('[data-page="' + page + '"]');
 if (!panel) return;
 currentPage = page;
 document.querySelectorAll('.site-page').forEach(item => item.hidden = item !== panel);
 document.querySelectorAll('.nav-link').forEach(link => {
  if (link.dataset.route === page) link.setAttribute('aria-current', 'page');
  else link.removeAttribute('aria-current');
 });
 document.title = pageNames[page] + ' | EFL Tutors';
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
  const [page, anchor = ''] = location.hash.slice(2).split('/');
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

// Timetable filters preserve the original six distinct classes.
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

// Preview enquiries: no requests or messages are sent.
const dialog = document.getElementById('enquiry');
const form = document.getElementById('enquiry-form');
const status = document.getElementById('enquiry-status');
document.querySelectorAll('[data-enquiry]').forEach(button => button.addEventListener('click', () => {
 form.reset();status.textContent = '';
 document.getElementById('enquiry-title').textContent = button.dataset.enquiry;
 const school = button.dataset.enquiry === 'School Partnership';
 document.getElementById('school-fields').hidden = !school;document.getElementById('parent-fields').hidden = school;
 document.getElementById('school-name').required = school;
 document.getElementById('enquiry-stage').value = school ? 'School or education partner' : '';
 const choice = document.getElementById('class-choice');
 choice.textContent = button.dataset.classSlot || '';choice.hidden = !button.dataset.classSlot;
 if (button.dataset.classSlot) document.getElementById('enquiry-stage').value = 'S4';
 dialog.showModal();
}));
document.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
form.addEventListener('submit', event => {
 event.preventDefault();status.textContent = 'Preview complete. Your enquiry has not been sent. Use the consultation link or email on the page to contact EFL Tutors.';
});

// Photo editing exists only in the standalone review copy.
const saveWebsite = document.getElementById('save-website');
const photoStatus = document.getElementById('photo-status');
function replacePhoto(config, image) {
 const frame = document.querySelector(config.frameSelector);
 if (!frame) return;
 image.className = config.imageClass + ' founder-image';image.dataset.photo = config.key;
 image.alt = config.alt;image.decoding = 'async';
 image.width = image.naturalWidth;image.height = image.naturalHeight;
 frame.querySelectorAll('.' + config.imageClass + ',.photo-number,.silhouette,.photo-label').forEach(node => node.remove());
 frame.prepend(image);frame.classList.add('has-photo');frame.removeAttribute('role');frame.removeAttribute('aria-label');
 const button = document.getElementById(config.buttonId);if (button) button.textContent = config.changeLabel;
}
const photoConfigs = [
 {key:'hero',inputId:'hero-file',buttonId:'choose-hero',frameSelector:'.hero-photo',imageClass:'hero-image',alt:'Emily Mason, founder of EFL Tutors',changeLabel:'Change Hero Photo'},
 {key:'portrait',inputId:'portrait-file',buttonId:'choose-portrait',frameSelector:'.founder-photo',imageClass:'portrait-image',alt:'Professional portrait of Emily Mason',changeLabel:'Change Professional Portrait'}
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
   photoStatus.textContent=count ? count+' photos restored. Save Website to keep them.' : 'No embedded founder photos were found in that file.';
  } catch {photoStatus.textContent='Unable to restore photos from that file.';} finally {event.target.value='';}
 });
 saveWebsite.addEventListener('click', () => {
  const copy=document.documentElement.cloneNode(true);
  copy.querySelector('#photo-status').textContent='';copy.querySelector('#enquiry').removeAttribute('open');copy.querySelector('#enquiry-status').textContent='';
  copy.querySelector('#navigation').classList.remove('open');copy.querySelector('.menu-toggle').setAttribute('aria-expanded','false');
  copy.querySelectorAll('input,textarea').forEach(input=>{input.removeAttribute('value');if(input.tagName==='TEXTAREA')input.textContent='';});
  document.querySelectorAll('select[id]').forEach(select=>{const target=copy.querySelector('#'+select.id);if(target)[...target.options].forEach(option=>option.toggleAttribute('selected',option.value===select.value));});
  copy.querySelector('body').dataset.startPage=currentPage;
  const blob=new Blob(['<!doctype html>\n',copy.outerHTML],{type:'text/html;charset=utf-8'});
  const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='efl-tutors-complete-website.html';document.body.append(link);link.click();link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),10000);photoStatus.textContent='Complete website saved with both photos and all five pages.';
 });
}
