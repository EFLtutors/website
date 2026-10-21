// The official Socket widget handles validation, mandatory CAPTCHA and submission.
// It is isolated in this same-origin frame and loaded only after a visitor requests it.
(() => {
 // Socket attempts to install Google Analytics by default. Disable it inside this frame.
 window.ga=()=>{};
 const status=document.getElementById('socket-status');
 const container=document.getElementById('socket-enquiry');
 const origin=document.body.dataset.appOrigin;
 let failed=false;
 function notify(state){if(window.parent!==window)window.parent.postMessage({type:'efl-enquiry-status',state},origin);}
 function resize(){if(window.parent!==window)window.parent.postMessage({type:'efl-enquiry-height',height:Math.ceil(document.documentElement.scrollHeight)},origin);}
 function unavailable(){
  if(failed)return;failed=true;
  status.textContent='The online form is unavailable. Please use WhatsApp or email.';
  document.getElementById('socket-fallback').hidden=false;notify('unavailable');resize();
 }
 if(location.origin!==origin){unavailable();return;}
 const timer=setTimeout(unavailable,15000);
 const observer=new MutationObserver(()=>{
  if(container.querySelector('form')){
   failed=false;document.getElementById('socket-fallback').hidden=true;
   const labels={client_name:'Your name',client_email:'Email address',client_phone:'Phone number',service_recipient_name:'Student name'};
   container.querySelectorAll('input[name]').forEach(input=>{if(labels[input.name])input.setAttribute('aria-label',labels[input.name]);});
   clearTimeout(timer);status.textContent='Please complete the form and CAPTCHA before submitting.';notify('ready');observer.disconnect();
  }
  resize();
 });
 observer.observe(container,{childList:true,subtree:true});
 new ResizeObserver(resize).observe(document.body);
 const script=document.createElement('script');script.src='https://cdn.tutorcruncher.com/socket/latest/socket.js';script.async=true;
 script.onerror=()=>{clearTimeout(timer);unavailable();};
 script.onload=async()=>{
  try{
   if(typeof window.socket!=='function')throw new Error('Socket unavailable');
   await window.socket(document.body.dataset.socketKey,{
    mode:'enquiry',element:'#socket-enquiry',router_mode:'history',url_root:'/',
    messages:{enquiry:'Enter your contact details and we will get in touch to discuss suitable support.',submit_enquiry:'Submit Enquiry',enquiry_submitted_thanks:'Thank you. Your enquiry has been submitted to EFL Tutors.'},
    event_callback:(event)=>{if(event==='enquiry_submitted'){status.textContent='Your enquiry has been submitted.';notify('submitted');resize();}}
   });
  }catch{clearTimeout(timer);unavailable();}
 };
 document.head.append(script);
})();
