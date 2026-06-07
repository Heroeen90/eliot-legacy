import streamlit as st
import subprocess
import os
from tools_data import TOOLS, CATEGORIES

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
/* إخفاء علامة Streamlit والشريط الجانبي */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarCollapsedControl"] {display: none !important;}
[data-testid="stAppViewContainer"] > .main {padding-left: 0 !important; padding-right: 0 !important;}
[data-testid="stAppViewContainer"] > .main > .block-container {padding: 10px 20px !important; max-width: 100% !important;}

/* ========== الألسنة المخصصة ========== */
.custom-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 6px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.06);
    justify-content: center;
}

.custom-tab {
    padding: 10px 18px;
    border-radius: 8px;
    background: transparent;
    border: none;
    color: #888;
    cursor: pointer;
    font-size: 0.85rem;
    font-family: inherit;
    font-weight: 500;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.custom-tab:hover {
    background: rgba(255,255,255,0.04);
    color: #ccc;
}

.custom-tab.active {
    background: linear-gradient(135deg, rgba(0,255,204,0.12), rgba(124,77,255,0.12));
    color: #00ffcc;
    font-weight: 700;
    box-shadow: 0 0 15px rgba(0,255,204,0.1);
}

/* ========== بطاقات الفئات ========== */
.category-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 10px;
    margin-bottom: 20px;
}

.category-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.category-card:hover {
    border-color: rgba(0,255,204,0.3);
    background: rgba(0,255,204,0.04);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.category-card.active {
    border-color: #00ffcc;
    background: rgba(0,255,204,0.08);
    box-shadow: 0 0 20px rgba(0,255,204,0.15);
}

.category-card .cat-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.category-card .cat-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #ddd;
    margin-bottom: 4px;
}

.category-card .cat-count {
    font-size: 0.7rem;
    color: #666;
}

/* ========== إطارات الأدوات ========== */
.stExpander {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
}
.stExpander:hover {
    border-color: rgba(255,0,127,0.3) !important;
}

/* ========== الطرفية ========== */
.terminal-output {
    background-color: #0a0a0a;
    color: #00ffcc;
    font-family: 'Courier New', monospace;
    padding: 15px;
    border-radius: 8px;
    min-height: 200px;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
    border: 1px solid #00ffcc33;
}

