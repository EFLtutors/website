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

These are **draft starter questions for tutor review**, using introductory National 5 topics or general subject skills. They do not cover every course unit and do not predict an exam grade. Have subject tutors approve questions, distractors and explanations before publishing.

## Editing and rebuilding

- `draft-source/source.html` — shared layout and page content
- `draft-source/assessments.json` — editable questions, choices, correct-answer indexes and explanations
- `styles.css` and `script.js` — shared styling and interactions
- `draft-source/build.py` — generates all six pages and the standalone preview

Run `python draft-source/build.py` after editing. Refresh the ZIP with the generated `preview.html` before sharing.

Browser checks are in `tests/test_resources.py`. Run `python tests/test_resources.py` with Playwright and Chromium installed. They cover all 72 answer keys, scoring, feedback, answer changes, restart, routing, saved attempts, mobile layouts and keyboard controls.

## Draft status

Enquiry forms are local previews and send nothing. Timetable details came from the original website and need current availability confirmation. Finalise payment/cancellation terms, business policies and metric definitions before launch. No deployment has been performed.
