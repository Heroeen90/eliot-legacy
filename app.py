import streamlit as st
import subprocess
import os
import json
import time
from datetime import datetime
from tools_data import TOOLS, CATEGORIES
from lab_scenarios import LAB_SCENARIOS
from report_generator import generate_report_html, generate_report_json, generate_summary

# ==================== إعداد الصفحة ====================
st.set_page_config(
    page_title="إرث إليوت | Eliot's Legacy",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CSS مخصص ====================
st.markdown("""
<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarCollapsedControl"] {display: none !important;}
[data-testid="stAppViewContainer"] > .main {padding-left: 0 !important; padding-right: 0 !important;}
[data-testid="stAppViewContainer"] > .main > .block-container {padding: 10px 20px !important; max-width: 100% !important;}

/* الألسنة */
.custom-tabs {display: flex; flex-wrap: wrap; gap: 4px; background: rgba(255,255,255,0.02); border-radius: 12px; padding: 6px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.06); justify-content: center;}
.custom-tab {padding: 8px 14px; border-radius: 8px; background: transparent; border: none; color: #888; cursor: pointer; font-size: 0.82rem; font-family: inherit; font-weight: 500; transition: all 0.2s; white-space: nowrap; text-decoration: none; display: inline-block;}
.custom-tab:hover {background: rgba(255,255,255,0.04); color: #ccc;}
.custom-tab.active {background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(124,77,255,0.12)); color: #00ffcc; font-weight: 700;}

/* البطاقات */
.category-cards {display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px;}
.category-card {background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; text-align: center; cursor: pointer; transition: all 0.2s; text-decoration: none; display: block;}
.category-card:hover {border-color: rgba(0,255,204,0.3); background: rgba(0,255,204,0.04); transform: translateY(-2px);}
.category-card.active {border-color: #00ffcc; background: rgba(0,255,204,0.08);}
.category-card .cat-icon {font-size: 1.8rem; margin-bottom: 6px;}
.category-card .cat-label {font-size: 0.8rem; font-weight: 700; color: #ddd;}
.category-card .cat-count {font-size: 0.65rem; color: #666;}

/* لوحة القيادة */
.dashboard-grid {display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px;}
.dash-card {background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 18px; text-align: center;}
.dash-card .dash-num {font-size: 2.2rem; font-weight: 900; color: #00ffcc;}
.dash-card .dash-label {font-size: 0.78rem; color: #888; margin-top: 4px;}

/* إطارات */
.stExpander {border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 10px !important; margin-bottom: 10px !important;}
.terminal-output {background-color: #0a0a0a; color: #00ffcc; font-family: 'Courier New', monospace; padding: 15px; border-radius: 8px; min-height: 200px; max-height: 400px; overflow-y: auto; white-space: pre-wrap; border: 1px solid #00ffcc33;}
.ai-response {background: linear-gradient(135deg, rgba(0,255,204,0.05), rgba(124,77,255,0.05)); border: 1px solid rgba(0,255,204,0.2); border-radius: 12px; padding: 20px; margin: 10px 0;}

/* سيناريوهات المختبر */
.lab-card {background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 18px; margin-bottom: 12px; transition: all 0.2s;}
.lab-card:hover {border-color: rgba(255,0,127,0.3); background: rgba(255,0,127,0.03);}
.lab-card .diff-badge {display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700;}
.diff-مبتدئ {background: rgba(0,255,0,0.1); color: #00ff00;}
.diff-متوسط {background: rgba(255,165,0,0.1); color: #ffa500;}
.diff-متقدم {background: rgba(255,0,0,0.1); color: #ff0000;}

/* نتيجة التحدي */
.flag-box {background: rgba(0,255,0,0.1); border: 2px solid #00ff00; border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0; animation: pulse 2s infinite;}
@keyframes pulse {0%,100% {box-shadow: 0 0 20px rgba(0,255,0,0.2);} 50% {box-shadow: 0 0 40px rgba(0,255,0,0.5);}}
.flag-box .flag {font-size: 1.5rem; font-weight: 900; color: #00ff00; font-family: monospace;}

/* الماسح الشامل */
.scan-progress {margin: 10px 0;}
.scan-progress .phase {padding: 8px 12px; margin: 4px 0; border-radius: 6px; font-size: 0.8rem;}
.phase-complete {background: rgba(0,255,0,0.08); color: #00ff00; border-left: 3px solid #00ff00;}
.phase-running {background: rgba(0,255,204,0.08); color: #00ffcc; border-left: 3px solid #00ffcc;}
.phase-pending {background: rgba(255,255,255,0.02); color: #666; border-left: 3px solid #333;}

::-webkit-scrollbar {width: 6px;} ::-webkit-scrollbar-track {background: transparent;} ::-webkit-scrollbar-thumb {background: rgba(255,255,255,0.08); border-radius: 3px;}
@media (max-width: 768px) {.custom-tab {padding: 6px 10px; font-size: 0.7rem;} .dashboard-grid {grid-template-columns: repeat(2, 1fr);}}
</style>
""", unsafe_allow_html=True)

# ==================== دوال المساعدة ====================
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        output = result.stdout
        if result.stderr: output += "\n" + result.stderr
        return output if output else "(تم التنفيذ - لا مخرجات)"
    except subprocess.TimeoutExpired: return "⏱️ انتهت مهلة الأمر"
    except Exception as e: return f"❌ خطأ: {str(e)}"

def ai_analyze_query(query):
    query_lower = query.lower()
    keyword_map = {
        "منافذ":["nmap","masscan"],"فحص":["nmap","masscan","nikto"],"شبكة":["nmap","arp_sweep"],
        "smb":["smb_version","eternal_blue","psexec"],"eternal":["eternal_blue"],
        "rdp":["bluekeep"],"log4j":["log4shell"],"sql":["sqli_tester","sqlmap"],
        "xss":["xss_scanner"],"jwt":["jwt_toolkit"],"nosql":["nosql_injection"],
        "xxe":["xxe_tester"],"lfi":["lfi_scanner"],"ssti":["ssti_detector"],
        "osint":["theharvester","sherlock","holehe","subfinder"],
        "بريد":["holehe"],"يوزر":["sherlock"],"كلمة مرور":["hydra","john","hashcat"],
        "ssl":["ssl_scanner"],"رؤوس":["security_headers"],"كوكيز":["cookie_analyzer"],
        "metasploit":["metasploit"],"beef":["beef"],"تصيد":["set"],
    }
    matched = set()
    for kw, tools in keyword_map.items():
        if kw in query_lower: matched.update(tools)
    if not matched: matched = ["nmap","metasploit","theharvester","hydra"]
    results = []
    for tid in list(matched)[:10]:
        tool = next((t for t in TOOLS if t['id']==tid), None)
        if tool: results.append(tool)
    return results

def render_tools(tools_in_cat, cat_info):
    if not tools_in_cat: return
    cols_per_row = 2
    for i in range(0, len(tools_in_cat), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(tools_in_cat):
                tool = tools_in_cat[idx]
                with cols[j]:
                    with st.expander(f"{cat_info['icon']} {tool['name']}", expanded=False):
                        st.markdown(f"**{tool['desc']}**")
                        c1,c2,c3=st.columns(3)
                        c1.caption(f"🚨 **{tool.get('risk','N/A').upper()}**")
                        c2.caption(f"📂 {cat_info['label']}")
                        c3.caption("💉 لقاح متوفر")
                        st.divider()
                        st.caption("📋 **الكود الخام:**")
                        st.code(tool['code'], language="bash", line_numbers=True)
                        st.caption("⚡ **أمر الاستخدام:**")
                        st.code(tool['usage'], language="bash")
                        if 'vaccine' in tool: st.info(f"💉 {tool['vaccine']}")

# ==================== المتغيرات ====================
if "selected_tab" not in st.session_state: st.session_state.selected_tab = "dashboard"
if "selected_cat" not in st.session_state: st.session_state.selected_cat = "scanner"
if "terminal_hist" not in st.session_state: st.session_state.terminal_hist = ""
if "ai_history" not in st.session_state: st.session_state.ai_history = []
if "scan_history" not in st.session_state: st.session_state.scan_history = []
if "lab_progress" not in st.session_state: st.session_state.lab_progress = {}
if "score" not in st.session_state: st.session_state.score = 0

total_tools = len(TOOLS)
query_params = st.query_params
if "tab" in query_params: st.session_state.selected_tab = query_params["tab"]
if "cat" in query_params: st.session_state.selected_cat = query_params["cat"]
selected_tab = st.session_state.selected_tab
selected_cat = st.session_state.selected_cat

# ==================== العنوان ====================
st.markdown("""
<div style="text-align:center;margin-bottom:10px">
    <h1 style="color:#00ffcc;font-size:2rem;margin:0">💀 إرث إليوت</h1>
    <p style="color:#666;font-size:0.8rem">Eliot's Legacy — منصة الاختراق المتكاملة</p>
</div>
""", unsafe_allow_html=True)

# ==================== الألسنة ====================
tabs = [
    {"key":"dashboard","label":"📊 لوحة القيادة"},
    {"key":"all","label":"📋 عرض الكل"},
    {"key":"categories","label":"📂 الفئات"},
    {"key":"scanner","label":"🔍 الماسح الشامل"},
    {"key":"lab","label":"🧪 المختبر الحي"},
    {"key":"ai","label":"🧠 المساعد الذكي"},
    {"key":"terminal","label":"💻 الطرفية"},
]
tab_html = '<div class="custom-tabs">'
for t in tabs:
    active = "active" if selected_tab == t["key"] else ""
    tab_html += f'<a href="?tab={t["key"]}" class="custom-tab {active}">{t["label"]}</a>'
tab_html += '</div>'
st.markdown(tab_html, unsafe_allow_html=True)

# ==================== المحتوى ====================

# --- لوحة القيادة ---
if selected_tab == "dashboard":
    st.subheader("📊 لوحة القيادة")
    
    # إحصائيات
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-card"><div class="dash-num">{total_tools}</div><div class="dash-label">أداة خام</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-card"><div class="dash-num">{len(CATEGORIES)}</div><div class="dash-label">فئة</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-card"><div class="dash-num">{len(LAB_SCENARIOS)}</div><div class="dash-label">سيناريو</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-card"><div class="dash-num">{st.session_state.score}</div><div class="dash-label">نقطة</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-card"><div class="dash-num">{len(st.session_state.scan_history)}</div><div class="dash-label">عملية</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-card"><div class="dash-num" style="color:#ff007f">v6.0</div><div class="dash-label">الإصدار</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # آخر العمليات
    st.subheader("📜 آخر العمليات")
    if st.session_state.scan_history:
        for item in reversed(st.session_state.scan_history[-10:]):
            st.caption(f"🔍 {item.get('type','')} | 🎯 {item.get('target','')} | ⏱️ {item.get('time','')}")
    else:
        st.info("لا توجد عمليات سابقة. ابدأ بفحص هدف!")
    
    # أزرار سريعة
    st.subheader("⚡ إجراءات سريعة")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("🔍 فتح الماسح الشامل", use_container_width=True):
            st.session_state.selected_tab = "scanner"
            st.rerun()
    with c2:
        if st.button("🧪 فتح المختبر الحي", use_container_width=True):
            st.session_state.selected_tab = "lab"
            st.rerun()
    with c3:
        if st.button("🧠 فتح المساعد الذكي", use_container_width=True):
            st.session_state.selected_tab = "ai"
            st.rerun()

# --- عرض الكل ---
elif selected_tab == "all":
    st.subheader("📋 جميع الأدوات")
    for cat_key, cat_info in CATEGORIES.items():
        tools_in_cat = [t for t in TOOLS if t['cat'] == cat_key]
        if tools_in_cat:
            st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)})")
            st.divider()
            render_tools(tools_in_cat, cat_info)
            st.divider()