/* ========== المساعد الذكي ========== */
.ai-response {
    background: linear-gradient(135deg, rgba(0,255,204,0.05), rgba(124,77,255,0.05));
    border: 1px solid rgba(0,255,204,0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}

/* ========== شريط التمرير ========== */
::-webkit-scrollbar {width: 6px;}
::-webkit-scrollbar-track {background: transparent;}
::-webkit-scrollbar-thumb {background: rgba(255,255,255,0.08); border-radius: 3px;}

/* ========== للهواتف ========== */
@media (max-width: 768px) {
    .custom-tab {padding: 8px 12px; font-size: 0.75rem;}
    .category-cards {grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));}
}
</style>
""", unsafe_allow_html=True)

# ==================== دالة تنفيذ الأوامر ====================
def execute_command(command):
    try:
        allowed_commands = [
            'nmap', 'ping', 'whois', 'dig', 'curl', 'traceroute',
            'hydra', 'john', 'hashcat', 'sqlmap', 'nikto', 'dirb',
            'gobuster', 'theHarvester', 'sherlock', 'holehe',
            'subfinder', 'exiftool', 'cewl', 'crunch', 'msfconsole',
            'python', 'python3', 'echo', 'ls', 'pwd', 'cat', 'head',
            'tail', 'grep', 'awk', 'sed', 'sort', 'uniq', 'wc',
            'ifconfig', 'ip', 'netstat', 'ss', 'ps', 'top',
            'wget', 'git', 'chmod', 'find', 'locate',
            'which', 'whereis', 'file', 'strings', 'xxd', 'hexdump',
            'tar', 'gzip', 'unzip', 'zip', 'bzip2',
            'netcat', 'nc', 'ssh', 'scp', 'rsync', 'ftp',
            'masscan', 'dnsenum', 'dnsrecon', 'fierce',
            'wafw00f', 'whatweb', 'wpscan', 'searchsploit',
            'msfvenom', 'setoolkit', 'beef-xss',
            'bash', 'sh', 'zsh', 'python2', 'ruby', 'perl', 'php', 'node',
            'apt', 'apt-get', 'yum', 'dnf', 'pacman', 'brew',
            'pip', 'pip3', 'gem', 'npm', 'yarn',
            'systemctl', 'service', 'df', 'du', 'free', 'uptime',
            'uname', 'hostname', 'openssl', 'gnupg', 'gpg',
            'base64', 'md5sum', 'sha256sum', 'cut', 'tr', 'tee',
            'ssh-keygen', 'tcpdump', 'tshark',
        ]

        base_cmd = command.strip().split()[0] if command.strip() else ""
        if base_cmd not in allowed_commands:
            return f"❌ الأمر '{base_cmd}' غير مسموح به في هذه البيئة."

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            timeout=60, cwd=os.path.expanduser("~")
        )

        output = ""
        if result.stdout: output += result.stdout
        if result.stderr: output += "\n[STDERR]\n" + result.stderr
        if not output: output = "(تم التنفيذ بنجاح - لا يوجد مخرجات)"
        return output

    except subprocess.TimeoutExpired: return "⏱️ انتهت مهلة الأمر (60 ثانية)"
    except FileNotFoundError: return f"❌ الأمر غير مثبت على هذا الخادم"
    except Exception as e: return f"❌ خطأ: {str(e)}"

# ==================== المساعد الذكي ====================
def ai_analyze_query(query):
    query_lower = query.lower()
    keyword_map = {
        "منافذ": ["nmap", "masscan"], "بورت": ["nmap", "masscan"],
        "فحص": ["nmap", "masscan", "nikto"], "شبكة": ["nmap", "arp_sweep"],
        "مسح": ["nmap", "masscan"], "smb": ["smb_version", "eternal_blue", "psexec"],
        "eternal": ["eternal_blue"], "wannacry": ["eternal_blue"],
        "rdp": ["bluekeep"], "bluekeep": ["bluekeep"],
        "log4j": ["log4shell"], "log4shell": ["log4shell"],
        "sql": ["sqli_tester", "sqlmap"], "حقن": ["sqli_tester", "nosql_injection", "ssti_detector"],
        "xss": ["xss_scanner"], "jwt": ["jwt_toolkit"],
        "nosql": ["nosql_injection"], "xxe": ["xxe_tester"],
        "lfi": ["lfi_scanner"], "ssti": ["ssti_detector"],
        "ssrf": ["ssrf_exploiter"], "csrf": ["csrf_analyzer"],
        "osint": ["theharvester", "sherlock", "holehe", "subfinder"],
        "معلومات": ["theharvester", "whois", "dig"],
        "نطاق": ["subfinder", "whois", "dig"],
        "بريد": ["holehe"], "ايميل": ["holehe"],
        "يوزر": ["sherlock"], "اسم مستخدم": ["sherlock"],
        "كلمة مرور": ["hydra", "john", "hashcat"], "تخمين": ["hydra"],
        "هاش": ["john", "hashcat"], "ssl": ["ssl_scanner"],
        "رؤوس": ["security_headers"], "كوكيز": ["cookie_analyzer"],
        "cors": ["cors_checker"], "clickjack": ["clickjacking"],
        "arp": ["arp_watchdog"], "hashdump": ["hashdump"],
        "صلاحيات": ["getsystem"], "persistence": ["persistence"],
        "keylogger": ["keylogger"], "metasploit": ["metasploit"],
        "beef": ["beef"], "هندسة اجتماعية": ["set"], "تصيد": ["set"],
    }

    matched_tools = set()
    for keyword, tools in keyword_map.items():
        if keyword in query_lower: matched_tools.update(tools)

    if not matched_tools: matched_tools = ["nmap", "metasploit", "theharvester", "hydra"]

    results = []
    for tool_id in list(matched_tools)[:10]:
        tool = next((t for t in TOOLS if t['id'] == tool_id), None)
        if tool: results.append(tool)
    return results

def generate_ai_response(query, matched_tools):
    if not matched_tools: return "عذراً، لم أجد أدوات مناسبة لاستفسارك."
    cat_names = {"scanner":"الفحص","exploit":"الاستغلال","osint":"OSINT","crack":"كسر كلمات المرور","defense":"الدفاع","post":"ما بعد الاختراق","framework":"المنصات المتكاملة"}
    response = f"### 🧠 تحليل المساعد الذكي\n\nبناءً على استفسارك **'{query}'**، إليك {len(matched_tools)} أدوات مقترحة:\n\n"
    for i, tool in enumerate(matched_tools[:5], 1):
        cat_label = cat_names.get(tool['cat'], tool['cat'])
        response += f"**{i}. {tool['name']}** ({cat_label})\n   📝 {tool['desc']}\n   ⚡ `{tool['usage']}`\n\n"
    response += "---\n💡 **نصيحة:** استعرض الأدوات من قسم 'عرض الكل' لعرض الكود الكامل."
    return response

# ==================== عرض الأدوات ====================
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
                        c1, c2, c3 = st.columns(3)
                        with c1: st.caption(f"🚨 **{tool.get('risk','N/A').upper()}**")
                        with c2: st.caption(f"📂 {cat_info['label']}")
                        with c3: st.caption("💉 لقاح متوفر")
                        st.divider()
                        st.caption("📋 **الكود الخام الكامل:**")
                        st.code(tool['code'], language="bash", line_numbers=True)
                        st.caption("⚡ **أمر الاستخدام:**")
                        st.code(tool['usage'], language="bash")
                        if 'vaccine' in tool: st.info(f"💉 **اللقاح:** {tool['vaccine']}")

# ==================== المتغيرات ====================
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "all"
if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = "scanner"

total_tools = len(TOOLS)

# ==================== العنوان الرئيسي ====================
st.markdown("""
<div style="text-align:center;margin-bottom:10px">
    <h1 style="color:#00ffcc;font-size:2.2rem;margin:0">💀 إرث إليوت</h1>
    <p style="color:#666;font-size:0.9rem">Eliot's Legacy — الأرشيف الكامل للأدوات الخام</p>
