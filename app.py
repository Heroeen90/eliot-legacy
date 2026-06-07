import streamlit as st
import subprocess
import os
import re
from tools_data import TOOLS, CATEGORIES

# ==================== إعداد الصفحة ====================
st.set_page_config(
    page_title="إرث إليوت | Eliot's Legacy",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إخفاء علامة Streamlit المائية
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stExpander {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
}
.stExpander:hover {
    border-color: rgba(255, 0, 127, 0.3) !important;
}
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
.ai-response {
    background: linear-gradient(135deg, rgba(0,255,204,0.05), rgba(124,77,255,0.05));
    border: 1px solid rgba(0,255,204,0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}
.suggestion-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.2s;
}
.suggestion-card:hover {
    border-color: #00ffcc;
    background: rgba(0,255,204,0.05);
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n[STDERR]\n" + result.stderr
        if not output:
            output = "(تم التنفيذ بنجاح - لا يوجد مخرجات)"

        return output

    except subprocess.TimeoutExpired:
        return "⏱️ انتهت مهلة الأمر (60 ثانية)"
    except FileNotFoundError:
        return f"❌ الأمر '{command.split()[0]}' غير مثبت على هذا الخادم"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# ==================== المساعد الذكي ====================
def ai_analyze_query(query):
    """تحليل استفسار المستخدم واقتراح الأدوات المناسبة"""
    query_lower = query.lower()

    # قاعدة معرفية للكلمات المفتاحية
    keyword_map = {
        "منافذ": ["nmap", "masscan"],
        "بورت": ["nmap", "masscan"],
        "فحص": ["nmap", "masscan"],
        "شبكة": ["nmap", "arp_sweep"],
        "واي فاي": ["wifi_scan"],
        "wifi": ["wifi_scan"],
        "مسح": ["nmap", "masscan"],
        "smb": ["smb_version", "eternal_blue", "psexec"],
        "eternal": ["eternal_blue"],
        "wannacry": ["eternal_blue"],
        "rdp": ["bluekeep"],
        "bluekeep": ["bluekeep"],
        "log4j": ["log4shell"],
        "log4shell": ["log4shell"],
        "psexec": ["psexec"],
        "bash": ["shellshock"],
        "shellshock": ["shellshock"],
        "sql": ["sqli_tester", "sqlmap"],
        "حقن": ["sqli_tester", "nosql_injection", "ssti_detector"],
        "xss": ["xss_scanner"],
        "jwt": ["jwt_toolkit"],
        "token": ["jwt_toolkit"],
        "nosql": ["nosql_injection"],
        "mongodb": ["nosql_injection"],
        "xxe": ["xxe_tester"],
        "xml": ["xxe_tester"],
        "lfi": ["lfi_scanner"],
        "ملفات": ["lfi_scanner"],
        "ssti": ["ssti_detector"],
        "قالب": ["ssti_detector"],
        "ssrf": ["ssrf_exploiter"],
        "csrf": ["csrf_analyzer"],
        "serial": ["insecure_deserialize"],
        "تسلسل": ["insecure_deserialize"],
        "osint": ["theharvester", "sherlock", "holehe", "subfinder"],
        "معلومات": ["theharvester", "whois", "dig"],
        "نطاق": ["subfinder", "whois", "dig", "theharvester"],
        "بريد": ["holehe"],
        "ايميل": ["holehe"],
        "يوزر": ["sherlock"],
        "اسم مستخدم": ["sherlock"],
        "كلمة مرور": ["hydra", "john", "hashcat"],
        "تخمين": ["hydra"],
        "هاش": ["john", "hashcat"],
        "hash": ["john", "hashcat"],
        "تشفير": ["john", "hashcat"],
        "ssl": ["ssl_scanner"],
        "tls": ["ssl_scanner"],
        "رؤوس": ["security_headers"],
        "headers": ["security_headers"],
        "كوكيز": ["cookie_analyzer"],
        "cors": ["cors_checker"],
        "clickjack": ["clickjacking"],
        "arp": ["arp_watchdog"],
        "spoof": ["arp_watchdog"],
        "hashdump": ["hashdump"],
        "sam": ["hashdump"],
        "صلاحيات": ["getsystem"],
        "system": ["getsystem"],
        "persistence": ["persistence"],
        "باب خلفي": ["persistence"],
        "keylogger": ["keylogger"],
        "تجسس": ["keylogger"],
        "migrate": ["migrate"],
        "pivot": ["pivoting"],
        "شبكة داخلية": ["pivoting"],
        "metasploit": ["metasploit"],
        "beef": ["beef"],
        "متصفح": ["beef"],
        "هندسة اجتماعية": ["set"],
        "تصيد": ["set"],
        "empire": ["empire"],
        "powershell": ["empire"],
        "cobalt": ["cobalt_strike"],
        "toolx": ["toolx"],
    }

    # البحث عن تطابقات
    matched_tools = set()
    for keyword, tools in keyword_map.items():
        if keyword in query_lower:
            matched_tools.update(tools)

    # إذا لم نجد شيئاً، نقترح أدوات عامة
    if not matched_tools:
        matched_tools = ["nmap", "metasploit", "theharvester", "hydra"]

    # تحويل المعرفات إلى كائنات الأدوات
    results = []
    for tool_id in list(matched_tools)[:10]:  # أقصى 10 اقتراحات
        tool = next((t for t in TOOLS if t['id'] == tool_id), None)
        if tool:
            results.append(tool)

    return results

def generate_ai_response(query, matched_tools):
    """توليد رد ذكي بالعربية"""
    if not matched_tools:
        return "عذراً، لم أجد أدوات مناسبة لاستفسارك. جرب كلمات مفتاحية مثل: فحص منافذ، تخمين كلمات مرور، جمع معلومات."

    cat_names = {
        "scanner": "الفحص", "exploit": "الاستغلال", "osint": "OSINT",
        "crack": "كسر كلمات المرور", "defense": "الدفاع",
        "post": "ما بعد الاختراق", "framework": "المنصات المتكاملة"
    }

    response = f"### 🧠 تحليل المساعد الذكي\n\n"
    response += f"بناءً على استفسارك **'{query}'**، إليك {len(matched_tools)} أدوات مقترحة:\n\n"

    for i, tool in enumerate(matched_tools[:5], 1):
        cat_label = cat_names.get(tool['cat'], tool['cat'])
        response += f"**{i}. {tool['name']}** ({cat_label})\n"
        response += f"   📝 {tool['desc']}\n"
        response += f"   ⚡ `{tool['usage']}`\n\n"

    response += "---\n"
    response += "💡 **نصيحة:** اضغط على اسم الأداة في القائمة الجانبية لعرض الكود الكامل وأمر الاستخدام."

    return response

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("# 💀 إرث إليوت")
    st.markdown("### Eliot's Legacy + AI")
    st.divider()

    total_tools = len(TOOLS)
    st.markdown(f"### 📊 إحصائيات")
    st.markdown(f"- **{total_tools}** أداة خام كاملة")
    st.markdown(f"- **{len(CATEGORIES)}** فئات رئيسية")
    st.markdown(f"- **🧠 مساعد ذكي**")
    st.divider()

    all_categories = list(CATEGORIES.keys())
    display_categories = ["ai", "all"] + all_categories + ["terminal"]

    selected_cat = st.radio(
        "📂 اختر الوضع",
        options=display_categories,
        format_func=lambda x: (
            "🧠 المساعد الذكي" if x == "ai"
            else "📋 عرض الكل" if x == "all"
            else "💻 الطرفية الحية" if x == "terminal"
            else f"{CATEGORIES[x]['icon']} {CATEGORIES[x]['label']}"
        ),
        key="category_selector"
    )

    st.divider()
    st.caption("⚡ جميع الأدوات للأغراض التعليمية فقط")
    st.caption("🛡️ Built with Streamlit by Sabriniak")

# ==================== المحتوى الرئيسي ====================
st.title("💀 إرث إليوت | Eliot's Legacy")
st.markdown("### الأرشيف الكامل + المساعد الذكي + الطرفية الحية")
st.divider()

# ==================== المساعد الذكي ====================
if selected_cat == "ai":
    st.subheader("🧠 المساعد الذكي | AI Assistant")
    st.markdown("اسأل أي سؤال عن أدوات إليوت وسأقترح لك الأنسب.")

    # حقل الإدخال
    user_query = st.text_input(
        "💬 ماذا تريد أن تفعل؟",
        placeholder="مثال: أريد فحص منافذ شبكة، أو كيفية اختراق SMB، أو جمع معلومات عن نطاق...",
        key="ai_query_input"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_btn = st.button("🧠 حلل", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑 مسح", use_container_width=True):
            if "ai_history" in st.session_state:
                st.session_state.ai_history = []

    # تهيئة السجل
    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []

    # تحليل الاستفسار
    if analyze_btn and user_query:
        with st.spinner("🧠 جاري تحليل استفسارك..."):
            matched_tools = ai_analyze_query(user_query)
            response = generate_ai_response(user_query, matched_tools)
            st.session_state.ai_history.append({
                "query": user_query,
                "response": response,
                "tools": matched_tools
            })

    # عرض التاريخ
    if st.session_state.ai_history:
        for item in reversed(st.session_state.ai_history):
            st.markdown(f'<div class="ai-response">{item["response"]}</div>', unsafe_allow_html=True)

            # عرض بطاقات الأدوات المقترحة
            if item["tools"]:
                st.markdown("#### 🔧 الأدوات المقترحة:")
                cols = st.columns(min(len(item["tools"]), 3))
                for i, tool in enumerate(item["tools"][:9]):
                    with cols[i % 3]:
                        cat_info = CATEGORIES.get(tool['cat'], {"icon": "🔧", "label": "أداة"})
                        with st.expander(f"{cat_info['icon']} {tool['name']}", expanded=False):
                            st.markdown(f"**{tool['desc']}**")
                            st.code(tool['code'], language="bash", line_numbers=True)
                            st.caption(f"⚡ `{tool['usage']}`")
                            if 'vaccine' in tool:
                                st.info(f"💉 {tool['vaccine']}")

            st.divider()
    else:
        st.info("👋 مرحباً! أنا المساعد الذكي. اكتب ما تريد فعله وسأقترح عليك الأدوات المناسبة.")
        st.markdown("""
        **أمثلة على ما يمكنك سؤالي عنه:**
        - "أريد فحص منافذ شبكة"
        - "كيف أخترق SMB؟"
        - "أداة لجمع المعلومات عن نطاق"
        - "تخمين كلمات المرور SSH"
        - "فحص ثغرات XSS"
        - "استخراج الهاشات من ويندوز"
        - "كيف أصنع باباً خلفياً؟"
        """)

# ==================== الطرفية الحية ====================
elif selected_cat == "terminal":
    st.subheader("💻 الطرفية الحية | Live Terminal")
    st.markdown("نفذ أوامر حقيقية مباشرة من هنا. **لأغراض التعليم فقط.**")

    command = st.text_input(
        "اكتب أمراً:",
        placeholder="مثال: nmap -F scanme.nmap.org",
        key="terminal_input"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        execute_btn = st.button("▶ نفذ", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑 مسح", use_container_width=True):
            if "terminal_history" in st.session_state:
                st.session_state.terminal_history = ""

    if "terminal_history" not in st.session_state:
        st.session_state.terminal_history = ""

    if execute_btn and command:
        with st.spinner("⏳ جاري التنفيذ..."):
            output = execute_command(command)
            st.session_state.terminal_history += f"$ {command}\n{output}\n{'─'*50}\n"

    if st.session_state.terminal_history:
        st.markdown("### 📟 المخرجات:")
        st.markdown(
            f'<div class="terminal-output">{st.session_state.terminal_history}</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("💡 اكتب أمراً في الحقل أعلاه واضغط 'نفذ'.")

    st.divider()
    st.caption("⚠️ الأوامر المتاحة محدودة لأسباب أمنية.")

# ==================== عرض الكل ====================
elif selected_cat == "all":
    for cat_key, cat_info in CATEGORIES.items():
        tools_in_cat = [t for t in TOOLS if t['cat'] == cat_key]

        if tools_in_cat:
            st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)} أداة)")
            st.divider()

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
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.caption(f"🚨 الخطورة: **{tool.get('risk', 'N/A').upper()}**")
                                with col2:
                                    st.caption(f"📂 الفئة: {cat_info['label']}")
                                with col3:
                                    st.caption(f"💉 لقاح متوفر")
                                st.divider()
                                st.caption("📋 **الكود الخام الكامل:**")
                                st.code(tool['code'], language="bash", line_numbers=True)
                                st.caption("⚡ **أمر الاستخدام:**")
                                st.code(tool['usage'], language="bash")
                                if 'vaccine' in tool:
                                    st.info(f"💉 **اللقاح:** {tool['vaccine']}")
            st.divider()

# ==================== عرض فئة محددة ====================
else:
    cat_info = CATEGORIES[selected_cat]
    tools_in_cat = [t for t in TOOLS if t['cat'] == selected_cat]
    st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)} أداة)")
    st.divider()

    if tools_in_cat:
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
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.caption(f"🚨 الخطورة: **{tool.get('risk', 'N/A').upper()}**")
                            with col2:
                                st.caption(f"📂 الفئة: {cat_info['label']}")
                            with col3:
                                st.caption(f"💉 لقاح متوفر")
                            st.divider()
                            st.caption("📋 **الكود الخام الكامل:**")
                            st.code(tool['code'], language="bash", line_numbers=True)
                            st.caption("⚡ **أمر الاستخدام:**")
                            st.code(tool['usage'], language="bash")
                            if 'vaccine' in tool:
                                st.info(f"💉 **اللقاح:** {tool['vaccine']}")
    else:
        st.info("لا توجد أدوات في هذه الفئة حالياً.")

# ==================== التذييل ====================
st.divider()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.caption(f"💀 إرث إليوت v3.0")
with col2:
    st.caption(f"📊 {total_tools} أداة")
with col3:
    st.caption("🧠 + مساعد ذكي")
with col4:
    st.caption("🛡️ تعليمي فقط")