# --- الفئات ---
elif selected_tab == "categories":
    st.subheader("📂 الفئات")
    cat_html = '<div class="category-cards">'
    for cat_key, cat_info in CATEGORIES.items():
        tools_count = len([t for t in TOOLS if t['cat'] == cat_key])
        active = "active" if selected_cat == cat_key else ""
        cat_html += f'<a href="?tab=categories&cat={cat_key}" class="category-card {active}" style="text-decoration:none"><div class="cat-icon">{cat_info["icon"]}</div><div class="cat-label">{cat_info["label"]}</div><div class="cat-count">{tools_count} أداة</div></a>'
    cat_html += '</div>'
    st.markdown(cat_html, unsafe_allow_html=True)
    st.divider()
    cat_info = CATEGORIES.get(selected_cat, {"icon":"🔧","label":selected_cat})
    tools_in_cat = [t for t in TOOLS if t['cat']==selected_cat]
    if tools_in_cat:
        st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)})")
        render_tools(tools_in_cat, cat_info)

# --- الماسح الشامل ---
elif selected_tab == "scanner":
    st.subheader("🔍 الماسح الشامل | All-in-One Scanner")
    st.markdown("أدخل هدفاً واحداً وسيقوم الماسح بتشغيل جميع الأدوات تلقائياً")
    
    target = st.text_input("🎯 الهدف:", placeholder="مثال: scanme.nmap.org أو 192.168.1.1")
    
    c1,c2 = st.columns(2)
    with c1:
        scan_type = st.selectbox("نوع الفحص:", ["سريع (3 دقائق)", "متوسط (8 دقائق)", "شامل (15 دقيقة)"])
    with c2:
        if st.button("🚀 بدء الفحص الشامل", type="primary", use_container_width=True) and target:
            st.session_state.terminal_hist = ""
            phases = [
                ("🔍 فحص المنافذ", f"nmap -F {target}"),
                ("🌐 فحص HTTP", f"curl -sI http://{target}" if not target.startswith('http') else f"curl -sI {target}"),
                ("🔒 فحص SSL", f"nmap --script ssl-enum-ciphers -p 443 {target}"),
                ("📂 فحص المسارات", f"dirb {target} /usr/share/wordlists/dirb/common.txt" if not target.startswith('http') else f"dirb {target}"),
                ("📧 جمع المعلومات", f"whois {target}"),
            ]
            
            all_findings = []
            for phase_name, cmd in phases:
                st.markdown(f'<div class="scan-progress"><div class="phase phase-running">⏳ {phase_name}...</div></div>', unsafe_allow_html=True)
                output = execute_command(cmd)
                st.session_state.terminal_hist += f"$ {cmd}\n{output}\n{'─'*50}\n"
                
                # تحليل بسيط للنتائج
                if "open" in output:
                    all_findings.append({"risk":"medium","name":"منفذ مفتوح","description":f"تم اكتشاف منافذ مفتوحة","fix":"أغلق المنافذ غير المستخدمة"})
                if "200 OK" in output:
                    all_findings.append({"risk":"low","name":"خادم HTTP نشط","description":"الموقع يستجيب","fix":"تأكد من تحديث الخادم"})
            
            st.session_state.scan_history.append({"type":"الماسح الشامل","target":target,"time":datetime.now().strftime('%H:%M'),"findings":len(all_findings)})
            
            st.success(f"✅ اكتمل الفحص! تم اكتشاف {len(all_findings)} نتيجة.")
            
            # عرض التقرير
            if all_findings:
                summary = generate_summary(all_findings)
                st.markdown(f"### 📊 ملخص النتائج")
                cols = st.columns(4)
                cols[0].metric("🔴 حرج", summary['critical'])
                cols[1].metric("🟠 عالي", summary['high'])
                cols[2].metric("🟡 متوسط", summary['medium'])
                cols[3].metric("🟢 منخفض", summary['low'])
                
                # تقرير HTML
                report_html = generate_report_html("الماسح الشامل", target, all_findings, ["nmap","curl","dirb","whois"], "5 دقائق")
                st.download_button("📥 تحميل التقرير (HTML)", report_html, f"report_{target}_{datetime.now().strftime('%Y%m%d')}.html", "text/html")
    
    # عرض سجل الطرفية
    if st.session_state.terminal_hist:
        with st.expander("📟 سجل الطرفية", expanded=False):
            st.markdown(f'<div class="terminal-output">{st.session_state.terminal_hist}</div>', unsafe_allow_html=True)

