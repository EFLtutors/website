# EFL Tutors audit and implementation — 21 October 2026

## Findings, in priority order

1. **Enquiry dead end:** service, timetable and school buttons opened a preview form that sent nothing. This was the largest conversion risk. There was no configured submission service or credential binding in the project/environment.
2. **Insufficient evidence behind visible percentages:** the 95% pass rate lacked a cohort, qualification, denominator and period. The 65% demographic figure lacked a defined population and period. A tiny draft footnote was not sufficient qualification for prominent public claims.
3. **The team was largely anonymous:** the site described tutor selection, but did not introduce Florence, Michael or Neel. Florence's existing client feedback was separated from her role.
4. **Repetition and mobile hierarchy:** the 390px homepage was approximately 12,949px long. Several sections repeated confidence and fit, and some small controls used 9–11px text. The editing gallery and launch notes could leak into public review journeys.
5. **Performance and SEO:** the two original founder JPEGs totalled 6.45MB, both lacked responsive alternatives, and the professional portrait was not lazy loaded. Every page shared one description; JavaScript shortened the generated titles. Canonical links, sharing previews and structured organisation information were absent.
6. **Accessibility details:** automated review identified low contrast in gold-on-blue labels, pale offering numbers, missing landmark coverage and a skipped heading level. These were corrected and rechecked.

What was already working: the blue-and-gold identity, authentic founder photos, visible £75 group price, clear distinction from hourly 1:1, real existing testimonials, WhatsApp contact link, six-class timetable filters and the 12 Quick Checks. Both existing browser suites passed before editing. This remains the same static website, with no framework replacement or new server dependencies. The official TutorCruncher widget is an optional, on-demand third-party integration.

## Page-by-page changes

| Page | Improvements |
| --- | --- |
| Home | Clearer understanding/confidence headline; Booster Classes retain the primary action; contextual secondary enquiry; named team near the service comparison; concise philosophy replaces repeated marketing cards; undefined percentages removed; year-group detail expandable; shorter school introduction. |
| Booster Classes | £75 pricing and all six original timetable rows preserved; Monday Physics at 6:30 pm added and existing Tuesday Chemistry at 6 pm updated to live on owner confirmation; class context carried into WhatsApp/email; waiting-list buttons request information rather than implying registration; direct subject Quick Checks and the Check → Practise → Review journey retained. |
| 1:1 Tutoring | Existing prices/subjects preserved; Katie's unaltered Florence testimonial comes from the shared evidence record; contact choices use genuine available routes. |
| Our Approach | Florence introduced prominently as Lead Tutor, with Michael and Neel as key tutors; owner-approved subjects and biographies, including Michael’s GTC Scotland registration/SQA marking role and Neel’s medical studies; Katie's feedback linked to Florence; safeguarding and TutorCruncher copy retained without invented features; no unverified demographic percentage. |
| Schools & Partners | School contact retains organisation/role/cohort context; no identifiable pupil data requested; no invented contract history, delivery agreement or reporting service. |
| Quick Checks | All 72 questions, scoring, explanations, feedback downloads, privacy behaviour and old Resources links preserved; heading order corrected; purpose remains a learning snapshot rather than an examination-grade or improvement claim. |

## Parent enquiry journey

A parent can compare the two offers, choose a class, then open a contextual contact dialog. WhatsApp includes the selected class, day, time and £75 price. The message remains a draft for the parent to send.

Email is clearly labelled as a handoff: two required fields (name and message), optional reply email/year group, browser validation, an inspectable email draft, an encoded `mailto:` link and a copy fallback if the email app or clipboard is unavailable. School enquiries require the organisation. No page claims delivery or displays a fake success receipt. Closing the dialog clears its details; exported website copies strip enquiry data and generated contact links.

**TutorCruncher Socket is now configured using the public key from the owner-supplied integration URL.** The webhook URL itself is not used as a form action. Official setup guidance confirms the key is public; no private API key is used. The live enquiry schema and company-options endpoints returned HTTP 200, and the actual official enquiry widget rendered in a read-only browser check using the permitted production origin. No client record, notification or enquiry was created.

The online callback form loads only when a parent requests it on the configured production origin. Local/downloaded previews use the working WhatsApp/email routes, because TutorCruncher rejects their origins (HTTP 403). The widget is isolated in `enquiry-widget.html`; closing the dialog discards its state. Load failures retain contact fallbacks. Provider success is shown only after its documented submission callback. Mandatory Google CAPTCHA is retained. The widget's default Google Analytics attempt is disabled within the frame, and its content-security policy restricts connections to the form/CAPTCHA services. No first-party analytics was introduced.

