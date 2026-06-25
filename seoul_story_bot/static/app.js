// 이야기가 있는 여행 — 새 흐름(도→시→OTT/연예인→작품→동선), 웹/모바일 별도 레이아웃
let lang = localStorage.getItem("lang") || "ko";
let L = {};
let mode = "";  // 'web' | 'mobile'
const S = { province: null, provinceName: "", city: null, cityName: "",
            method: null, pickId: null, pickName: "",
            work: null, workTitle: "", stops: [], stopIndex: 0 };

function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function $(id){return document.getElementById(id);}
async function api(path){ const r = await fetch(path); if(!r.ok) throw new Error(r.status); return r.json(); }

// ---- 레이아웃 모드(웹/모바일 별도) ----
function detectMode(){ return window.innerWidth >= 1000 ? "web" : "mobile"; }
function applyMode(){ const m = detectMode(); if(m !== mode){ mode = m; document.body.className = mode; } }
window.addEventListener("resize", applyMode);

// ---- 부트 / 언어 ----
async function boot(){
  applyMode();
  try{ const ui = await api(`/api/ui?lang=${lang}`); L = ui.labels || {}; }catch(e){ L = {}; }
  $("hero-title").textContent = L.hero_title || "이야기가 있는 여행";
  $("hero-sub").textContent = L.hero_sub || "";
  $("foot").textContent = L.foot || "";
  $("lang-ko").classList.toggle("on", lang === "ko");
  $("lang-en").classList.toggle("on", lang === "en");
  showProvince();
}
async function setLang(l){ lang = l; localStorage.setItem("lang", l); document.documentElement.lang = l; await boot(); }

// ---- 공통 렌더 헬퍼 ----
function setApp(...nodes){ const a = $("app"); a.innerHTML = ""; nodes.forEach(n => a.appendChild(n)); window.scrollTo({top:0, behavior:"smooth"}); }
function sectionTitle(t){ const h = document.createElement("h2"); h.className = "section-title"; h.textContent = t; return h; }
function grid(cls){ const d = document.createElement("div"); d.className = "grid " + (cls||""); return d; }
function card(html, onclick, extraCls){
  const d = document.createElement("div"); d.className = "card " + (extraCls||""); d.innerHTML = html;
  if(onclick) d.onclick = onclick; return d;
}
function crumbs(items){  // items: [{label, go?}]  마지막이 현재
  const c = $("crumbs"); c.innerHTML = "";
  if(items.length > 1){
    const prev = items[items.length - 2];
    const b = document.createElement("button"); b.className = "back-btn";
    b.textContent = "← " + (L.nav_back || "뒤로");
    b.onclick = prev.go || showProvince;
    c.appendChild(b);
  }
  const trail = document.createElement("div"); trail.className = "trail";
  items.forEach((it,i)=>{
    const span = document.createElement("span");
    span.className = "crumb" + (i === items.length-1 ? " cur" : "");
    span.textContent = it.label;
    if(it.go && i < items.length-1){ span.classList.add("link"); span.onclick = it.go; }
    trail.appendChild(span);
    if(i < items.length-1){ const sep = document.createElement("span"); sep.className="sep"; sep.textContent="›"; trail.appendChild(sep); }
  });
  c.appendChild(trail);
}
function kindLabel(kind){
  return ({actor:L.kind_actor||"배우", idol:L.kind_idol||"아이돌", ott:L.kind_ott||"OTT", broadcaster:L.kind_broadcaster||"채널"})[kind] || "";
}
function homeCrumb(){ return {label:L.nav_home||"처음으로", go:showProvince}; }
function provCrumb(){ return {label:S.provinceName, go:()=>showCity({id:S.province, name:S.provinceName})}; }
function cityCrumb(){ return {label:S.cityName, go:()=>showMethod({id:S.city, name:S.cityName})}; }

// ---- 1. 도 ----
async function showProvince(){
  S.method=null; S.pickId=null; S.work=null;
  crumbs([{label:L.nav_home||"처음으로"}]);
  let provs; try{ provs = await api(`/api/provinces?lang=${lang}`); }catch(e){ return errBox(); }
  const g = grid("prov");
  provs.forEach(p=>{
    const badge = p.has_data ? "" : `<span class="badge soon">${esc(L.no_data||"준비 중")}</span>`;
    g.appendChild(card(`<div class="cname">${esc(p.name)}</div>${badge}`,
      p.has_data ? ()=>showCity(p) : null, p.has_data ? "" : "disabled"));
  });
  setApp(sectionTitle(L.step_province||"여행할 지역을 골라보세요"), g);
}

