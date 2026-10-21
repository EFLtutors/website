"""Render approved content records as escaped, server-free HTML at build time."""
import html
import json
import re
from urllib.parse import urlparse

def escaped(value):
    return html.escape(str(value), quote=True)

def render_testimonial(record, compact=True):
    quote = escaped(record['quote'])
    excerpt = escaped(record['excerpt'])
    full = f'<details class="full-testimonial"><summary>Read full testimonial</summary><blockquote>{quote}</blockquote></details>' if compact and excerpt != quote else ''
    body = excerpt if compact else quote
    return f'''<figure class="testimonial"><span class="review-source">Client-reported · {escaped(record['focus'])}</span><span class="quote-mark" aria-hidden="true">“</span><h3>{escaped(record['title'])}</h3><blockquote>{body}</blockquote>{full}<figcaption><strong>{escaped(record['name'])}</strong><span>{escaped(record['context'])}</span></figcaption></figure>'''

def render_team(records, full=False):
    result=[]
    for record in records:
        name=escaped(record['name']);key=escaped(record['id'])
        identity=f'<span class="tutor-initial" aria-hidden="true">{name[0]}</span>'
        if record.get('photo'):
            photo=record['photo']
            if not photo.startswith('assets/') or '..' in photo:
                raise ValueError('Team photographs must use local assets.')
            identity=f'<img class="tutor-portrait" src="{escaped(photo)}" alt="{name}, {escaped(record["role"])}" width="320" height="400" loading="lazy">'
        subjects=''
        if record['subjects']:
            subjects=f'<p class="tutor-subjects"><strong>Subjects:</strong> {escaped(", ".join(record["subjects"]))}</p>'
        if record['levels']:
            subjects+=f'<p class="tutor-subjects"><strong>Levels:</strong> {escaped(", ".join(record["levels"]))}</p>'
        credentials=''.join('<li>'+escaped(item)+'</li>' for item in record.get('credentials',[])) if full else ''
        if credentials:subjects+='<ul class="tutor-credentials">'+credentials+'</ul>'
        contact=f'<button class="text-button" data-enquiry="Tuition with {name}">Ask About Tuition with {name} →</button>' if full else f'<a class="text-link" href="our-approach.html#tutor-{key}" data-route="our-approach" data-anchor="tutor-{key}">Meet {name} →</a>'
        prefix='tutor-' if full else 'home-tutor-'
        bio=f'<p>{escaped(record["bio"] if full else record.get("summary",record["bio"]))}</p>' if full or key=='florence' else ''
        result.append(f'''<article class="named-tutor {'lead-tutor' if key=='florence' else ''}" id="{prefix}{key}"><div class="tutor-identity">{identity}<div><p class="eyebrow">{escaped(record['role'])}</p><h3>{name}</h3></div></div>{bio}{subjects}<p class="tutor-check">PVG checked</p>{contact}</article>''')
    return ''.join(result)

def expand(source, root):
    testimonials=json.loads((root/'draft-source/testimonials.json').read_text())
    team=json.loads((root/'draft-source/team.json').read_text())
    for record in testimonials:
        if record['excerpt'] not in record['quote']:
            raise ValueError('Testimonial excerpts must be verbatim passages from the full quotation.')
    def reviews(match):
        key=match.group(1)
        selected=testimonials if key=='all' else [r for r in testimonials if r['id']==key]
        if not selected:raise ValueError('Unknown testimonial '+key)
        return ''.join(render_testimonial(r,compact=key=='all') for r in selected)
    source=re.sub(r'<!-- testimonials:([a-z-]+) -->',reviews,source)
    source=source.replace('<!-- team:summary -->',render_team(team))
    source=source.replace('<!-- team:full -->',render_team(team,True))
    return source
