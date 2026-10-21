"""Rebuild and package review/public copies using only the standard library."""
from pathlib import Path
import subprocess
import sys
import zipfile
root=Path(__file__).resolve().parent.parent
subprocess.run([sys.executable,str(root/'draft-source/build.py')],check=True,cwd=root)
review_notes='''EFL Tutors website review

Extract this ZIP, then open OPEN-WEBSITE.html in a modern browser.
All six main pages, original founder photos and 12 Quick Checks are embedded.
The audit and handover is included as audit-and-handover.md.

Use the top photo controls to change either image, then Save Website to keep it.
Quick Checks run locally. Save My Feedback creates a local text file; no answers are submitted.
WhatsApp/email links work through your own apps. A prepared email is not sent until you send it.

The configured TutorCruncher online form loads only on the permitted production origin.
It is unavailable in this downloaded review copy; WhatsApp/email remain available.
No real client enquiry or booking was sent in testing. Final delivery must be checked after deployment.

The existing live website has not been changed. This file is for review.
'''
with zipfile.ZipFile(root/'website-preview.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 z.write(root/'preview.html','OPEN-WEBSITE.html')
 z.writestr('READ-ME.txt',review_notes)
 z.write(root/'audit-and-handover.md','audit-and-handover.md')
public_files=['index.html','booster-classes.html','tutoring.html','schools-partners.html','our-approach.html','quick-checks.html','resources.html','enquiry-widget.html','enquiry-widget.js','styles.css','components.css','script.js','robots.txt','sitemap.xml']
with zipfile.ZipFile(root/'public-site.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in public_files:z.write(root/name,name)
 for path in (root/'assets').rglob('*'):
  if path.is_file() and path.name not in ['founder-hero.jpg','founder-professional.jpg']:
   z.write(path,str(path.relative_to(root)))
 z.writestr('READ-ME.txt','EFL Tutors public static files\n\nKeep the HTML, CSS, JavaScript and assets together when hosting. This is not a deployment.\n\nDraft indexing is disabled. Before launch, confirm the intended production domain in draft-source/site.json, approve launch inputs, set indexable true, and run python draft-source/package.py from the source repository to rebuild.\n\nThe TutorCruncher form needs the permitted production origin. Confirm allowed domains and fields, then test receipt/notifications with a controlled enquiry. Local previews use WhatsApp/email.\n\nOriginal full-resolution founder JPEGs remain in the repository and standalone editor; this public package uses responsive WebP derivatives.\n')
 z.write(root/'audit-and-handover.md','audit-and-handover.md')
for name in ['website-preview.zip','public-site.zip']:
 with zipfile.ZipFile(root/name) as z:
  if z.testzip():raise RuntimeError('Invalid ZIP: '+name)
 print(name,(root/name).stat().st_size,'bytes')