**Remaining TutorCruncher setup:** the actual schema currently contains only name, optional email, optional phone and student name. Add suitable Client custom fields for subject, year group and message (with Client can Access / Enquiry Form flags), then review required fields in TutorCruncher. Basic forms do not enforce a contact channel by default; use the documented advanced configuration if a reply address/number must be required. Until richer fields are configured, the online route is labelled a general callback request; WhatsApp/email retain class and subject context. School enquiries retain their separate organisation-focused routes. Confirm the final deployed domain is allowed, set approved privacy/terms links and manually test one controlled enquiry and its delivery/notifications after deployment. CAPTCHA completion and final submission were not automated.

Official references:
- https://help.tutorcruncher.com/en/articles/14182719-getting-started-with-tutorcruncher-socket
- https://help.tutorcruncher.com/en/articles/14182718-basic-client-enquiry-form-socket
- https://help.tutorcruncher.com/en/articles/14182716-advanced-client-enquiry-form-socket

The existing Calendly URL was preserved from the live website. A first generic request was rejected, but a follow-up using normal browser headers returned **HTTP 200**. The page is reachable; availability, successful scheduling and confirmation delivery were not tested. Test a controlled booking manually before launch.

## Evidence and claims requiring review

| Item | Source/status | Action before launch |
| --- | --- | --- |
| 500+ students; founded 2020 | Supplied by the owner; shown with attribution | Confirm the student-count definition and current total. No pass-rate inference is made. |
| 95% pass rate | Held out of public copy | Supply cohort, qualifications, period, denominator, method and supporting records before reinstating. |
| 65% neurodivergent/additional-support-needs students | Held out of public copy | Supply population, period and appropriate basis for publication before reinstating. Neurodivergent-friendly positioning remains. |
| Google 5.0/5 from 20 reviews | Official EFL profile checked 21 October 2026 | Recheck before launch; dated summary is not an automatically synchronised review feed. |
| Lauren, Joanna and Katie | Previously published EFL quotations, retained verbatim | Confirm continuing publication permission and context. These are client-reported experiences, not verified exam results or measured progress. |
| Florence as Lead Tutor and relationship strengths | This owner brief | Subjects and biography now approved and incorporated. Confirm qualification levels and portrait. No tutor-management/training duties asserted. |
| Michael and Neel as key tutors; all PVG checked/compliant | This owner brief | Supplied subjects/biographies are now incorporated. Michael’s registration and marking role and Neel’s student/instructor roles use owner-approved wording. Confirm individual qualification levels and approved portraits; keep credentials current. |
| Booster Classes £75/month | Explicit owner instruction | Confirm joining, billing and cancellation terms. No term length invented. |
| 1:1 from £40/£45/£50 by level | Existing live website, rechecked 21 October 2026 | Confirm current rates, subject availability and S1–S3 pricing. |
| Seven timetable rows; 4–8 students; weekly 75-minute sessions | Original six rows plus owner-confirmed Monday Physics 6:30 pm and Tuesday Chemistry 6 pm live updates, 21 October 2026 | Physics uses National 5 like the existing timetable; confirm if different. Confirm dates/capacity. The timetable is not live inventory. |
| School partnerships/reporting | Future discussions | Agree scope, safeguarding, procurement, consent/data handling, delivery and reporting before commissioning. |

No new exam result, independence outcome, client identity, testimonial, tutor qualification or partner logo was invented. There is not yet approved evidence for every desired outcome category. Add genuine independence, engagement and examination stories when authorised evidence is available.

## Maintainability, SEO and performance

- `draft-source/source.html`: existing shared layout and content.
- `draft-source/team.json`: editable team records. Subjects and approved biographies are populated; empty level/photo fields document what is still missing.
- `draft-source/testimonials.json`: full quotation, verbatim excerpt, author/context, outcome theme and source. The build rejects an excerpt that is not part of its original quotation.
- `draft-source/content.py`: escaped reusable rendering. No runtime content requests.
- `components.css`: focused new components/accessibility refinements; original theme remains in `styles.css`.
- `draft-source/site.json`: production domain, optional form URL and indexing switch.

Public pages have unique retained titles/descriptions, canonical URLs, Open Graph information, a 1200×630 sharing image and truthful EducationalOrganization structured data. A sitemap and robots file are generated. **Draft indexing is disabled** (`indexable: false`, public `noindex,follow`, robots disallow); set the correct production domain and enable indexing only when publishing the approved site. The standalone editor always remains noindex.

Responsive WebP derivatives are provided at 480/960/1440px; the largest pair totals approximately 299KB versus the originals' 6.45MB. Originals are unchanged and retained in the standalone editor. The public hero is prioritised and the lower portrait lazy loaded. This is an asset-size comparison, not a measured real-user speed improvement. No first-party analytics was introduced. Google profile and TutorCruncher load only on request; unnecessary Socket analytics is disabled inside its restricted frame.

## Validation and remaining launch work

