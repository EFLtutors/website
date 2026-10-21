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
        if record['id']=='florence':
            identity=f'<div class="tutor-photo-slot {"has-photo" if record.get("photo") else ""}" data-tutor-photo="florence">{identity}</div>'
        subjects=''
        if record['subjects']:
            subjects=f'<p class="tutor-subjects"><strong>Subjects:</strong> {escaped(", ".join(record["subjects"]))}</p>'
        if record['levels']:
            subjects+=f'<p class="tutor-subjects"><strong>Levels:</strong> {escaped(", ".join(record["levels"]))}</p>'
        credentials=''.join('<li>'+escaped(item)+'</li>' for item in record.get('credentials',[])) if full else ''
        if credentials:subjects+='<ul class="tutor-credentials">'+credentials+'</ul>'
        contact=f'<button class="text-button" data-enquiry="Tuition with {name}">Ask About Tuition with {name} →</button>' if full else f'<a class="text-link" href="our-approach.html#tutor-{key}" data-route="our-approach" data-anchor="tutor-{key}">Meet {name} →</a>'
        prefix='tutor-' if full else 'home-tutor-'
        bio=f'<p>{escaped(record["bio"] if full else record.get("summary",record["bio"]))}</p>'
        result.append(f'''<article class="named-tutor {'lead-tutor' if key=='florence' else ''}" id="{prefix}{key}"><div class="tutor-identity">{identity}<div><p class="eyebrow">{escaped(record['role'])}</p><h3>{name}</h3></div></div>{bio}{subjects}<p class="tutor-check">PVG checked</p>{contact}</article>''')
    return ''.join(result)

def render_parent_support(needs, testimonials):
    """Show aims and practical support separately from verbatim parent evidence."""
    routes={'our-approach':'our-approach.html','booster-classes':'booster-classes.html','tutoring':'tutoring.html','quick-checks':'quick-checks.html'}
    reviews={record['id']:record for record in testimonials}
    buttons=[];panels=[]
    for need in needs:
        key=escaped(need['id']);concern=escaped(need['concern'])
        buttons.append(f'<button type="button" class="need-circle" id="need-{key}" data-parent-need="{key}" aria-pressed="false" aria-controls="support-{key}">{concern}</button>')
        route=need['route'];anchor=need.get('anchor','');href=routes[route]+('#'+anchor if anchor else '')
        next_link=f'<a class="text-link" href="{escaped(href)}" data-route="{escaped(route)}"'+(f' data-anchor="{escaped(anchor)}"' if anchor else '')+f'>{escaped(need["label"])} →</a>'
        review=reviews.get(need.get('testimonial'))
        if review:
            if need['proof'] not in review['quote']:raise ValueError('Parent-support evidence must be verbatim.')
            proof=f'<figure class="need-proof"><p class="eyebrow">A parent’s experience</p><blockquote>“{escaped(need["proof"])}”</blockquote><figcaption><strong>{escaped(review["name"])}</strong> · {escaped(review["context"])}</figcaption><a class="text-link" href="#testimonials">Read our parent reviews →</a></figure>'
        else:
            proof=f'<div class="need-next-step"><p class="eyebrow">You don’t have to work it out alone</p><h4>Start with a conversation.</h4><p>Tell us their subject, year group and what feels difficult. We’ll explain the support available.</p><button class="text-button" data-enquiry="Support with {concern}">Talk to us about your child →</button></div>'
        panels.append(f'<article class="parent-solution" id="support-{key}" aria-labelledby="support-title-{key}"><div class="need-solution"><p class="eyebrow">What we work towards</p><h3 id="support-title-{key}">{escaped(need["goal"])}</h3><p>{escaped(need["support"])}</p>{next_link}</div><span class="need-arrow" aria-hidden="true">→</span>{proof}</article>')
    return '<div class="needs-choices" role="group" aria-label="Choose what your child finds difficult" hidden>'+''.join(buttons)+'</div><p class="sr-only" id="need-announcement" role="status"></p><div class="parent-solutions">'+''.join(panels)+'</div>'

def expand(source, root):
    testimonials=json.loads((root/'draft-source/testimonials.json').read_text())
    team=json.loads((root/'draft-source/team.json').read_text())
    needs=json.loads((root/'draft-source/home-support.json').read_text())
    source=source.replace('<!-- parent-support -->',render_parent_support(needs,testimonials))
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