// ---- 2. 시 ----
async function showCity(p){
  S.province=p.id; S.provinceName=p.name;
  crumbs([homeCrumb(), {label:p.name}]);
  let cities; try{ cities = await api(`/api/cities?province=${p.id}&lang=${lang}`); }catch(e){ return errBox(); }
  if(!cities.length){ const e=document.createElement("p"); e.className="empty"; e.textContent=L.no_data||"준비 중"; return setApp(sectionTitle(p.name), e); }
  const g = grid("city");
  cities.forEach(ct=>{
    const badge = ct.has_data ? "" : `<span class="badge soon">${esc(L.no_data||"준비 중")}</span>`;
    g.appendChild(card(`<div class="cname">${esc(ct.name)}</div>${badge}`,
      ct.has_data ? ()=>showMethod(ct) : null, ct.has_data ? "" : "disabled"));
  });
  setApp(sectionTitle(L.step_city||"도시를 골라보세요"), g);
}

// ---- 3. 방식(OTT/연예인) ----
function showMethod(ct){
  S.city=ct.id; S.cityName=ct.name;
  crumbs([homeCrumb(), provCrumb(), {label:ct.name}]);
  const g = grid("method");
  g.appendChild(card(`<div class="big">${esc(L.by_ott||"OTT·채널로")}</div><div class="desc">${esc(L.by_ott_desc||"")}</div>`, ()=>showPicker("platform"), "method-card"));
  g.appendChild(card(`<div class="big">${esc(L.by_person||"연예인으로")}</div><div class="desc">${esc(L.by_person_desc||"")}</div>`, ()=>showPicker("person"), "method-card"));
  setApp(sectionTitle(L.step_method||"어떻게 찾을까요?"), g);
}

// ---- 3b. 플랫폼/연예인 선택 ----
async function showPicker(kind){
  const isP = kind === "platform";
  crumbs([homeCrumb(), provCrumb(), cityCrumb(), {label: isP ? (L.step_platform||"OTT·채널") : (L.step_person||"연예인")}]);
  let items; try{ items = await api(`/api/${isP?"platforms":"persons"}?city=${S.city}&lang=${lang}`); }catch(e){ return errBox(); }
  const g = grid("pick");
  items.forEach(p=>{
    g.appendChild(card(
      `<div class="pname">${esc(p.name)}</div><div class="pmeta">${esc(kindLabel(p.kind))} · ${p.count}${esc(L.works_unit||"")}</div>`,
      ()=>showWorks(kind, p.id, p.name), "pick-card"));
  });
  setApp(sectionTitle(isP ? (L.step_platform||"OTT·채널을 골라보세요") : (L.step_person||"연예인을 골라보세요")), g);
}

// ---- 4. 작품 ----
async function showWorks(kind, id, name){
  S.method=kind; S.pickId=id; S.pickName=name;
  crumbs([homeCrumb(), provCrumb(), cityCrumb(), {label:name, go:()=>showPicker(kind)}]);
  const q = kind === "platform" ? `platform=${id}` : `person=${id}`;
  let works; try{ works = await api(`/api/works?city=${S.city}&${q}&lang=${lang}`); }catch(e){ return errBox(); }
  const g = grid("works");
  works.forEach(w=>{
    const badge = w.has_route
      ? `<span class="badge ready">${esc(L.badge_ready||"동선 있음")}</span>`
      : `<span class="badge soon">${esc(L.badge_soon||"동선 준비 중")}</span>`;
    g.appendChild(card(`<div class="wtitle">${esc(w.title)}</div><div class="wsum">${esc(w.summary)}</div>${badge}`,
      ()=>showRoute(w.work_id, name), w.has_route ? "work ok" : "work soon"));
  });
  setApp(sectionTitle(`${esc(name)} · ${L.step_work||"작품을 골라보세요"}`), g);
}

// ---- 5. 동선 ----
async function showRoute(workId, pickName){
  let route; try{ route = await api(`/api/route?city=${S.city}&work=${workId}&lang=${lang}`); }
  catch(e){ route = {stops:[], work_title:""}; }
  S.work=workId; S.workTitle=route.work_title||""; S.stops=route.stops||[]; S.stopIndex=0;
  crumbs([homeCrumb(), provCrumb(), cityCrumb(),
          {label:pickName||S.pickName, go:()=>showWorks(S.method, S.pickId, S.pickName)},
          {label:S.workTitle}]);
  if(S.stops.length === 0){
    const wrap=document.createElement("div"); wrap.className="route-soon";
    wrap.innerHTML = `<div class="soon-icon">🗺️</div><p>${esc(L.route_soon||"이 작품의 동선은 준비 중이에요.")}</p>`;
    return setApp(sectionTitle(S.workTitle), wrap);
  }
  renderRouteShell();
}

