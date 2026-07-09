// TravelMind App v3
var currentSessionId = null, eventSource = null, agentResults = {}, isProcessing = false;
var agentStatus = {};
var AGENT_NAMES = ["orchestrator","destination","itinerary","booking","visa","packing","local","summarizer"];
function addMessage(role, content) {
  var c = document.getElementById("chatMessages"), d = document.createElement("div");
  if (role === "user") {
    d.className = "msg o";
    d.innerHTML = '<div class="bb us">' + content + '</div><div class="av" style="background:linear-gradient(135deg,#D97706,#EA580C);color:white">王</div>';
  } else {
    d.className = "msg";
    d.innerHTML = '<div class="av" style="background:linear-gradient(135deg,#1E3A5F,#4A8BC2);color:white">🧳</div><div class="bb ai">' + content + '</div>';
  }
  c.appendChild(d); c.scrollTop = c.scrollHeight;
}
function showTyping() {
  if (document.getElementById("typingEl")) return;
  var d = document.createElement("div"); d.className = "msg"; d.id = "typingEl";
  d.innerHTML = '<div class="av" style="background:linear-gradient(135deg,#1E3A5F,#4A8BC2);color:white">🧳</div><div class="bb ai"><span class="ld"></span>正在处理你的需求...</div>';
  document.getElementById("chatMessages").appendChild(d);
  document.getElementById("chatMessages").scrollTop = document.getElementById("chatMessages").scrollHeight;
}
function hideTyping() { var e = document.getElementById("typingEl"); if (e) e.remove(); }
function updateAgentStatus(name, status) {
  agentStatus[name] = status;
  var done = 0, run = 0;
  for (var i = 0; i < AGENT_NAMES.length; i++) {
    var n = AGENT_NAMES[i];
    if (agentStatus[n] === "completed" || agentStatus[n] === "done") done++;
    if (agentStatus[n] === "running") run++;
  }
  var badge = document.getElementById("agentBadge");
  if (!badge) return;
  if (run > 0) badge.innerHTML = '<span class="nm">' + done + "/" + AGENT_NAMES.length + '</span> 运行中...';
  else badge.innerHTML = '<span class="nm">' + AGENT_NAMES.length + '</span> Agents <span style="margin-left:4px;font-size:10px;color:var(--stone-400)">🧠→📋→📝</span>';
}
function startStream(sid) {
  if (eventSource) eventSource.close();
  currentSessionId = sid; agentStatus = {};
  for (var i = 0; i < AGENT_NAMES.length; i++) agentStatus[AGENT_NAMES[i]] = "pending";
  eventSource = new EventSource("/api/travel/stream/" + sid);
  eventSource.onmessage = function(e) { try { handleEvent(JSON.parse(e.data)); } catch(err) {} };
  eventSource.onerror = function() { eventSource.close(); hideTyping(); isProcessing = false; updateSendBtn(); };
}
function handleEvent(data) {
  var ev = data.event, p = data.data || {};
  switch(ev) {
    case "agent_start": updateAgentStatus(p.agent_name, "running"); showTyping(); break;
    case "agent_complete": updateAgentStatus(p.agent_name, "completed"); agentResults[p.agent_name] = p.result; hideTyping(); break;
    case "agent_error": updateAgentStatus(p.agent_name, "error"); hideTyping(); break;
    case "workflow_complete": hideTyping(); isProcessing = false; updateSendBtn();
      if (p && p.outputs) { agentResults = p.outputs; renderReport(p.outputs); addMessage("assistant", "旅行方案已生成，在右侧可以查看每日安排、费用明细等详情。"); } break;
    case "workflow_error": hideTyping(); isProcessing = false; updateSendBtn(); addMessage("assistant", "抱歉，生成方案时出现错误，请重试。"); break;
    case "done": eventSource.close(); isProcessing = false; updateSendBtn(); break;
  }
}
function updateSendBtn() {
  var btn = document.getElementById("sendBtn");
  if (!btn) return;
  btn.disabled = isProcessing;
  if (isProcessing) {
    btn.innerHTML = '<div style="display:flex;gap:2px;align-items:center;justify-content:center;height:100%"><div style="width:4px;height:4px;border-radius:50%;background:white;animation:bounce 1.4s infinite"></div><div style="width:4px;height:4px;border-radius:50%;background:white;animation:bounce 1.4s .2s infinite"></div><div style="width:4px;height:4px;border-radius:50%;background:white;animation:bounce 1.4s .4s infinite"></div></div>';
  } else {
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M22 2L11 13"/><path d="M22 2L15 22L11 13L2 9L22 2z"/></svg>';
  }
}
async function sendMessage() {
  if (isProcessing) return;
  var text = document.getElementById("chatInput").value.trim();
  if (!text) return;
  isProcessing = true; updateSendBtn();
  addMessage("user", document.getElementById("chatInput").value);
  document.getElementById("chatInput").value = "";
  var wc = document.getElementById("welcomeScreen");
  if (wc) wc.style.display = "none";
  showTyping();
  try {
    var r = await fetch("/api/travel", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({message: text}) });
    var d = await r.json();
    startStream(d.session_id);
  } catch(e) {
    hideTyping(); isProcessing = false; updateSendBtn();
    addMessage("assistant", "网络错误，请检查连接后重试。");
  }
}
function useExample(text) { document.getElementById("chatInput").value = text; sendMessage(); }
var currentTab = "overview";
function renderReport(outputs) {
  document.getElementById("resultsContainer").innerHTML = '<div class="report-container">' + renderHero(outputs) + renderTabs() + '<div id="reportContent" class="report-content">' + renderOverviewTab(outputs) + '</div></div>';
}
function renderHero(o) {
  var dest = o.destination || {}, itin = o.itinerary || {}, b = o.booking || {};
  var dName = dest.destination || itin.destination || "目的地", days = itin.days || 5;
  var bMin = "", bSav = "";
  if (b.budget_estimate) { bMin = b.budget_estimate.flight_min + b.budget_estimate.hotel_min * days; bSav = "预算参考"; }
  return '<div class="hero"><div class="hm"><div class="ic">🗾</div><div class="in"><h1>' + dName + " " + days + ' 日旅行方案</h1><div class="tg"><span>🌸 最佳季节</span><span>🍜 地道美食</span><span>🎯 智能规划</span></div></div></div><div class="hd"><div class="lb">预算参考</div><div class="am">¥' + (bMin || "待估算") + '</div>' + (bSav ? '<div class="sv">' + bSav + "</div>" : "") + '</div></div>';
}
function renderTabs() {
  return '<div class="tr"><button class="act" onclick="switchTab(\'overview\')">📋 行程总览</button><button onclick="switchTab(\'cost\')">💰 费用明细</button><button onclick="switchTab(\'packing\')">🎒 行李清单</button><button onclick="switchTab(\'info\')">📍 实用信息</button></div>';
}
function switchTab(tab) {
  currentTab = tab;
  var btns = document.querySelectorAll(".tr button");
  for (var i = 0; i < btns.length; i++) btns[i].classList.remove("act");
  var idx = ["overview","cost","packing","info"].indexOf(tab);
  if (btns[idx]) btns[idx].classList.add("act");
  var el = document.getElementById("reportContent");
  if (tab === "overview") el.innerHTML = renderOverviewTab(agentResults);
  else if (tab === "cost") el.innerHTML = renderCostTab(agentResults);
  else if (tab === "packing") el.innerHTML = renderPackingTab(agentResults);
  else el.innerHTML = renderInfoTab(agentResults);
}
function renderFlightTable(b) {
  var flights = b.flights || [];
  if (flights.length === 0) return '<div class="card tw"><div class="th"><div class="tl"><span class="ico">✈️</span><span class="tx">航班推荐</span></div></div><div style="padding:20px;text-align:center;color:var(--stone-400);font-size:13px">暂无数据</div></div>';
  var minP = Math.min.apply(null, flights.map(function(f) { return f.price; }));
  var rows = "";
  for (var i = 0; i < flights.length; i++) {
    var f = flights[i];
    rows += '<tr><td>' + f.airline + " " + f.flight;
    if (f.price === minP) rows += ' <span class="rc"><span class="st">★</span> 推荐</span>';
    rows += '</td><td>' + (f.departure || "") + "–" + (f.arrival || "") + '</td><td style="text-align:right"><span class="pr' + (f.price === minP ? " gn" : "") + '">¥' + f.price + '</span></td></tr>';
  }
  return '<div class="card tw"><div class="th"><div class="tl"><span class="ico">✈️</span><span class="tx">航班推荐</span></div><span class="bg gn">最低 ¥' + minP + '</span></div><table><thead><tr><th>航班</th><th>时间</th><th style="text-align:right">价格</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
}
function renderHotelTable(b) {
  var hotels = b.hotels || [];
  if (hotels.length === 0) return '<div class="card tw"><div class="th"><div class="tl"><span class="ico">🏨</span><span class="tx">酒店推荐</span></div></div><div style="padding:20px;text-align:center;color:var(--stone-400);font-size:13px">暂无数据</div></div>';
  var minP = Math.min.apply(null, hotels.map(function(h) { return h.price_per_night; }));
  var rows = "";
  for (var i = 0; i < hotels.length; i++) {
    var h = hotels[i]; var stars = "";
    for (var s = 0; s < (h.stars || 3); s++) stars += "★";
    var isMin = h.price_per_night === minP;
    rows += '<tr><td>' + h.name + ' <span style="color:var(--stone-400);font-size:11px">' + stars + '</span></td><td>' + h.rating + '</td><td style="text-align:right"><span class="pr' + (isMin ? " gn" : "") + '">¥' + h.price_per_night + '</span></td></tr>';
  }
  return '<div class="card tw"><div class="th"><div class="tl"><span class="ico">🏨</span><span class="tx">酒店推荐</span></div><span class="bg gn">¥' + minP + '/晚起</span></div><table><thead><tr><th>酒店</th><th>评分</th><th style="text-align:right">价格/晚</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
}
function renderOverviewTab(o) {
  var itin = o.itinerary || {}, days = itin.itinerary || [], html = '<div class="g3">';
  for (var i = 0; i < days.length; i++) {
    var d = days[i];
    html += '<div class="card"><div class="ch"><div class="no ' + (d.day === 1 ? "bl" : "gr") + '">' + d.day + '</div><div class="ti"><div class="tt">' + (d.title || "第" + d.day + "天") + '</div></div></div><div class="cb">';
    var acts = d.activities || [];
    for (var j = 0; j < acts.length; j++) {
      var a = acts[j], cls = "mo";
      if (a.time && a.time.indexOf("下午") > -1) cls = "af";
      if (a.time && a.time.indexOf("晚上") > -1) cls = "ev";
      html += '<div class="ac"><span class="tm ' + cls + '">' + (a.time || "") + '</span><div class="d"><p>' + (a.activity || "") + '</p><div class="s">' + (a.description || "") + '</div></div></div>';
    }
    html += '</div></div>';
  }
  html += '</div><div class="g2">';
  html += renderFlightTable(o.booking || {});
  html += renderPackingCard(o.packing || {});
  html += renderHotelTable(o.booking || {});
  html += renderVisaCard(o.visa || {});
  html += '</div>';
  return html;
}
function renderPackingCard(p) {
  var items1 = (p.essentials || []).slice(0,4);
  var items2 = (p.clothing || []).concat(p.electronics || []).slice(0,4);
  var tip = p.weather_tip || "建议根据目的地天气准备合适衣物";
  function mk(arr) { var h = ""; for (var i = 0; i < arr.length; i++) h += '<div class="it"><span class="ck">✓</span>' + arr[i] + '</div>'; return h; }
  return '<div class="card"><div class="tc"><div class="thdr"><div class="tl"><span class="ico">🎒</span><span class="tx">行李清单</span></div><span class="bg am">建议携带</span></div><div class="g2i"><div class="gs"><div class="gt">📄 必备品</div>' + mk(items1) + '</div><div class="gs"><div class="gt">👔 衣物/电子</div>' + mk(items2) + '</div></div><div class="fn">🌤 ' + tip + '</div></div></div>';
}
function renderVisaCard(v) {
  var status = v && v.status ? v.status : "待查询";
  var isFree = status && (status.indexOf("免签") > -1 || status === "无需签证");
  var color = isFree ? "gn" : "am", txt = isFree ? "无需签证" : "需要办理";
  var h = '<div class="card"><div class="th" style="border-bottom:1px solid var(--stone-200)"><div class="tl"><span class="ico">🛂</span><span class="tx">签证信息</span></div><span class="bg ' + color + '">' + txt + '</span></div><div class="vg"><div class="vi"><div class="vl">状态</div><div class="vv" style="color:' + (isFree ? "var(--em)" : "var(--amber)") + '">' + status + '</div></div>';
  if (v && v.country) h += '<div class="vi"><div class="vl">目的地</div><div class="vv">' + v.country + '</div></div>';
  if (v && v.processing_days) h += '<div class="vi"><div class="vl">办理时间</div><div class="vv">' + v.processing_days + '</div></div>';
  if (v && v.fee) h += '<div class="vi"><div class="vl">费用</div><div class="vv">' + v.fee + '</div></div>';
  h += '</div>';
  if (v && v.notes) h += '<div class="vn">💡 ' + v.notes + '</div>';
  return h + '</div>';
}
function renderCostTab(o) { return '<div class="g2">' + renderFlightTable(o.booking || {}) + renderHotelTable(o.booking || {}) + '</div>'; }
function renderPackingTab(o) {
  var p = o.packing || {};
  function mk(arr) { var h = ""; for (var i = 0; i < (arr || []).length; i++) h += '<div class="it"><span class="ck">✓</span>' + arr[i] + '</div>'; return h; }
  return '<div class="card"><div class="tc"><div class="thdr"><div class="tl"><span class="ico">🎒</span><span class="tx">行李清单</span></div></div><div class="g2i"><div class="gs"><div class="gt">📄 必备证件</div>' + mk(p.essentials) + '</div><div class="gs"><div class="gt">👔 穿搭建议</div>' + mk(p.clothing) + '</div></div><div class="g2i" style="margin-top:12px"><div class="gs"><div class="gt">📱 电子产品</div>' + mk(p.electronics) + '</div><div class="gs"><div class="gt">💊 健康防护</div>' + mk(p.health) + '</div></div></div></div>';
}
function renderInfoTab(o) {
  var local = o.local || {}, dest = o.destination || {}, h = '<div class="g2">';
  h += '<div class="card"><div class="th" style="border-bottom:1px solid var(--stone-200)"><div class="tl"><span class="ico">📍</span><span class="tx">实用信息</span></div></div><div class="vg"><div class="vi"><div class="vl">国家</div><div class="vv">' + (local.country || dest.country || "") + '</div></div><div class="vi"><div class="vl">语言</div><div class="vv">' + (local.language || dest.language || "") + '</div></div><div class="vi"><div class="vl">货币</div><div class="vv">' + (local.currency || dest.currency || "") + '</div></div><div class="vi"><div class="vl">时区</div><div class="vv">' + (local.timezone || dest.timezone || "") + '</div></div></div></div>';
  h += renderVisaCard(o.visa || {});
  h += '</div>';
  if (dest.tips && dest.tips.length > 0) {
    h += '<div class="card" style="margin-top:12px;padding:16px"><div style="display:flex;align-items:center;gap:8px;margin-bottom:10px"><span style="font-size:18px">💡</span><span style="font-size:13px;font-weight:600">当地小贴士</span></div>';
    for (var i = 0; i < dest.tips.length; i++) h += '<div style="font-size:12px;padding:4px 0;color:var(--stone-500)">• ' + dest.tips[i] + '</div>';
    h += '</div>';
  }
  return h;
}