</div>
""", unsafe_allow_html=True)

# ==================== الألسنة المخصصة ====================
tabs = [
    {"key": "all", "label": "📋 عرض الكل", "icon": ""},
    {"key": "categories", "label": "📂 الفئات", "icon": ""},
    {"key": "ai", "label": "🧠 المساعد الذكي", "icon": ""},
    {"key": "terminal", "label": "💻 الطرفية الحية", "icon": ""},
]

tab_html = '<div class="custom-tabs">'
for t in tabs:
    active = "active" if st.session_state.selected_tab == t["key"] else ""
    tab_html += f'<a href="?tab={t["key"]}" class="custom-tab {active}">{t["label"]}</a>'
tab_html += '</div>'
st.markdown(tab_html, unsafe_allow_html=True)

# ==================== قراءة الاختيار من الـ URL ====================
query_params = st.query_params
if "tab" in query_params:
    st.session_state.selected_tab = query_params["tab"]
if "cat" in query_params:
    st.session_state.selected_cat = query_params["cat"]

selected_tab = st.session_state.selected_tab
selected_cat = st.session_state.selected_cat

# ==================== عرض المحتوى حسب التبويب ====================

# ---------- عرض الكل ----------
if selected_tab == "all":
    for cat_key, cat_info in CATEGORIES.items():
        tools_in_cat = [t for t in TOOLS if t['cat'] == cat_key]
        if tools_in_cat:
            st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)} أداة)")
            st.divider()
            render_tools(tools_in_cat, cat_info)
            st.divider()

# ---------- الفئات ----------
elif selected_tab == "categories":
    st.subheader("📂 اختر فئة لعرض أدواتها")
    
    # بطاقات الفئات
    cat_html = '<div class="category-cards">'
    for cat_key, cat_info in CATEGORIES.items():
        tools_count = len([t for t in TOOLS if t['cat'] == cat_key])
        active = "active" if selected_cat == cat_key else ""
        cat_html += f'''
        <a href="?tab=categories&cat={cat_key}" class="category-card {active}" style="text-decoration:none">
            <div class="cat-icon">{cat_info['icon']}</div>
            <div class="cat-label">{cat_info['label']}</div>
            <div class="cat-count">{tools_count} أداة</div>
        </a>'''
    cat_html += '</div>'
    st.markdown(cat_html, unsafe_allow_html=True)
    
    st.divider()
    
    # عرض أدوات الفئة المختارة
    cat_info = CATEGORIES.get(selected_cat, {"icon": "🔧", "label": selected_cat})
    tools_in_cat = [t for t in TOOLS if t['cat'] == selected_cat]
    if tools_in_cat:
        st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)} أداة)")
        render_tools(tools_in_cat, cat_info)
    else:
        st.info("لا توجد أدوات في هذه الفئة.")

# ---------- المساعد الذكي ----------
elif selected_tab == "ai":
    st.subheader("🧠 المساعد الذكي | AI Assistant")
    st.markdown("اسأل أي سؤال عن أدوات إليوت وسأقترح لك الأنسب.")

    user_query = st.text_input(
        "💬 ماذا تريد أن تفعل؟",
        placeholder="مثال: أريد فحص منافذ شبكة، كيفية اختراق SMB...",
        key="ai_query"
    )

    c1, c2 = st.columns([1, 5])
    with c1: analyze_btn = st.button("🧠 حلل", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑 مسح", use_container_width=True):
            if "ai_history" in st.session_state: st.session_state.ai_history = []

    if "ai_history" not in st.session_state: st.session_state.ai_history = []

    if analyze_btn and user_query:
        with st.spinner("🧠 جاري تحليل استفسارك..."):
            matched = ai_analyze_query(user_query)
            resp = generate_ai_response(user_query, matched)
            st.session_state.ai_history.append({"query": user_query, "response": resp, "tools": matched})

    if st.session_state.ai_history:
        for item in reversed(st.session_state.ai_history):
            st.markdown(f'<div class="ai-response">{item["response"]}</div>', unsafe_allow_html=True)
            if item["tools"]:
                st.markdown("#### 🔧 الأدوات المقترحة:")
                cols = st.columns(min(len(item["tools"]), 3))
                for i, tool in enumerate(item["tools"][:9]):
                    with cols[i % 3]:
                        c_info = CATEGORIES.get(tool['cat'], {"icon": "🔧", "label": "أداة"})
                        with st.expander(f"{c_info['icon']} {tool['name']}", expanded=False):
                            st.markdown(f"**{tool['desc']}**")
                            st.code(tool['code'], language="bash", line_numbers=True)
                            st.caption(f"⚡ `{tool['usage']}`")
                            if 'vaccine' in tool: st.info(f"💉 {tool['vaccine']}")
            st.divider()
    else:
        st.info("👋 مرحباً! اكتب ما تريد فعله وسأقترح الأدوات المناسبة.")
        st.markdown("- أريد فحص منافذ شبكة\n- كيف أخترق SMB؟\n- أداة لجمع المعلومات عن نطاق\n- تخمين كلمات المرور SSH")

# ---------- الطرفية الحية ----------
elif selected_tab == "terminal":
    st.subheader("💻 الطرفية الحية | Live Terminal")
    st.markdown("نفذ أوامر حقيقية مباشرة من هنا.")

    command = st.text_input("اكتب أمراً:", placeholder="مثال: nmap -F scanme.nmap.org", key="term_cmd")
    c1, c2 = st.columns([1, 5])
    with c1: exec_btn = st.button("▶ نفذ", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑 مسح", use_container_width=True):
            if "term_hist" in st.session_state: st.session_state.term_hist = ""

    if "term_hist" not in st.session_state: st.session_state.term_hist = ""

    if exec_btn and command:
        with st.spinner("⏳ جاري التنفيذ..."):
            output = execute_command(command)
            st.session_state.term_hist += f"$ {command}\n{output}\n{'─'*50}\n"

    if st.session_state.term_hist:
        st.markdown("### 📟 المخرجات:")
        st.markdown(f'<div class="terminal-output">{st.session_state.term_hist}</div>', unsafe_allow_html=True)
    else:
        st.info("💡 اكتب أمراً في الحقل أعلاه واضغط 'نفذ'.")

# ==================== التذييل ====================
st.divider()
st.caption(f"💀 إرث إليوت v4.0 | 📊 {total_tools} أداة | 🧠 مساعد ذكي | 💻 طرفية حية | 🛡️ تعليمي فقط")
