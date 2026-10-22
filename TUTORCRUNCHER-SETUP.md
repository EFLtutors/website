# Connecting the EFL contact form to TutorCruncher

The website already uses TutorCruncher's official Socket enquiry form. The public Socket key was taken from the webhook link you supplied. The webhook itself is not used as a custom form's submission URL, and no private API key belongs in browser code.

## What works now

On the configured production domain, open a parent/class enquiry and choose **Request a Callback Online**. TutorCruncher's official form loads in an isolated frame. Its mandatory CAPTCHA and submission are handled by TutorCruncher. WhatsApp and email remain available alongside it.

A read-only check on 22 October 2026 loaded the real form successfully. The current fields are your name (required), email (optional), phone (optional), and student name (optional). The current account schema has no subject, year group or message fields. Class-specific WhatsApp/email enquiries retain that context; the present online form is a general callback request.

The downloaded HTML and local preview cannot use the production-only form. That is a domain restriction, not a missing API key. No test enquiry or CAPTCHA was submitted, and delivery has not yet been verified.

## Finish the account setup

1. In TutorCruncher, go to **System → Settings → TutorCruncher API → API Integrations** and edit the existing Socket integration. Check its **Allowed Domains**. Include the exact deployed origin (with the correct www/non-www choice); add a staging domain if you want to test there. Keep `site_url` in `draft-source/site.json` consistent and rebuild the website if changing it.
2. Add Client custom fields for **subject**, **year group**, **message** and, if needed, the requested class. Enable **Client can Access** and **Enquiry Form** for the fields you want on the form. Check the form renders them after saving. Add any required privacy/terms link in the provider configuration.
3. Make sure an enquiry requires a way to reply. The current basic form allows both phone and email to be empty. Review TutorCruncher's advanced enquiry-form configuration with your account settings/support if you need one contact channel to be compulsory. The website has not pretended this setting is already enabled.
4. Check who receives enquiry notifications and how a new enquiry appears in your TutorCruncher account. These account-side settings cannot be changed from this static project.
5. After the draft is hosted on an allowed domain, manually send one controlled test enquiry using your own details and complete CAPTCHA yourself. Confirm the client/enquiry record, field values, email notifications and acknowledgement. Then verify failure and required-field messages.

Future automatic class-context prefill should be added only after the actual field identifiers are confirmed. Do not paste an API secret into the website or post a normal contact form to `/webhook`.

Official setup guide: https://help.tutorcruncher.com/en/articles/14182719-getting-started-with-tutorcruncher-socket

The existing live website has not been deployed or changed by this revision.
