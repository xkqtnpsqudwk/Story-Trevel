// 화면 로직 (바닐라 JS)
// 흐름: 콘텐츠 목록 → 선택 → 동선 조회 → 지점 이동 → 질문

let currentContentId = null;
let stops = [];
let stopIndex = 0;

// HTML 이스케이프 (데이터에 <,> 등이 들어와도 안전하게 표시)
function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// 콘텐츠 목록 불러오기 (F1)
async function loadContents() {
  const box = document.getElementById("content-list");
  try {
    const res = await fetch("/api/contents");
    const contents = await res.json();
    box.innerHTML = "";
    contents.forEach((c) => {
      const div = document.createElement("div");
      div.className = "card";
      div.onclick = () => selectContent(c.content_id);
      div.innerHTML = `<h3>${esc(c.title)}</h3><p>${esc(c.summary)}</p>`;
      box.appendChild(div);
    });
  } catch (e) {
    box.innerHTML = '<div class="loading">콘텐츠를 불러오지 못했어요.</div>';
  }
}

// 콘텐츠 선택 → 동선 조회 (F2)
async function selectContent(cid) {
  currentContentId = cid;
  const res = await fetch(`/api/route/${cid}`);
  if (!res.ok) { alert("이 콘텐츠의 동선이 아직 없어요."); return; }
  const route = await res.json();
  stops = route.stops;
  stopIndex = 0;
  document.getElementById("route-title").textContent = route.title;
  document.getElementById("step-contents").classList.add("hidden");
  document.getElementById("step-route").classList.remove("hidden");
  document.getElementById("answer").textContent = "";
  renderSteps();
  renderStop();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// 동선 진행 점(dot) 표시
function renderSteps() {
  const box = document.getElementById("steps");
  box.innerHTML = "";
  stops.forEach((_, i) => {
    if (i > 0) { const bar = document.createElement("span"); bar.className = "bar"; box.appendChild(bar); }
    const dot = document.createElement("span");
    dot.className = "dot" + (i === stopIndex ? " active" : "");
    box.appendChild(dot);
  });
}

// 현재 지점의 해설·체험 그리기 (F3·F4)
function renderStop() {
  const s = stops[stopIndex];
  const isWonhyeong = s.stop_type === "세계관 원형";
  // 카카오 지도 검색 링크 (장소 이름으로 검색)
  const mq = encodeURIComponent(s.map_query || s.name);
  const mapEmbed = `https://www.google.com/maps?q=${mq}&z=16&hl=ko&output=embed`;
  const mapBig = `https://www.google.com/maps/search/?api=1&query=${mq}`;
  // 주변 체험을 칩으로 (쉼표·가운뎃점 기준 분리)
  const chips = s.theme_exp.split(/[,·]/).map((t) => t.trim()).filter(Boolean)
    .map((t) => `<span class="chip">${esc(t)}</span>`).join("");

  document.getElementById("stop-area").innerHTML = `
    <div class="stop">
      <span class="badge ${isWonhyeong ? "wonhyeong" : ""}">${esc(s.stop_type)}</span>
      <div class="place-name">${esc(s.name)}</div>
      <div class="place-area">${esc(s.area)}</div>
      <iframe class="map-frame" src="${mapEmbed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="${esc(s.name)} 지도"></iframe>
      <a class="map-link" href="${mapBig}" target="_blank" rel="noopener">큰 지도로 열기 →</a>

      <div class="block">
        <div class="label">콘텐츠 × 장소 이야기</div>
        <div class="text">${esc(s.story_text)}</div>
      </div>
      <div class="block">
        <div class="label">장소 이야기</div>
        <div class="text">${esc(s.place_story)}</div>
      </div>
      <div class="block">
        <div class="label">주변 테마 체험</div>
        <div class="chips">${chips}</div>
      </div>
    </div>`;

  document.getElementById("stop-indicator").textContent = `${stopIndex + 1} / ${stops.length} 지점`;
  document.getElementById("prev-btn").disabled = stopIndex === 0;
  document.getElementById("next-btn").disabled = stopIndex === stops.length - 1;
  renderSteps();
}

function moveStop(delta) {
  const next = stopIndex + delta;
  if (next < 0 || next >= stops.length) return;
  stopIndex = next;
  renderStop();
}

function resetToContents() {
  document.getElementById("step-route").classList.add("hidden");
  document.getElementById("step-contents").classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// 질문하기 (F5)
async function askQuestion() {
  const input = document.getElementById("question");
  const q = input.value.trim();
  if (!q) return;
  const out = document.getElementById("answer");
  out.className = "answer thinking";
  out.textContent = "답변을 생각하는 중…";
  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content_id: currentContentId, question: q }),
    });
    const data = await res.json();
    out.className = "answer";
    out.textContent = data.answer;
  } catch (e) {
    out.className = "answer";
    out.textContent = "답변을 가져오지 못했어요.";
  }
}

loadContents();
