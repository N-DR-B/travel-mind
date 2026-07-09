/* ===== TravelMind Frontend App ===== */

let currentSessionId = null;
let eventSource = null;
let agentResults = {};
let isProcessing = false;

// === Theme ===
function initTheme() {
    const saved = localStorage.getItem("tm-theme") || "light";
    if (saved === "dark") document.documentElement.classList.add("dark");
    updateThemeIcon(saved);
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle("dark");
    const theme = isDark ? "dark" : "light";
    localStorage.setItem("tm-theme", theme);
    updateThemeIcon(theme);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById("themeBtn");
    if (btn) btn.innerHTML = theme === "dark" ? '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>' : '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
}

// === Chat ===
function addMessage(role, content) {
    const container = document.getElementById("chatMessages");
    const div = document.createElement("div");
    div.className = `msg msg-${role}`;

    if (role === "assistant" && typeof content === "object") {
        div.textContent = JSON.stringify(content, null, 2);
    } else {
        div.textContent = content;
    }
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function showTyping() {
    const container = document.getElementById("chatMessages");
    const div = document.createElement("div");
    div.className = "msg msg-typing";
    div.id = "typingIndicator";
    div.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById("typingIndicator");
    if (el) el.remove();
}

// === Agent Workflow ===
function initWorkflow() {
    ["orchestrator","destination","itinerary","booking","visa","packing","local","summarizer"].forEach(name => {
        const card = document.getElementById(`agent-${name}`);
        if (card) {
            card.className = "agent-card status-pending";
        }
    });
}

function updateAgentStatus(agentName, status, message) {
    const card = document.getElementById(`agent-${agentName}`);
    if (!card) return;
    card.className = `agent-card status-${status}`;
    const textEl = card.querySelector(".agent-status-text");
    if (textEl) {
        const msgs = {
            pending: "等待执行",
            running: "正在处理...",
            completed: "已完成",
            error: "处理出错"
        };
        textEl.textContent = message || msgs[status] || status;
    }
    const badge = card.querySelector(".agent-status-badge");
    if (badge) {
        const labels = { pending: "等待", running: "执行中", completed: "✓ 完成", error: "✗ 错误" };
        badge.textContent = labels[status] || status;
    }
}

// === SSE Events ===
function startStream(sessionId) {
    if (eventSource) eventSource.close();
    currentSessionId = sessionId;

    // Load agents and show workflow
    initWorkflow();

    eventSource = new EventSource(`/api/travel/stream/${sessionId}`);

    eventSource.onmessage = function(e) {
        try {
            const data = JSON.parse(e.data);
            handleEvent(data);
        } catch (err) {
            console.log("SSE raw:", e.data);
        }
    };

    eventSource.onerror = function() {
        console.log("SSE connection closed");
        eventSource.close();
        hideTyping();
        isProcessing = false;
        updateSendBtn();
    };
}

function handleEvent(data) {
    const { event, data: payload } = data;

    switch (event) {
        case "agent_start":
            updateAgentStatus(payload.agent_name, "running");
            showTyping();
            break;

        case "agent_complete":
            updateAgentStatus(payload.agent_name, "completed");
            agentResults[payload.agent_name] = payload.result;
            hideTyping();
            break;

        case "agent_error":
            updateAgentStatus(payload.agent_name, "error", payload.error);
            hideTyping();
            break;

        case "workflow_complete":
            hideTyping();
            isProcessing = false;
            updateSendBtn();
            if (payload && payload.outputs) {
                agentResults = payload.outputs;
                renderReport(payload.outputs);
                addMessage("assistant", "旅行方案已生成，您可以在右侧查看详情！");
            }
            break;

        case "workflow_error":
            hideTyping();
            isProcessing = false;
            updateSendBtn();
            addMessage("assistant", "抱歉，生成方案时出现错误，请重试。");
            break;

        case "done":
            eventSource.close();
            isProcessing = false;
            updateSendBtn();
            break;
    }
}

// === Send Message ===
async function sendMessage() {
    if (isProcessing) return;
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;

    isProcessing = true;
    updateSendBtn();

    addMessage("user", text);
    input.value = "";
    input.style.height = "auto";

    initWorkflow();
    showTyping();

    try {
        const resp = await fetch("/api/travel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });
        const data = await resp.json();
        startStream(data.session_id);
    } catch (err) {
        hideTyping();
        isProcessing = false;
        updateSendBtn();
        addMessage("assistant", "网络错误，请检查连接后重试。");
    }
}

function updateSendBtn() {
    const btn = document.getElementById("sendBtn");
    if (btn) {
        btn.disabled = isProcessing;
        btn.innerHTML = isProcessing ? '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>' : '发送 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13"/><path d="M22 2L15 22L11 13L2 9L22 2z"/></svg>';
    }
}

// === Report Rendering ===
let currentTab = "overview";

function renderReport(outputs) {
    const container = document.getElementById("resultsContainer");
    const welcome = document.getElementById("welcomeScreen");
    if (welcome) welcome.style.display = "none";

    container.innerHTML = `
        <div class="report-container">
            ${renderTabs()}
            <div id="reportContent" class="report-content">
                ${renderOverviewTab(outputs)}
            </div>
        </div>
    `;
}

function renderTabs() {
    return `
        <div class="report-tabs">
            <button class="report-tab active" onclick="switchTab('overview')">📋 行程总览</button>
            <button class="report-tab" onclick="switchTab('cost')">💰 费用明细</button>
            <button class="report-tab" onclick="switchTab('packing')">🎒 行李清单</button>
            <button class="report-tab" onclick="switchTab('info')">📍 实用信息</button>
        </div>
    `;
}

function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll(".report-tab").forEach(el => el.classList.remove("active"));
    document.querySelectorAll(".report-tab")[["overview","cost","packing","info"].indexOf(tab)].classList.add("active");
    const content = document.getElementById("reportContent");
    content.innerHTML = tab === "overview" ? renderOverviewTab(agentResults) :
                        tab === "cost" ? renderCostTab(agentResults) :
                        tab === "packing" ? renderPackingTab(agentResults) :
                        renderInfoTab(agentResults);
}

function renderOverviewTab(o) {
    const dest = o.destination || {};
    const itin = o.itinerary || {};
    const visa = o.visa || {};
    const days = itin.days || 5;
    const destName = dest.destination || itin.destination || "目的地";
    const itineraryList = itin.itinerary || [];

    return `
        <div class="report-card">
            <div class="report-card-title">
                ✈️ ${destName} ${days}日旅行方案
                <span class="badge badge-primary">完整方案</span>
            </div>
            <div class="report-section">
                <p style="color: var(--text-secondary); line-height: 1.6;">${dest.description || ""}</p>
            </div>
            ${dest.best_season ? `
            <div class="report-section">
                <h4>最佳旅行季节</h4>
                <p style="font-size:0.9rem;">${dest.best_season}</p>
            </div>` : ""}
            ${dest.cuisine ? `
            <div class="report-section">
                <h4>🍜 推荐美食</h4>
                <div class="tag-list">${dest.cuisine.map(c => `<span class="tag">${c}</span>`).join("")}</div>
            </div>` : ""}
        </div>

        <div class="report-card">
            <div class="report-card-title">📋 每日行程</div>
            <div class="daily-itinerary">
                ${itineraryList.length > 0 ? itineraryList.map(d => `
                    <div class="day-card">
                        <div class="day-header">📅 第 ${d.day} 天 · ${d.title || ""}</div>
                        <div class="day-body">
                            ${(d.activities || []).map(a => `
                                <div class="activity-item">
                                    <span class="activity-time">${a.time || ""}</span>
                                    <span class="activity-desc"><strong>${a.activity || ""}</strong>${a.description ? " — " + a.description : ""}</span>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `).join("") : '<p style="color:var(--text-muted)">行程数据加载中...</p>'}
            </div>
        </div>

        ${visa.status ? `
        <div class="report-card">
            <div class="report-card-title">🛂 签证信息</div>
            <div class="report-section">
                <p><strong>状态:</strong> ${visa.status}${visa.visa_type ? " · " + visa.visa_type : ""}</p>
                ${visa.processing_days ? `<p><strong>办理时间:</strong> ${visa.processing_days}</p>` : ""}
                ${visa.fee ? `<p><strong>费用:</strong> ${visa.fee}</p>` : ""}
                ${visa.notes ? `<p style="margin-top:8px;color:var(--text-secondary);font-size:0.85rem;">💡 ${visa.notes}</p>` : ""}
            </div>
        </div>` : ""}
    `;
}

function renderCostTab(o) {
    const booking = o.booking || {};
    const dest = o.destination || {};
    const flights = booking.flights || [];
    const hotels = booking.hotels || [];

    return `
        <div class="report-card">
            <div class="report-card-title">✈️ 航班推荐 <span class="badge badge-success">比价结果</span></div>
            ${flights.length > 0 ? `
            <table class="flight-table">
                <tr><th>航空公司</th><th>航班号</th><th>时间</th><th>价格</th></tr>
                ${flights.map(f => `<tr><td>${f.airline}</td><td>${f.flight}</td><td>${f.departure}-${f.arrival}</td><td class="price-highlight">¥${f.price}</td></tr>`).join("")}
            </table>` : '<p style="color:var(--text-muted)">暂无航班数据</p>'}
        </div>
        <div class="report-card">
            <div class="report-card-title">🏨 酒店推荐</div>
            ${hotels.length > 0 ? `
            <table class="hotel-table">
                <tr><th>酒店</th><th>评分</th><th>位置</th><th>价格/晚</th></tr>
                ${hotels.map(h => `<tr><td>${h.name}${"★".repeat(h.stars||3)}</td><td>${h.rating}</td><td>${h.location}</td><td class="price-highlight">¥${h.price_per_night}</td></tr>`).join("")}
            </table>` : '<p style="color:var(--text-muted)">暂无酒店数据</p>'}
        </div>
    `;
}

function renderPackingTab(o) {
    const packing = o.packing || {};
    const categories = [
        {key:"essentials", label:"📄 必备证件", items: packing.essentials || []},
        {key:"clothing", label:"👔 衣物", items: packing.clothing || []},
        {key:"electronics", label:"📱 电子产品", items: packing.electronics || []},
        {key:"health", label:"💊 健康防护", items: packing.health || []},
        {key:"other", label:"🎒 其他", items: packing.other || []},
    ];

    return `
        <div class="report-card">
            <div class="report-card-title">🎒 行李清单</div>
            ${packing.weather_tip ? `<p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">🌤 ${packing.weather_tip}</p>` : ""}
            <div class="packing-grid">
                ${categories.filter(c => c.items.length > 0).map(c => `
                    <div class="packing-category">
                        <h4>${c.label}</h4>
                        ${c.items.map(item => `<div class="packing-item">${item}</div>`).join("")}
                    </div>
                `).join("")}
            </div>
        </div>
    `;
}

function renderInfoTab(o) {
    const local = o.local || {};
    const dest = o.destination || {};
    return `
        <div class="report-card">
            <div class="report-card-title">📍 实用信息</div>
            <div class="report-section">
                <h4>基本信息</h4>
                <p style="font-size:0.9rem;line-height:1.6;">
                    ${local.country ? `🌏 国家: ${local.country}<br>` : ""}
                    ${local.language ? `🗣 语言: ${local.language}<br>` : ""}
                    ${local.currency ? `💵 货币: ${local.currency}<br>` : ""}
                    ${local.timezone ? `🕐 时区: ${local.timezone}<br>` : ""}
                    ${local.exchange_rate ? `💱 汇率: ${local.exchange_rate}` : ""}
                </p>
            </div>
            ${dest.tips && dest.tips.length > 0 ? `
            <div class="report-section">
                <h4>💡 当地小贴士</h4>
                <ul style="font-size:0.85rem;line-height:1.6;padding-left:16px;color:var(--text-secondary);">
                    ${dest.tips.map(t => `<li style="margin-bottom:4px;">${t}</li>`).join("")}
                </ul>
            </div>` : ""}
            ${local.emergency ? `
            <div class="report-section">
                <h4>🆘 紧急联系方式</h4>
                <p style="font-size:0.9rem;line-height:1.6;">
                    报警: ${local.emergency.police || "110"}<br>
                    急救: ${local.emergency.ambulance || "120"}<br>
                    使馆: ${local.emergency.embassy || "请查询当地使领馆"}
                </p>
            </div>` : ""}
        </div>
    `;
}

// === Input Auto-resize ===
function autoResize(el) {
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
}

// === Example Suggestions ===
function useExample(text) {
    document.getElementById("chatInput").value = text;
    sendMessage();
}

// === Init ===
document.addEventListener("DOMContentLoaded", function() {
    initTheme();
    initWorkflow();

    // Enter to send
    document.getElementById("chatInput").addEventListener("keydown", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