# --- المختبر الحي ---
elif selected_tab == "lab":
    st.subheader("🧪 المختبر الحي | Live Lab")
    st.markdown("اختر سيناريو للتدرب على اختبار الاختراق بشكل عملي")
    
    for scenario in LAB_SCENARIOS:
        with st.expander(f"{scenario['name']} — {scenario['difficulty']} — ⏱️ {scenario['duration']}", expanded=False):
            st.markdown(f"**{scenario['desc']}**")
            st.markdown(f"🎯 **الهدف:** `{scenario['target']}`")
            
            # أدوات مقترحة
            st.caption("🔧 الأدوات المطلوبة:")
            tools_html = " ".join([f"`{t}`" for t in scenario['tools_needed']])
            st.markdown(tools_html)
            
            # الخطوات
            st.caption("📝 الخطوات:")
            for step in scenario['steps']:
                st.markdown(f"- {step}")
            
            # تلميحات
            with st.expander("💡 تلميحات"):
                for hint in scenario['hints']:
                    st.markdown(f"- {hint}")
            
            # خانة إدخال الفلاق
            st.markdown("---")
            st.caption("🏁 أدخل كلمة العلم (flag) التي وجدتها بعد إكمال التحدي:")
            flag_input = st.text_input(f"العلم:", placeholder="FLAG{...}", key=f"flag_{scenario['id']}")
            
            if flag_input:
                if flag_input == scenario['flag']:
                    st.balloons()
                    st.markdown(f'<div class="flag-box"><div class="flag">🎉 تهانينا!</div><p>لقد أكملت تحدي "{scenario["name"]}" بنجاح!</p><p>العلم: {scenario["flag"]}</p></div>', unsafe_allow_html=True)
                    st.session_state.score += 100
                else:
                    st.error("❌ العلم غير صحيح. حاول مرة أخرى!")

