"""Render approved content records as escaped, server-free HTML at build time."""
import html
import json
import re
from urllib.parse import urlparse

def escaped(value):
    return html.escape(str(value), quote=True)

def render_google_reviews(records, featured=False):
    cards=[]
    for record in records:
        if featured and not record.get('featured'):continue
        if record['excerpt'] not in record['quote']:raise ValueError('Google excerpts must be verbatim.')
        if record['rating'] not in range(1,6):raise ValueError('Invalid review rating.')
        for field in ['source_url','author_url']:
            parsed=urlparse(record[field])
            if parsed.scheme!='https' or parsed.hostname!='www.google.com':raise ValueError('Google attribution must use Google source links.')
        date=record['published']
        from datetime import date as date_type
        display=date_type.fromisoformat(date).strftime('%d %B %Y').lstrip('0')
        quote=record['excerpt'] if featured else record['quote']
        more=f'<a class="text-link" href="{escaped(record["source_url"])}" target="_blank" rel="noopener">Read on Google<span class="sr-only">: {escaped(record["name"])} (opens in a new tab)</span> →</a>'
        cards.append(f'<figure class="google-review-card"><div class="google-review-card-top"><span class="google-review-source">Google review</span><span class="google-review-stars" role="img" aria-label="{record["rating"]} out of 5 stars">{"★"*record["rating"]}</span></div><h3>{escaped(record["title"])}</h3><blockquote>{escaped(quote)}</blockquote><figcaption><a href="{escaped(record["author_url"])}" target="_blank" rel="noopener">{escaped(record["name"])}<span class="sr-only"> (Google profile, opens in a new tab)</span></a><span>{escaped(record["context"])} · <time datetime="{escaped(date)}">{display}</time></span><small>Client-reported · {escaped(record["focus"])}</small></figcaption>{more}</figure>')
    return ''.join(cards)

def render_social_links(config):
    icons={
        'facebook':'<path d="M14 21v-8h3l.5-3H14V8c0-.9.3-1.5 1.5-1.5H18V3.2A21 21 0 0 0 15 3c-3 0-5 1.8-5 5v2H7v3h3v8Z"/>',
        'linkedin':'<path d="M5 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm-1.7 2h3.4v11H3.3Zm5.5 0H12v1.5c.7-1.2 1.9-1.8 3.4-1.8 3.6 0 4.3 2.4 4.3 5.5V21h-3.4v-5.2c0-1.2 0-2.9-1.8-2.9s-2.1 1.4-2.1 2.8V21H8.8Z"/>'}
    result=[]
    for key,label,domain in [('facebook','Facebook','facebook.com'),('linkedin','LinkedIn','linkedin.com')]:
        icon=f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{icons[key]}</svg>'
        url=config.get('social_links',{}).get(key)
        if url:
            parsed=urlparse(url)
            if parsed.scheme!='https' or not (parsed.hostname==domain or parsed.hostname.endswith('.'+domain)):raise ValueError('Unexpected social profile URL.')
            result.append(f'<a class="social-link" href="{escaped(url)}" target="_blank" rel="noopener" aria-label="EFL Tutors on {label} (opens in a new tab)">{icon}<span>{label}</span></a>')
        else:
            result.append(f'<span class="social-link social-pending editor-only" role="img" aria-label="{label}: profile link needed">{icon}<span>{label} · link needed</span></span>')
    return '<div class="social-links">'+''.join(result)+'</div>'

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
    google=json.loads((root/'draft-source/google-reviews.json').read_text())
    config=json.loads((root/'draft-source/site.json').read_text())
    source=source.replace('<!-- google-reviews:featured -->',render_google_reviews(google,featured=True))
    source=source.replace('<!-- google-reviews:all -->',render_google_reviews(google))
    source=source.replace('<!-- social-links -->',render_social_links(config))
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
