# EFL Tutors website

An existing static site, now with 11 pages, refined rather than rebuilt: blue and gold, authentic founder photos, Booster Classes first, personal 1:1 tuition, named team, parent feedback and free Quick Checks.

## Run and build

From this repository:

```sh
python draft-source/build.py
python -m http.server 8000
```

Normal builds use Python's standard library. Public HTML files share `styles.css`, `components.css`, `script.js` and `assets/`. `enquiry-widget.html`/`enquiry-widget.js` serve the optional Socket frame. Keep them together. `resources.html` is a compatibility copy of Quick Checks, to preserve old Quick Check bookmarks. The new umbrella is `more-resources.html`.

`preview.html` is a standalone editor with all pages, original founder photos, fonts and Quick Checks embedded. `website-preview.zip` contains it as `OPEN-WEBSITE.html`. Opening, photo replacement and Save Website need no server. External contact/booking/Google links need internet.

## Edit

| File | Purpose |
| --- | --- |
| `draft-source/source.html` | Existing layout and shared copy |
| `draft-source/pages.json` | All 11 routes, filenames, navigation labels and metadata |
| `draft-source/google-reviews.json` | Verbatim attributed Google reviews, checked dates and homepage selection |
| `draft-source/team.json` | Approved team details; empty fields are intentionally unclaimed |
| `draft-source/home-support.json` | Parent concerns, support aims and verbatim proof excerpts |
| `draft-source/testimonials.json` | Full genuine quotations, verbatim excerpts and source/context |
| `draft-source/assessments.json` | 12 subject Quick Checks; 72 questions and explanations |
| `draft-source/content.py` | Escaped reusable content rendering |
| `draft-source/site.json` | Intended domain, indexing switch, public Socket key and optional hosted enquiry URL |
| `styles.css` | Existing brand/theme |
| `components.css` | Refined components, contact dialog and accessibility |
| `script.js` | Navigation, contact handoff, photos, timetable and Quick Checks |

Rebuild after editing. Run `python draft-source/package.py` to rebuild both download ZIPs: `website-preview.zip` for review and `public-site.zip` for conventional static hosting. The public ZIP does not include the editor or large original JPEGs. Public founder photos use committed WebP derivatives. Optional regeneration uses `python draft-source/optimise_images.py` (Pillow required only for this asset-preparation step). The original JPEGs remain untouched. `draft-source/social-preview.html` is the source of the social sharing image.

## Contact and privacy behaviour

WhatsApp uses the owner-confirmed **07803 375101**. Class enquiries include the selected class in a draft, not an automatic message. Email enquiries validate details and prepare a `mailto:` draft with a manual-copy fallback. Nothing is sent automatically. **TutorCruncher Socket is configured** using the owner-supplied public key. On the permitted production origin, parents can explicitly load its official callback form with required CAPTCHA. It is isolated in a frame, discarded on close, and its default analytics is disabled. Local/downloaded previews retain WhatsApp/email because their origins are not allowed by TutorCruncher. The current provider form lacks subject/year-group/message fields and leaves contact details optional; finish those settings and a controlled delivery test before launch. See the handover for exact requirements.

Quick Checks run in the tab, without personal details, storage or answer submission. Save My Feedback creates a local file. Repeating the same six questions is practice, not proof of improvement. Attempts and contact details are excluded from saved website copies.

Four genuine Google reviews are stored in `draft-source/google-reviews.json`, with three featured directly on the homepage and all four on Reviews. Author names, dates, ratings and source/profile links are retained. The dated selection is updated manually, not automatically synced. The original three website testimonials remain distinct. The optional official Google profile embed loads only when opened; no first-party analytics has been added.

## Checks

Requires Python Playwright and Chromium at `/usr/bin/chromium`:

```sh
python tests/test_resources.py
python tests/test_website.py
python tests/test_enquiries.py
python tests/test_tutorcruncher.py
python tests/test_resources_and_reviews.py
node --check script.js
node --check enquiry-widget.js
```

The first suite covers all 72 answers, explanations, scoring, navigation, keyboard use and responsive feedback. The second covers all public pages at five widths, photo containment, timetable filters, Google opt-in, old links and Quick Check downloads. The third covers parent/school email drafts and validation, WhatsApp context, copy fallback, private-data export, evidence records and metadata. The Socket suite tests provider loading/failure, origin checks, message validation and state reset with a fixture. Tests do not send messages.

## Launch status

Read [audit-and-handover.md](audit-and-handover.md) for the audit, implementation, evidence register and remaining inputs. Undefined pass-rate/demographic percentages are held out of public copy. Approved subjects and biographies are now populated; individual qualification levels and approved tutor portraits still need confirming. Pricing, timetable, publication permissions and business policies require final review.

**Draft indexing is disabled.** Confirm `site_url`, then set `indexable: true` and rebuild when the approved public site is ready to launch. The live website has not been deployed or changed.

Latest draft: self-hosted Nunito Sans body text; Monday Physics 6:30 pm and Tuesday Chemistry 6 pm live (£75/month). The standalone toolbar also lets you add Florence’s portrait to both her profiles and save it with the website. The public build still needs her original JPG attachment.

Homepage revision: Scotland-wide hero, Confidence Starts Here service comparison, accessible concern-circle controls, genuine parent proof, illustrated Scotland map, fuller approved tutor summaries and a Quick Check → conversation → agreed support journey. All seven support explanations remain visible without JavaScript. The map is a local SVG, embedded in the standalone copy; attribution is in `assets/scotland-map-attribution.txt` and its on-page credits. Goals are separate from client-reported experiences; there is no invented grade improvement or examination-success statistic.

Latest update (22 October 2026): green “Spaces available” labels, complete £75 Booster Class value explanation, owner-provided reputation/refund FAQ, direct Google review cards and a dedicated Reviews page. More Resources contains National 5 Quick Checks, two draft Blog guides, Founder Story and Become a Tutor. Higher Quick Checks are not advertised as available. Social icon links are configured in `draft-source/site.json`; unconfigured profiles appear only as review-copy placeholders and are omitted from the public site.

Read [TUTORCRUNCHER-SETUP.md](TUTORCRUNCHER-SETUP.md) for the exact account-side steps. The production-domain callback form was rechecked read-only; subject/year/message fields, required contact details, notifications and submission delivery still need account setup/testing. No private key is needed in frontend code.
