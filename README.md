# EFL Tutors website draft

A six-page static website with your original blue-and-gold identity and founder photos:

- `index.html` — homepage, founder story, testimonials and company statistics
- `booster-classes.html` — £75/month classes, timetable, filters and FAQs
- `tutoring.html` — 1:1 subjects, prices and FAQs
- `schools-partners.html` — prospective partnerships and a school enquiry preview
- `our-approach.html` — teaching philosophy
- `resources.html` — 12 free online subject self-checks with instant feedback

## Review the website

For the complete standalone review copy, open `preview.html` in a browser. All six pages, both founder photos, styling, fonts and assessment content are embedded. `website-preview.zip` contains that file as `OPEN-WEBSITE.html`.

The individual HTML files use shared `assets/`, `styles.css` and `script.js`. Keep those together. To serve the normal site locally, run `python -m http.server 8000` from this directory.

## Free assessments

The Resources page has six-question starter assessments for Maths, Applications of Maths, English, Physics, Chemistry, Biology, History, Geography, Modern Studies, Business Management, Psychology and Media.

Parents and students can choose a subject, answer at their own pace, return to change answers, then see a score for those six questions, explanations and topics worth revisiting. No account, email, payment, storage or answer submission is involved. Assessments reset when leaving/reloading the page; saved website copies exclude attempts.

Each self-check starts with **two easy (C/D-style)** questions, followed by **two medium (B-style)** and **two hard (A-style)** questions. The questions include application and reasoning, not just recall. Maths now includes indices and circle geometry in place of averages and probability.

These are **draft questions and indicative difficulty bands for tutor review**, using National 5-style topics or general subject skills. The bands are not official grade allocations. They do not cover every course unit and do not predict an exam grade. Have subject tutors approve questions, distractors and explanations before publishing.

## Editing and rebuilding

- `draft-source/source.html` — shared layout and page content
- `draft-source/assessments.json` — editable questions, choices, correct-answer indexes and explanations
- `styles.css` and `script.js` — shared styling and interactions
- `draft-source/build.py` — generates all six pages and the standalone preview

Run `python draft-source/build.py` after editing. Refresh the ZIP with the generated `preview.html` before sharing.

Browser checks are in `tests/test_resources.py`. Run `python tests/test_resources.py` with Playwright and Chromium installed. They cover all 72 answer keys, scoring, feedback, answer changes, restart, routing, saved attempts, mobile layouts and keyboard controls.

## Draft status

Enquiry forms are local previews and send nothing. Timetable details came from the original website and need current availability confirmation. Finalise payment/cancellation terms, business policies and metric definitions before launch. No deployment has been performed.

## Our tutors and safeguarding

Our Approach now includes dedicated team and safeguarding sections, linked from the homepage, 1:1 page and footer. The copy uses the facts supplied by the company: every tutor holds a PVG; some tutors are GTC Scotland-registered teachers; the team includes subject professionals and experienced graduates; selection considers student connection, specialist knowledge and shared values. TutorCruncher is described as supporting organisation and oversight as part of the safeguarding approach. No unconfirmed software features or session-recording claims are included.