# --- المساعد الذكي ---
elif selected_tab == "ai":
    st.subheader("🧠 المساعد الذكي | Advanced AI")
    user_query = st.text_input("💬 ماذا تريد أن تفعل؟", placeholder="مثال: أريد فحص شبكة كاملة، أو كيفية اختراق ووردبريس...")
    c1,c2=st.columns([1,5])
    with c1: analyze_btn=st.button("🧠 حلل",type="primary",use_container_width=True)
    with c2:
        if st.button("🗑 مسح",use_container_width=True): st.session_state.ai_history=[]
    if analyze_btn and user_query:
        with st.spinner("🧠 جاري التحليل..."):
            matched=ai_analyze_query(user_query)
            resp=f"### 🧠 تحليل استفسارك\n\nبناءً على **'{user_query}'**، إليك {len(matched)} أدوات:\n\n"
            for i,t in enumerate(matched[:5],1):
                resp+=f"**{i}. {t['name']}**\n   📝 {t['desc']}\n   ⚡ `{t['usage']}`\n\n"
            st.session_state.ai_history.append({"query":user_query,"response":resp,"tools":matched})
    if st.session_state.ai_history:
        for item in reversed(st.session_state.ai_history):
            st.markdown(f'<div class="ai-response">{item["response"]}</div>',unsafe_allow_html=True)
            if item["tools"]:
                st.markdown("#### 🔧 الأدوات المقترحة:")
                cols=st.columns(min(len(item["tools"]),3))
                for i,t in enumerate(item["tools"][:9]):
                    with cols[i%3]:
                        ci=CATEGORIES.get(t['cat'],{"icon":"🔧","label":"أداة"})
                        with st.expander(f"{ci['icon']} {t['name']}",expanded=False):
                            st.markdown(f"**{t['desc']}**")
                            st.code(t['code'],language="bash",line_numbers=True)
                            if 'vaccine' in t: st.info(f"💉 {t['vaccine']}")
            st.divider()
    else:
        st.info("👋 اكتب ما تريد فعله وسأقترح الأدوات المناسبة.")

