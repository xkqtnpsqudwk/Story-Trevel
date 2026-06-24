// 화면 로직 (권역 모델, 다국어)
let lang = localStorage.getItem("lang") || "ko";
let LABELS = {};
let currentContentId = null;
let stops = [];
let stopIndex = 0;

function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function routeOpen(){return !document.getElementById("step-route").classList.contains("hidden");}

async function setLang(l){
  lang=l; localStorage.setItem("lang",l); document.documentElement.lang=l;
  await loadUI(); await loadContents();
  if(currentContentId && routeOpen()){ await selectContent(currentContentId, stopIndex); }
}

async function loadUI(){
  const data = await (await fetch(`/api/ui?lang=${lang}`)).json();
  LABELS = data.labels;
  const set=(id,t)=>{const e=document.getElementById(id); if(e) e.textContent=t;};
  set("hero-title",LABELS.hero_title); set("hero-sub",LABELS.hero_sub);
  set("pick-title",LABELS.pick); set("back-btn",LABELS.back);
  set("prev-btn",LABELS.prev); set("next-btn",LABELS.next);
  set("ask-title",LABELS.ask_title); set("ask-btn",LABELS.ask_btn); set("foot",LABELS.foot);
  const q=document.getElementById("question"); if(q) q.placeholder=LABELS.ask_ph;
  document.getElementById("lang-ko").classList.toggle("on",lang==="ko");
  document.getElementById("lang-en").classList.toggle("on",lang==="en");
}

async function loadContents(){
  const box=document.getElementById("content-list");
  try{
    const contents=await (await fetch(`/api/contents?lang=${lang}`)).json();
    box.innerHTML="";
    contents.forEach(c=>{
      const div=document.createElement("div");
      div.className="card"; div.onclick=()=>selectContent(c.content_id);
      div.innerHTML=`<h3>${esc(c.title)}</h3><p>${esc(c.summary)}</p>`;
      box.appendChild(div);
    });
  }catch(e){ box.innerHTML='<div class="loading">!</div>'; }
}

async function selectContent(cid, keepIndex=0){
  const res=await fetch(`/api/route/${cid}?lang=${lang}`);
  if(!res.ok){ return; }
  const route=await res.json();
  currentContentId=cid; stops=route.stops; stopIndex=Math.min(keepIndex, stops.length-1);
  document.getElementById("route-title").textContent=route.content_title;
  document.getElementById("area-line").textContent=`${LABELS.area_label} · ${route.area_name} — ${route.area_blurb}`;
  document.getElementById("step-contents").classList.add("hidden");
  document.getElementById("step-route").classList.remove("hidden");
  document.getElementById("answer").textContent="";
  renderStop(); window.scrollTo({top:0,behavior:"smooth"});
}

function renderSteps(){
  const box=document.getElementById("steps"); box.innerHTML="";
  stops.forEach((_,i)=>{
    if(i>0){const bar=document.createElement("span");bar.className="bar";box.appendChild(bar);}
    const dot=document.createElement("span"); dot.className="dot"+(i===stopIndex?" active":""); box.appendChild(dot);
  });
}

function renderStop(){
  const s=stops[stopIndex];
  const isModel=(s.stop_type||"").indexOf("원형")>=0 || /model/i.test(s.stop_type);
  const mq=encodeURIComponent(s.map_query||s.name);
  const mapEmbed=`https://www.google.com/maps?q=${mq}&z=16&hl=${lang}&output=embed`;
  const mapBig=`https://www.google.com/maps/search/?api=1&query=${mq}`;
  const chips=(s.theme_exp||"").split(/[,·]/).map(t=>t.trim()).filter(Boolean)
    .map(t=>`<span class="chip">${esc(t)}</span>`).join("");
  const visitBlock=s.visit?`<div class="block"><div class="label">${esc(LABELS.lbl_visit)}</div><div class="text">${esc(s.visit)}</div></div>`:"";
  const crossBlock=(s.cross&&s.cross.length)
    ?`<div class="block"><div class="label">${esc(LABELS.cross_label)}</div><div class="chips">${
        s.cross.map(x=>`<span class="chip cross" onclick="selectContent('${x.content_id}')">${esc(x.title)}</span>`).join("")
      }</div></div>`:"";

  document.getElementById("stop-area").innerHTML=`
    <div class="stop">
      <span class="badge ${isModel?"wonhyeong":""}">${esc(s.stop_type)}</span>
      <div class="place-name">${esc(s.name)}</div>
      <div class="place-area">${esc(s.area)}</div>
      <iframe class="map-frame" src="${mapEmbed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="${esc(s.name)}"></iframe>
      <a class="map-link" href="${mapBig}" target="_blank" rel="noopener">${esc(LABELS.map_open)}</a>
      <div class="block"><div class="label">${esc(LABELS.lbl_story)}</div><div class="text">${esc(s.story_text)}</div></div>
      <div class="block"><div class="label">${esc(LABELS.lbl_place)}</div><div class="text">${esc(s.place_story)}</div></div>
      ${visitBlock}
      <div class="block"><div class="label">${esc(LABELS.lbl_theme)}</div><div class="chips">${chips}</div></div>
      ${crossBlock}
    </div>`;

  document.getElementById("stop-indicator").textContent=(LABELS.stop_fmt||"{i}/{n}").replace("{i}",stopIndex+1).replace("{n}",stops.length);
  document.getElementById("prev-btn").disabled=stopIndex===0;
  document.getElementById("next-btn").disabled=stopIndex===stops.length-1;
  renderSteps();
}

function moveStop(d){const n=stopIndex+d; if(n<0||n>=stops.length)return; stopIndex=n; renderStop();}
function resetToContents(){
  document.getElementById("step-route").classList.add("hidden");
  document.getElementById("step-contents").classList.remove("hidden");
  window.scrollTo({top:0,behavior:"smooth"});
}

async function askQuestion(){
  const input=document.getElementById("question"); const q=input.value.trim(); if(!q)return;
  const out=document.getElementById("answer"); out.className="answer thinking"; out.textContent=LABELS.thinking;
  try{
    const data=await (await fetch("/api/ask",{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({content_id:currentContentId,question:q,lang})})).json();
    out.className="answer"; out.textContent=data.answer;
  }catch(e){ out.className="answer"; out.textContent="!"; }
}

(async function init(){ await loadUI(); await loadContents(); })();
