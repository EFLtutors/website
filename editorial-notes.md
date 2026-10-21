# EFL Tutors — review and launch notes

## Clarity, WhatsApp and Quick Checks update

Resources is now **Quick Checks**, with `quick-checks.html` as the main URL. Old resource URLs and standalone bookmarks remain compatible. Links appear on every main page, and the Booster Classes page has a hero link, matching subject links on all three class cards, a pre-timetable invitation, a short Check → Practise → Review journey and a FAQ.

The owner confirmed **07803 375101** for WhatsApp. The shared floating button opens `https://wa.me/447803375101` with a generic draft enquiry. The contact section also has a direct chat link. No message is sent automatically and no chat script loads on the site.

Longer testimonials now show short verbatim excerpts with the original full quotations available in expandable details. Founder and other explanatory paragraphs are shorter; full lesson explanations are expandable. The homepage has four decision-focused FAQs and a compact Quick Check invitation.

The results screen now offers **Save My Feedback**, producing a dated local text download with score, topics, chosen and correct answers, and explanations. No answers are automatically submitted or retained. There is no central progress dashboard. The copy positions Quick Checks as a starting snapshot for a discussion with a tutor. Repeating the same questions cannot establish independent improvement; meaningful progress review needs fresh questions and tutor feedback. A later validated, versioned question bank and agreed reporting/data arrangements would be required for formal programme-level measurement.

## Previous design direction

The shorter EFL Tutors name is now visible throughout, with a new text wordmark in the original royal blue (#064280) and gold (#e89b3c). It retains both original founder photographs, the learning philosophy and the existing parent testimonials.

The homepage follows a clearer parent journey: introduction and visible £75 Booster Class price, company figures, two tuition choices, reviews, EFL's approach, Emily's story, Quick Checks, school stages, getting started, schools and FAQs. The lead choice is weekly small-group Booster Classes; premium 1:1 tuition is the second option. Female-led, neurodivergent-friendly and Scotland-wide positioning uses the owner's supplied facts.

Central Tutors (https://centraltutors.co.uk/) and Educamus (https://educamus.co.uk/?view=home) were reviewed on 21 October 2026 for clear choices, visible prices, review placement and parent-friendly explanations. Their copy, photographs, outcomes and credentials were not imported. Central Tutors now also advertises group tuition: EFL's positioning should not claim group tuition is unique to EFL.

## Google business profile and reviews

The owner supplied https://share.google/X8bbJVbUG5ptDFynB, which resolves to **Edinburgh, Fife and Lothians Tutors**. Google's official business-profile embed was checked on **21 October 2026** and showed **5.0/5 from 20 reviews**, with EFL's existing website linked.

- Google Maps CID: `12299693131977025457`
- Place ID: `ChIJ_wwbh-nHh0gRsWfNqbxJsao`
- Profile: https://www.google.com/maps?cid=12299693131977025457
- Official embed: https://www.google.com/maps?cid=12299693131977025457&output=embed

The homepage includes a dated rating summary, a real Google link and an optional embedded Google business profile. Opening the embedded profile connects to Google; it does not load before the visitor chooses it. Closing it, navigating away in the standalone copy, or saving a copy removes its active URL. Its Google-provided rating and reviews link require an internet connection.

This is an official profile embed, not an automatically synchronised carousel of individual Google review quotations. The three text testimonials remain attributed to the original EFL website. Lauren, Joanna and Katie's quotations are reproduced verbatim and are not labelled as Google reviews. The dated rating outside the embed must be rechecked before launch and when updated. A live review-card feed would require a chosen supported review provider or an approved API integration.

The business profile retains the original regional name; the website explains EFL Tutors is the shorter name for the same business. Coordinate any public rebrand of the Google profile separately.

## Pricing and availability

Every Booster Class is **£75 per student per month**, as instructed. Classes are described on the existing site as weekly 75-minute online sessions, typically 4–8 students, through the school year.

The copied timetable retains six distinct classes: Sunday 2:30pm English; Sunday 4pm Applications of Maths; Sunday 6pm Maths; Monday 6pm Maths; Tuesday 6pm Chemistry; Tuesday 7:30pm Applications of Maths. All are National 5, with times in Europe/London. Availability is a draft copied from the original website, not live inventory. Confirm the timetable, current capacity, joining arrangements, billing dates and cancellation terms before publication.

1:1 prices from the original website checked 17 October 2026: National 5 from £40/hour, Higher from £45/hour, Advanced Higher from £50/hour. Ask about S1–S3 pricing and availability. No payment system or booking backend has been added.

## Founder photos and content

Both original photographs remain at **4016 × 6016 pixels**, without recompression. The hero and professional portrait remain in independent fixed photo frames. Preview photo controls allow either slot to be changed, imported from a saved HTML copy, and exported with all six pages. The two additional founder-photo placeholders remain in the expandable behind-the-scenes area. They are clearly placeholders.

Emily's introduction is draft copy based on the existing website and company facts, for her review. School partnerships are a future ambition, not an existing-contract claim.

## Figures, team and safeguarding

500+ students, founding in 2020, 95% pass rate and 65% neurodivergent/additional-support-needs students were supplied by the owner. Add the relevant cohort, qualifications, denominator and dates for the 95% figure, and population/period for the 65% figure before launch. A visible draft footnote records that these definitions are still needed.

Safeguarding and team copy uses owner-supplied facts: every tutor holds a PVG; some are GTC Scotland-registered teachers; the team also includes professionals and experienced graduates. Selection considers student connection, subject knowledge and shared values. TutorCruncher supports organisation and oversight; no unconfirmed software features, automatic checks or session recording are asserted. Finalise and publish the safeguarding policy and relevant contact arrangements.

## Free assessments

The Quick Checks page retains 12 online subject checks and 72 questions. Every assessment has two easy (C/D-style), two medium (B-style) and two hard (A-style) questions. These are indicative difficulty bands for tutor review, not official grade allocations or grade predictions. Maths includes indices and circle geometry in place of averages and probability, with an accessible circle diagram.

No personal details are requested, and no answers are submitted or stored. Attempts clear when leaving/reloading Quick Checks and are excluded from saved review copies. Have subject tutors approve questions, distractors, difficulty and explanations before publishing.

## Review, build and launch

The canonical source is `draft-source/source.html`, `draft-source/assessments.json`, `styles.css` and `script.js`. Run `python draft-source/build.py` to generate the six normal pages and self-contained `preview.html`. `website-preview.zip` contains the standalone file as `OPEN-WEBSITE.html` and brief opening instructions.

The standalone copy opens without a server. Google's optional embedded profile and external booking links require internet. The normal pages use shared assets; keep their folders together. Local development: `python -m http.server 8000` from the repository root. Acceptance checks: `python tests/test_resources.py` and `python tests/test_website.py` with Python Playwright and Chromium installed.

Enquiry forms remain clearly labelled local previews and send nothing. The existing email and Calendly consultation links remain available. Before launch, connect enquiries and privacy information, confirm policies and commercial terms, approve editorial claims and questions, and agree school delivery arrangements as needed. The live website has not been changed.