# --- الطرفية ---
elif selected_tab == "terminal":
    st.subheader("💻 الطرفية الحية")
    cmd=st.text_input("اكتب أمراً:",placeholder="nmap -F scanme.nmap.org")
    c1,c2=st.columns([1,5])
    with c1: exec_btn=st.button("▶ نفذ",type="primary",use_container_width=True)
    with c2:
        if st.button("🗑 مسح",use_container_width=True): st.session_state.terminal_hist=""
    if exec_btn and cmd:
        with st.spinner("⏳..."):
            output=execute_command(cmd)
            st.session_state.terminal_hist+=f"$ {cmd}\n{output}\n{'─'*50}\n"
            st.session_state.scan_history.append({"type":"طرفية","target":cmd.split()[-1] if cmd.split() else "N/A","time":datetime.now().strftime('%H:%M')})
    if st.session_state.terminal_hist:
        st.markdown("### 📟 المخرجات:")
        st.markdown(f'<div class="terminal-output">{st.session_state.terminal_hist}</div>',unsafe_allow_html=True)

# ==================== التذييل ====================
st.divider()
st.caption(f"💀 إرث إليوت v6.0 | 📊 {total_tools} أداة | 🧪 {len(LAB_SCENARIOS)} سيناريو | 🏆 {st.session_state.score} نقطة | 🛡️ تعليمي فقط")
