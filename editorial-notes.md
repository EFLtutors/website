# EFL Tutors — five-page website draft

The approved homepage with your photos is saved separately at `/workspace/website-snapshots/approved-homepage-with-photos.html`. A snapshot of the editable draft before expansion is also retained. No live website changes have been made.

## What is built

1. **Home:** the approved blue-and-gold design, founder photos, four company metrics, parent testimonials, S1–S6 positioning and Booster Classes as the lead offer.
2. **Booster Classes:** National 5 Maths, Applications of Maths and English cards; a six-class timetable with subject, day and availability filters; class-specific enquiries and ten Booster Class FAQs.
3. **1:1 Tutoring:** subjects and prices by qualification, premium positioning, tutor matching, a real parent testimonial and six FAQs.
4. **Schools & Partners:** possible areas of collaboration, a proposed working process, a separate school enquiry form and FAQs. The page invites future conversations and does not claim existing contracts, provider approval or agreed services.
5. **Our Approach:** the original site's practice → understanding → confidence philosophy, lesson principles, individual learning needs and links to the two tuition options.

## Opening and saving

Download `index.html` and open it in a browser. This is a self-contained review copy: all five pages, styling, fonts and your two photos are embedded. The navigation switches between distinct pages inside that file. **Save Website** saves all five pages and your current photo choices together.

The `site/` directory is a conventional static website containing five separate HTML pages, shared CSS, JavaScript, fonts and images. Open `site/index.html` after extracting the ZIP, or serve that directory with a static web server. The static pages use normal links and show only their own content. The photo editing toolbar is present only in the review copy.

The editable source is `source.html`, `styles.css`, `script.js` and `assets/` (or `site/assets/` in the packaged download). Run `python build-standalone.py` to rebuild both outputs. The original live website remains unchanged.

## Prices and timetable

All Booster Classes are **£75 per student per month**, following your latest instruction. The old £675 total and nine-payment wording have been removed. A minimum commitment, billing dates, joining rules and cancellation terms have not been invented; agree and publish those before enrolment.

The existing site was checked on 17 October 2026. Its timetable lists:

| Day | Start, UK local time | National 5 subject | Enquiry status in the draft |
| --- | --- | --- | --- |
| Sunday | 2:30 pm | English | Enquiries open |
| Sunday | 4:00 pm | Applications of Maths | Enquiries open |
| Sunday | 6:00 pm | Maths | Enquiries open |
| Monday | 6:00 pm | Maths | Waiting list |
| Tuesday | 6:00 pm | Chemistry | Waiting list |
| Tuesday | 7:30 pm | Applications of Maths | Waiting list |

Source: `/programmes.html`. Classes are described there as weekly 75-minute online sessions, typically with 4–8 students. Times use Europe/London so they follow UK daylight saving. These are copied schedule details, not live inventory. Current dates and availability must be confirmed before booking. The draft avoids guaranteeing spaces and does not accept payments.

Premium 1:1 prices from `/tutoring.html`: National 5 from £40/hour, Higher from £45/hour, Advanced Higher from £50/hour. Subjects are copied by qualification level. S1–S3 support is offered as an enquiry with pricing to be discussed.

## Founder photos and clarity

Both original photos were extracted from your uploaded saved HTML at **4016 × 6016 pixels** and retained without recompression. They are embedded at full resolution in the review copy and provided as original JPEGs in the static site. Images remain clipped inside their fixed boxes. The **Photo fit** selector lets you choose between filling the box and showing the whole photograph, without stretching the image.

**Change Hero Photo** and **Change Professional Portrait** update the two slots independently. **Restore Saved Photos** can retrieve the two embedded photographs from a previous saved HTML file. It reads image data only and does not execute scripts from that file.

Optional AI clarity edits were tried and saved separately in `/workspace/website-snapshots/clarity-options/`. They can change fine detail and are smaller than the originals, so the website uses your original photos by default. Those alternatives have not replaced the originals.

## Content and remaining launch inputs

The 500+ students, 2020 founding year, 95% pass rate and 65% neurodivergent/additional-support-needs figure come from your instructions. Add the cohort, denominator, qualifications and date range for the pass rate, and the population and period behind the 65% figure before publication.

Parent quotations from Lauren, Joanna and Katie are reproduced verbatim from the original site. The founder's first-person introduction is drafted from existing site content and your figures; review its wording.

The enquiry forms validate inputs locally but send nothing. School enquiries have organisation, role and approximate cohort fields. Class enquiries retain the chosen subject, day, time and £75 monthly price. Connect a form service and privacy notice before enabling submission. Your existing Calendly and email links remain available.

Before launch, confirm availability, billing and cancellation terms, business identity, privacy information, safeguarding arrangements, tutor checks, school procurement requirements and any agreed reporting service. No payment system, CMS or live booking backend is included.