Completed: all four browser suites passed; build, JavaScript syntax checks and source JSON/HTML/link checks passed; the extracted public package loaded all six main pages without missing assets or JavaScript errors. Screenshots and reflow checks covered 320, 390, 768, 1024 and 1440px. Both original JPEG files remain unchanged.

The actual TutorCruncher script, options and enquiry-schema requests returned HTTP 200 and its real form rendered in a read-only browser check with all non-GET requests blocked. After analytics was disabled, that check made no non-GET requests. No enquiry, CAPTCHA challenge or booking was submitted. The provider submission/delivery and screen-reader/cross-browser checks remain manual launch tasks.

The available browser suites cover all 72 Quick Check answers; six-page navigation and five responsive widths; parent/school validation, email/WhatsApp handoff and private-data export; and Socket origin checks, loading/error fallback, message validation and frame reset using a fake provider. Available reproducible checks:

- `python draft-source/build.py`
- `python draft-source/package.py` (rebuilds both review/public ZIPs)
- `node --check script.js`
- `python tests/test_resources.py`
- `python tests/test_website.py`
- `python tests/test_enquiries.py`
- `python tests/test_tutorcruncher.py`
- `node --check enquiry-widget.js`

Additional review used Chromium desktop/mobile screenshots and axe-core 4.10.3 against WCAG 2.0/2.1/2.2 A/AA and best-practice checks. The six main pages at mobile/desktop plus contact and Quick Check states returned zero automated violations after fixes. The provider’s CAPTCHA flow and assistive-technology use still require manual testing. Automated accessibility checks are useful evidence, not a claim of complete compliance or a substitute for assistive-technology testing. There is no configured project linter, production monitoring or real-user performance analytics.

Before launch: finish tutor/claims approvals, confirm prices/timetable, approve privacy and commercial policies and safeguarding procedures, test the real contact/booking routes, finish the TutorCruncher field/domain setup and delivery test, confirm domain/hosting, enable indexing at the appropriate time, and deploy the public files. The current live website has not been changed.

## Latest readability and class updates

Main text uses self-hosted Nunito Sans with Poppins headings, clearer line spacing and larger action text. EFL colours and existing page structure remain. Physics (Monday 6:30 pm) and Chemistry (Tuesday 6 pm) are labelled live, with £75/month pricing, contextual enquiries and subject Quick Checks. Chemistry updates its existing row rather than creating a duplicate.

Florence’s inline chat photograph is visible but its original file is not accessible in the workspace. The draft therefore retains her initial rather than inventing a photo. The standalone Add Florence’s Portrait control accepts the original, updates both profiles in contained, uncropped frames and includes it in Save Website. An accessible JPG attachment is needed to incorporate the exact photograph in the repository/public site.

## Homepage messaging and parent journey revision

The owner’s new Scotland-wide positioning now leads the hero: “Scotland’s tutoring and learning specialists”, with confidence-boosting classes and tuition for National 5 and Higher. “Confidence Starts Here” introduces the existing service comparison and clear £75/month / 1:1 prices. Booster Classes retain primary action priority; free Quick Checks and a personal conversation are clear alternatives. Repeated hero and philosophy content is folded into relevant sections.

Seven circular concern controls reveal one support explanation at a time. They work with mouse, touch and keyboard, expose selection state and announce the chosen aim. Without JavaScript, all seven explanations remain readable. New editable records live in `draft-source/home-support.json`; the build validates proof excerpts against the original review. Enjoying learning, confidence, exam readiness, study routines, understanding, inclusion and focus are framed as aims. No new testimonials, outcome data or guaranteed examination success were invented. Genuine parent feedback and the dated Google profile connection remain distinct.

The coverage section welcomes learners from S1 to Advanced Higher and includes a local illustrated Scotland map with the Hebrides, Orkney and Shetland. Geographic labels illustrate online reach, not offices. The SVG is embedded in the standalone review and has no map-provider requests. Crown copyright / OGL attribution appears in its metadata, `assets/scotland-map-attribution.txt` and visible expandable credits.

Florence, Michael and Neel have clearer homepage introductions using approved details. Founder photographs and Florence’s upload/restore controls remain. A prominent “A clear way to start: a Quick Check” section explains the route from free feedback to a real conversation, transparent prices and agreed tuition. Booking remains the existing external consultation link; there is no claim of automatic lesson booking or immediate availability.

Revision validation: all four existing browser suites passed. Additional tests exercised all seven concern controls by mouse and keyboard in static and standalone copies, the no-JavaScript fallback, local map loading, and map/photo persistence in exported HTML. Screenshots/reflow covered all six pages at 320, 390, 768, 1024 and 1440px. A further photo-fixture check verified both Florence profiles at 320/390/768/1440px. All seven concern states at mobile and desktop returned zero automated axe violations. No live enquiry or booking was submitted.
