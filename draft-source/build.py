"""Build a self-contained review copy and a conventional six-page static site."""
from pathlib import Path
from html.parser import HTMLParser
import base64,mimetypes,re,shutil,json,html as html_utils
root=Path(__file__).resolve().parent.parent
assets=root/'assets'
if not assets.exists():assets=root/'site/assets'
source=(root/'draft-source/source.html').read_text()
assessment_data=json.loads((root/'draft-source/assessments.json').read_text())
assessment_json=json.dumps(assessment_data,ensure_ascii=False).replace('<','\\u003c')
source=source.replace('<!-- assessment-data -->','<script type="application/json" id="assessment-data">'+assessment_json+'</script>')
def data_url(path):
 mime=mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
 return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
font_css=(assets/'fonts/fonts.css').read_text()
font_css=re.sub(r'url\(([^)]+)\)',lambda m:'url('+data_url(assets/'fonts'/m.group(1))+')',font_css)
preview=source.replace('<link rel="stylesheet" href="assets/fonts/fonts.css">','<style>\n'+font_css+'\n</style>')
preview=preview.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+(root/'styles.css').read_text()+'\n</style>')
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
pages={'home':('index.html','Scottish Booster Classes & Tuition | EFL Tutors'),'booster-classes':('booster-classes.html','Booster Classes, Timetable & FAQs | EFL Tutors'),'tutoring':('tutoring.html','1:1 Tutoring & Prices | EFL Tutors'),'schools-partners':('schools-partners.html','Schools & Partners | EFL Tutors'),'our-approach':('our-approach.html','Our Approach | EFL Tutors'),'resources':('resources.html','Free Subject Assessments & Resources | EFL Tutors')}
for page,(filename,title) in pages.items():
 parser=SinglePage(page);parser.feed(source)
 output=''.join(parser.parts)
 output=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',output,count=1,flags=re.S)
 (site/filename).write_text(output)
# Styles, scripts and editorial notes already live at the site root.
if assets.resolve()!=(site/'assets').resolve():shutil.copytree(assets,site/'assets',dirs_exist_ok=True)
print('Built preview.html and six static pages. Original photos are retained.')