function renderRouteShell(){
  const wrap = document.createElement("div"); wrap.className = "route";
  wrap.innerHTML = `
    <div class="route-head"><h2 class="route-title">${esc(S.workTitle)}</h2><div id="steps" class="steps"></div></div>
    <div id="stop-area"></div>
    <div class="nav">
      <button id="prev-btn" class="ghost" onclick="moveStop(-1)">${esc(L.prev||"← 이전")}</button>
      <span id="stop-indicator"></span>
      <button id="next-btn" class="ghost" onclick="moveStop(1)">${esc(L.next||"다음 →")}</button>
    </div>
    <div class="ask-box">
      <h3>${esc(L.ask_title||"이 작품·장소에 대해 물어보기")}</h3>
      <div class="ask-row">
        <input id="question" type="text" placeholder="${esc(L.ask_ph||"")}" onkeydown="if(event.key==='Enter')askQuestion()" />
        <button class="primary" onclick="askQuestion()">${esc(L.ask_btn||"질문")}</button>
      </div>
      <div id="answer" class="answer"></div>
    </div>`;
  setApp(wrap);
  renderStop();
}

function renderStop(){
  const s = S.stops[S.stopIndex];
  const isModel = (s.stop_type||"").indexOf("원형") >= 0 || /model/i.test(s.stop_type||"");
  const mq = encodeURIComponent(s.map_query || s.name);
  const mapEmbed = `https://maps.google.com/maps?q=${mq}&z=16&hl=${lang}&ie=UTF8&output=embed`;
  const mapBig = `https://www.google.com/maps/search/?api=1&query=${mq}`;
  const chips = (s.theme_exp||"").split(/[,·]/).map(t=>t.trim()).filter(Boolean).map(t=>`<span class="chip">${esc(t)}</span>`).join("");
  const visitBlock = s.visit ? `<div class="block"><div class="label">${esc(L.lbl_visit||"방문 정보")}</div><div class="text">${esc(s.visit)}</div></div>` : "";
  const crossBlock = (s.cross && s.cross.length)
    ? `<div class="block"><div class="label">${esc(L.cross_label||"이 장소에서 함께 촬영된 작품")}</div><div class="chips">${
        s.cross.map(x=>`<span class="chip cross" onclick="crossTo('${esc(x.work_id)}')">${esc(x.title)}</span>`).join("")}</div></div>` : "";
  $("stop-area").innerHTML = `
    <div class="stop">
      <div class="stop-media">
        <span class="badge ${isModel?"wonhyeong":"site"}">${esc(s.stop_type)}</span>
        <div class="place-name">${esc(s.name)}</div>
        <div class="place-area">${esc(s.area)}</div>
        <iframe class="map-frame" src="${mapEmbed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="${esc(s.name)}"></iframe>
        <a class="map-link" href="${mapBig}" target="_blank" rel="noopener">${esc(L.map_open||"큰 지도로 열기 →")}</a>
      </div>
      <div class="stop-text">
        <div class="block"><div class="label">${esc(L.lbl_story||"콘텐츠 × 장소 이야기")}</div><div class="text">${esc(s.story_text)}</div></div>
        <div class="block"><div class="label">${esc(L.lbl_place||"장소 이야기")}</div><div class="text">${esc(s.place_story)}</div></div>
        ${visitBlock}
        <div class="block"><div class="label">${esc(L.lbl_theme||"주변 테마 체험")}</div><div class="chips">${chips}</div></div>
        ${crossBlock}
      </div>
    </div>`;
  $("stop-indicator").textContent = (L.stop_fmt||"{i}/{n}").replace("{i}", S.stopIndex+1).replace("{n}", S.stops.length);
  $("prev-btn").disabled = S.stopIndex === 0;
  $("next-btn").disabled = S.stopIndex === S.stops.length-1;
  const sb = $("steps"); sb.innerHTML = "";
  S.stops.forEach((_,i)=>{
    if(i>0){ const bar=document.createElement("span"); bar.className="bar"; sb.appendChild(bar); }
    const dot=document.createElement("span"); dot.className="dot"+(i===S.stopIndex?" active":""); sb.appendChild(dot);
  });
}
function moveStop(d){ const n = S.stopIndex + d; if(n<0 || n>=S.stops.length) return; S.stopIndex = n; renderStop(); const a=$("answer"); if(a) a.textContent=""; }
function crossTo(workId){ showRoute(workId, S.pickName); }

async function askQuestion(){
  const inp = $("question"); const q = inp.value.trim(); if(!q) return;
  const out = $("answer"); out.className = "answer thinking"; out.textContent = L.thinking || "…";
  try{
    const r = await fetch("/api/ask", {method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({city:S.city, work:S.work, question:q, lang})});
    const data = await r.json(); out.className = "answer"; out.textContent = data.answer;
  }catch(e){ out.className = "answer"; out.textContent = lang==="en"?"Couldn't get an answer. Please try again.":"답변을 불러오지 못했어요. 잠시 후 다시 시도해 주세요."; }
}

function errBox(){
  const e = document.createElement("div"); e.className = "loading";
  e.textContent = lang==="en" ? "Couldn't load. Check the server and refresh." : "불러오지 못했어요. 서버 상태를 확인하고 새로고침해 주세요.";
  setApp(e);
}

boot();
