var E=`<div class="pglite-app-container">

    <h1><tt>pglite</tt></h1>

    <div>Executed commands:</div>
    <div class="code-editor" title="code-editor"></div>
    <div id="pglite-timestamp"></div>
    <hr>
    <div>Result:</div>
    <div title="results"></div>
    <hr>
    <div>Raw Output:</div>
    <div title="output"></div>
</div>`;import{PGlite as R}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";function S(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){let n=Math.random()*16|0;return(t==="x"?n:n&3|8).toString(16)})}var v=new window.AudioContext,M=t=>{if(t){let n=new SpeechSynthesisUtterance(t);window.speechSynthesis.speak(n)}};function D(t=440,n=1e3,i=.1,a="sine",r=null){let o=v.createOscillator(),s=v.createGain();s.gain.value=i,o.type=a,o.frequency.value=t,o.connect(s),s.connect(v.destination),o.start(),s.gain.exponentialRampToValueAtTime(1e-5,v.currentTime+n/1e3),setTimeout(()=>{o.stop(),r&&setTimeout(()=>{M(r)},100)},n)}function b(t=null){D(500,5,.05,"sine",t)}function q(t=null){D(50,400,.1,"sawtooth",t)}var Q=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function L(t){let n=document.createElement("table"),i=n.insertRow();return t.fields.forEach(a=>{let r=document.createElement("th");r.textContent=a.name,i.appendChild(r)}),n}function U(t,n){t.rows.forEach(i=>{let a=n.insertRow();t.fields.forEach(r=>{let o=a.insertCell();o.textContent=String(i[r.name])})})}function I(t){if(t&&t.file_content&&t.file_info){let{file_content:n,file_info:i}=t,a=atob(n),r=new Array(a.length);for(let p=0;p<a.length;p++)r[p]=a.charCodeAt(p);let o=new Uint8Array(r),s=new Blob([o],{type:i.type});return new File([s],i.name,{type:i.type,lastModified:i.lastModified})}return null}function O({model:t,el:n}){let i=t.get("idb"),a=t.get("file_package"),r=I(a),o={};r&&(o.loadDataDir=r);let s=i?new R(i,o):new R(o),g=t.get("headless"),p=document.createElement("div");p.innerHTML=E;let A=S();p.id=A,g&&(p.style="display: none; visibility: hidden;"),n.appendChild(p),t.on("change:datadump",async()=>{if(t.get("datadump")=="generate_dump"){let l=await s.dumpDataDir(),w=new FileReader;w.onload=y=>{let u={name:l.name,size:l.size,type:l.type,lastModified:l.lastModified},m=y.target.result.split(",")[1],_={file_info:u,file_content:m};t.set("file_package",_),t.set("response",{status:"datadump_ready"}),t.save_changes(),t.get("audio")&&b()},w.readAsDataURL(l)}}),t.on("change:code_content",async()=>{function c(e){if(g)return;let d=n.querySelector('div[title="code-editor"]');d.innerHTML=d.innerHTML+"<br>"+e}function l(e){if(g)return;let d=n.querySelector('div[title="output"]'),x=n.querySelector('div[title="results"]');d.innerHTML=JSON.stringify(e);let h=L(e);U(e,h),x.innerHTML="",x.append(h)}function w(e,d){g||(c(e),l(d))}function y(e){t.get("audio")&&q(e.message),t.set("response",{status:"error",error_message:e.message})}let u=t.get("code_content");if(!u)return;let m=t.get("multiline"),_=t.get("multiexec"),f={rows:[],fields:[{name:"",dataTypeID:0}]};if(_)try{c(u);let e=await s.exec(u);l(e[e.length-1]),t.set("response",{status:"completed",response:e,response_type:"multi"})}catch(e){y(e)}else if(m!=""){let e=u.split(m);for(let d of e){let x=d.trim();if(x!==""){c(`${x};`);try{f=await s.query(x),l(f)}catch(h){y(h)}}}t.set("response",{status:"completed",response:f,response_type:"single"})}else{c(u);try{f=await s.query(u),l(f),t.set("response",{status:"completed",response:f,response_type:"single"})}catch(e){y(e)}}t.save_changes(),t.get("audio")&&b()});let T;s.query("select version();").then(c=>{T=c.rows[0],t.set("about",T),t.set("response",{status:"ready"}),t.save_changes()}).catch(c=>{alert(c),console.error("Error executing query:",c)})}var V={render:O};export{V as default};
