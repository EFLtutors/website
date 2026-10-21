"""Build a self-contained review copy and a conventional six-page static site."""
from pathlib import Path
from html.parser import HTMLParser
import base64,mimetypes,re,shutil,json,html as html_utils
from content import expand
from urllib.parse import urlparse
root=Path(__file__).resolve().parent.parent
assets=root/'assets'
if not assets.exists():assets=root/'site/assets'
config=json.loads((root/'draft-source/site.json').read_text())
base=config['site_url'].rstrip('/')
if urlparse(base).scheme!='https':raise ValueError('Use an HTTPS production site URL.')
pages={
 'home':('index.html','Scottish Booster Classes & Personal Tuition | EFL Tutors','Online Booster Classes at £75 per month and personal 1:1 tutoring for S1–S6 across Scotland. Meet our PVG-checked team and find suitable support.'),
 'booster-classes':('booster-classes.html','National 5 Booster Classes · £75/month | EFL Tutors','Small-group National 5 tuition in Maths, Applications of Maths and English. See our £75 monthly price, example timetable, Quick Checks and parent FAQs.'),
 'tutoring':('tutoring.html','Personal 1:1 Tutoring & Hourly Prices | EFL Tutors','Explore individual online tutoring for National 5, Higher and Advanced Higher. View subjects and hourly prices, meet the team and ask about tutor fit.'),
 'schools-partners':('schools-partners.html','Tuition for Schools & Education Partners | EFL Tutors','Discuss a potential tuition partnership for Scottish secondary learners. Agree learning goals, support needs, safeguarding and delivery with EFL Tutors.'),
 'our-approach':('our-approach.html','Meet Our Tutors & Teaching Approach | EFL Tutors','Meet Lead Tutor Florence, Michael and Neel. Learn how EFL combines practice, understanding and confidence, with individual support and PVG-checked tutors.'),
 'quick-checks':('quick-checks.html','Free Subject Quick Checks & Feedback | EFL Tutors','Try six free subject questions with instant explanations. Save your feedback, identify a focus for practice and discuss next steps with a tutor.')
}
metadata={key:{'title':value[1],'description':value[2]} for key,value in pages.items()}
source=expand((root/'draft-source/source.html').read_text(),root)
source=source.replace('</head>','<script type="application/json" id="page-metadata">'+json.dumps(metadata,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')
form_url=config.get('enquiry_form_url')
if form_url:
 if urlparse(form_url).scheme!='https':raise ValueError('The configured enquiry form must use HTTPS.')
 source=source.replace('<div class="enquiry-routes">','<div class="enquiry-routes"><a class="button blue" href="'+html_utils.escape(form_url,quote=True)+'" target="_blank" rel="noopener">Open Enquiry Form<span class="sr-only"> (opens in a new tab)</span></a>')
socket_key=config.get('tutorcruncher_public_key')
if socket_key and not re.fullmatch(r'[a-f0-9]{20}',socket_key):raise ValueError('Invalid TutorCruncher public Socket key format.')
origin=urlparse(base).scheme+'://'+urlparse(base).netloc
socket_markup=('<section id="online-enquiry-option" class="online-enquiry-option" data-origin="'+origin+'" hidden><button id="load-online-enquiry" type="button" class="button outline full">Request a Callback Online</button><p class="form-privacy">Loads TutorCruncher and Google CAPTCHA. For subject, year-group and class details, use the WhatsApp or email options.</p><p id="online-enquiry-status" role="status"></p><iframe id="online-enquiry-frame" title="EFL Tutors online enquiry form" data-src="enquiry-widget.html" hidden></iframe></section>') if socket_key else ''
source=source.replace('<!-- tutorcruncher-enquiry -->',socket_markup)
widget=(root/'draft-source/enquiry-widget.html').read_text().replace('__PUBLIC_KEY__',socket_key or '').replace('__APP_ORIGIN__',origin)
(root/'enquiry-widget.html').write_text(widget)
assessment_data=json.loads((root/'draft-source/assessments.json').read_text())
assessment_json=json.dumps(assessment_data,ensure_ascii=False).replace('<','\\u003c')
source=source.replace('<!-- assessment-data -->','<script type="application/json" id="assessment-data">'+assessment_json+'</script>')
def data_url(path):
 mime=mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
 return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
font_css=(assets/'fonts/fonts.css').read_text()
font_css=re.sub(r'url\(([^)]+)\)',lambda m:'url('+data_url(assets/'fonts'/m.group(1))+')',font_css)
preview=source.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>').replace('<link rel="stylesheet" href="assets/fonts/fonts.css">','<style>\n'+font_css+'\n</style>')
preview=preview.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+(root/'styles.css').read_text()+'\n</style>')
preview=preview.replace('<link rel="stylesheet" href="components.css">','<style>\n'+(root/'components.css').read_text()+'\n</style>')
preview=preview.replace('<script src="script.js" defer></script>','<script>\n'+(root/'script.js').read_text()+'\n</script>')
preview=re.sub(r'\b(src|href)="(assets/[^"]+)"',lambda m:m.group(1)+'="'+data_url(assets/m.group(2).removeprefix('assets/'))+'"',preview)
preview=preview.replace('href="editorial-notes.md"','href="'+data_url(root/'editorial-notes.md')+'" download="efl-draft-notes.md"')
# Keep every preview link inside this one file, including links opened in a new tab.
def preview_link(match):
 tag=match.group()
 page=re.search(r'data-route="([^"]+)"',tag).group(1)
 anchor=re.search(r'data-anchor="([^"]+)"',tag)
 return re.sub(r'href="[^"]*"','href="#/'+page+('/'+anchor.group(1) if anchor else '')+'"',tag,count=1)
preview=re.sub(r'<a\b[^>]*\bdata-route="[^"]+"[^>]*>',preview_link,preview)
(root/'preview.html').write_text(preview)
# Each public page has only its own content, ordinary links and shared assets.
void={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class SinglePage(HTMLParser):
 def __init__(self,page):super().__init__(convert_charrefs=False);self.page=page;self.skip=0;self.parts=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if self.skip:
   if t not in void:self.skip+=1
   return
  if 'editor-only' in d.get('class','').split() or ('data-page' in d and d['data-page']!=self.page):
   if t not in void:self.skip=1
   return
  if t=='body':
   d['data-preview']='false';d['data-start-page']=self.page
   self.parts.append('<body'+''.join(' '+k+(('="'+html_utils.escape(v,quote=True)+'"') if v is not None else '') for k,v in d.items())+'>')
  elif d.get('data-page')==self.page:self.parts.append(self.get_starttag_text().replace(' hidden',''))
  else:self.parts.append(self.get_starttag_text())
 def handle_startendtag(self,t,attrs):
  if not self.skip:self.parts.append(self.get_starttag_text())
 def handle_endtag(self,t):
  if self.skip:
   if t not in void:self.skip-=1
  else:self.parts.append('</'+t+'>')
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
 def handle_entityref(self,n):
  if not self.skip:self.parts.append('&'+n+';')
 def handle_charref(self,n):
  if not self.skip:self.parts.append('&#'+n+';')
 def handle_decl(self,d):
  if not self.skip:self.parts.append('<!'+d+'>')
 def handle_comment(self,d):
  if not self.skip:self.parts.append('<!--'+d+'-->')
site=root
organisation={'@context':'https://schema.org','@type':'EducationalOrganization','name':'EFL Tutors','alternateName':'Edinburgh, Fife and Lothians Tutors','url':base+'/','email':config['contact_email'],'telephone':'+'+config['whatsapp_number'],'areaServed':'Scotland','founder':{'@type':'Person','name':'Emily Mason'}}
for page,(filename,title,description) in pages.items():
 parser=SinglePage(page);parser.feed(source)
 output=''.join(parser.parts)
 output=re.sub(r'<title>.*?</title>','<title>'+html_utils.escape(title)+'</title>',output,count=1,flags=re.S)
 output=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+html_utils.escape(description,quote=True)+'">',output,count=1)
 canonical=base+('/' if page=='home' else '/'+filename)
 tags=(f'<link rel="canonical" href="{canonical}">'
       f'<meta name="robots" content="{"index,follow" if config["indexable"] else "noindex,follow"}">'
       '<meta property="og:type" content="website"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="EFL Tutors">'
       f'<meta property="og:title" content="{html_utils.escape(title,quote=True)}"><meta property="og:description" content="{html_utils.escape(description,quote=True)}">'
       f'<meta property="og:url" content="{canonical}"><meta property="og:image" content="{base}/assets/social-preview.png">'
       '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="EFL Tutors: Practice builds understanding. Understanding builds confidence.">'
       '<meta name="twitter:card" content="summary_large_image">'
       '<script type="application/ld+json">'+json.dumps(organisation,ensure_ascii=False).replace('<','\\u003c')+'</script>')
 output=output.replace('</head>',tags+'</head>')
 # Keep originals in the standalone editor; serve efficient derivatives on public pages.
 for image in ['founder-hero','founder-professional']:
  output=output.replace('src="assets/'+image+'.jpg"', 'src="assets/'+image+'-960.webp" srcset="assets/'+image+'-480.webp 480w, assets/'+image+'-960.webp 960w, assets/'+image+'-1440.webp 1440w" sizes="(max-width: 600px) calc(100vw - 48px), (max-width: 1080px) 540px, 500px"'+(' fetchpriority="high"' if image=='founder-hero' else ''))
 (site/filename).write_text(output)
# Keep previously shared resource URLs working after the Quick Checks rename.
(site/'resources.html').write_text((site/'quick-checks.html').read_text())
# Styles, scripts and editorial notes already live at the site root.
if assets.resolve()!=(site/'assets').resolve():shutil.copytree(assets,site/'assets',dirs_exist_ok=True)
print('Built preview.html and six static pages. Original photos are retained.')

# Draft indexing is deliberately disabled until launch inputs are approved.
(site/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+base+'/sitemap.xml\n' if config['indexable'] else 'Disallow: /\n'))
urls=[base+('/' if key=='home' else '/'+value[0]) for key,value in pages.items()]
(site/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+url+'</loc></url>' for url in urls)+'</urlset>\n')
