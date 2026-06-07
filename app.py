import streamlit as st
import subprocess
import os
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
div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
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
.terminal-input {
    background-color: #0a0a0a;
    color: #00ffcc;
    border: 1px solid #00ffcc33;
    font-family: 'Courier New', monospace;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==================== دالة تنفيذ الأوامر ====================
def execute_command(command):
    """تنفيذ أمر في الطرفية وإرجاع الناتج"""
    try:
        # قائمة بالأوامر المسموح بها (للأمان)
        allowed_commands = [
            'nmap', 'ping', 'whois', 'dig', 'curl', 'traceroute',
            'hydra', 'john', 'hashcat', 'sqlmap', 'nikto', 'dirb',
            'gobuster', 'theHarvester', 'sherlock', 'holehe',
            'subfinder', 'exiftool', 'cewl', 'crunch', 'msfconsole',
            'python', 'python3', 'echo', 'ls', 'pwd', 'cat', 'head',
            'tail', 'grep', 'awk', 'sed', 'sort', 'uniq', 'wc',
            'ifconfig', 'ip', 'netstat', 'ss', 'ps', 'top', 'htop',
            'wget', 'git', 'chmod', 'chown', 'find', 'locate',
            'which', 'whereis', 'file', 'strings', 'xxd', 'hexdump',
            'tar', 'gzip', 'unzip', 'zip', 'bzip2', 'arpspoof',
            'tcpdump', 'aircrack-ng', 'reaver', 'bettercap', 'responder',
            'netcat', 'nc', 'socat', 'proxychains', 'tor', 'ssh',
            'scp', 'rsync', 'ftp', 'sftp', 'telnet', 'rdesktop',
            'masscan', 'zmap', 'dnsenum', 'dnsrecon', 'fierce',
            'wafw00f', 'whatweb', 'wpscan', 'joomscan', 'droopescan',
            'searchsploit', 'exploitdb', 'msfvenom', 'msfdb',
            'setoolkit', 'beef-xss', 'empire', 'covenant',
            'powershell', 'cmd', 'bash', 'sh', 'zsh',
            'python2', 'ruby', 'perl', 'php', 'node', 'go',
            'gcc', 'g++', 'make', 'cmake', 'autoconf',
            'docker', 'kubectl', 'ansible', 'puppet', 'terraform',
            'aws', 'gcloud', 'az', 'ibmcloud',
            'apt', 'apt-get', 'yum', 'dnf', 'pacman', 'brew',
            'pip', 'pip3', 'gem', 'cpan', 'npm', 'yarn',
            'systemctl', 'service', 'journalctl',
            'mount', 'umount', 'df', 'du', 'free', 'uptime',
            'uname', 'hostname', 'hostnamectl', 'timedatectl',
            'useradd', 'usermod', 'userdel', 'groupadd', 'passwd',
            'iptables', 'ufw', 'firewalld', 'nft',
            'openssl', 'gnupg', 'gpg', 'base64', 'md5sum', 'sha256sum',
            'cut', 'tr', 'tee', 'xargs', 'nohup', 'screen', 'tmux',
            'ssh-keygen', 'ssh-copy-id', 'ssh-agent', 'ssh-add',
            'tcpdump', 'tshark', 'wireshark', 'ettercap', 'dsniff',
            'sslstrip', 'sslsplit', 'mitmproxy', 'burpsuite',
            'zaproxy', 'skipfish', 'arachni', 'w3af', 'ironwasp',
            'vega', 'acunetix', 'netsparker', 'appspider',
            'nessus', 'openvas', 'qualys', 'rapid7', 'tenable',
        ]

        # التحقق من أن الأمر مسموح
        base_cmd = command.strip().split()[0] if command.strip() else ""
        if base_cmd not in allowed_commands:
            return f"❌ الأمر '{base_cmd}' غير مسموح به في هذه البيئة.\n💡 استخدم الأدوات المتاحة في المنصة."

        # تنفيذ الأمر
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.path.expanduser("~")
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

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("# 💀 إرث إليوت")
    st.markdown("### Eliot's Legacy")
    st.markdown("أرشيف + مختبر حي")
    st.divider()

    # إحصائية
    total_tools = len(TOOLS)
    st.markdown(f"### 📊 إحصائيات")
    st.markdown(f"- **{total_tools}** أداة خام كاملة")
    st.markdown(f"- **{len(CATEGORIES)}** فئات رئيسية")
    st.divider()

    # قائمة الفئات مع خيار "عرض الكل"
    all_categories = list(CATEGORIES.keys())
    display_categories = ["all"] + all_categories + ["terminal"]

    selected_cat = st.radio(
        "📂 اختر الفئة",
        options=display_categories,
        format_func=lambda x: (
            "📋 عرض الكل" if x == "all"
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
st.markdown("### الأرشيف الكامل + الطرفية الحية")
st.divider()

# ==================== الطرفية الحية ====================
if selected_cat == "terminal":
    st.subheader("💻 الطرفية الحية | Live Terminal")
    st.markdown("نفذ أوامر حقيقية مباشرة من هنا. **لأغراض التعليم فقط.**")

    # حقل الإدخال
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

    # تهيئة سجل الطرفية
    if "terminal_history" not in st.session_state:
        st.session_state.terminal_history = ""

    # تنفيذ الأمر
    if execute_btn and command:
        with st.spinner("⏳ جاري التنفيذ..."):
            output = execute_command(command)
            st.session_state.terminal_history += f"$ {command}\n{output}\n{'─'*50}\n"

    # عرض سجل الطرفية
    if st.session_state.terminal_history:
        st.markdown("### 📟 المخرجات:")
        st.markdown(
            f'<div class="terminal-output">{st.session_state.terminal_history}</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("💡 اكتب أمراً في الحقل أعلاه واضغط 'نفذ'. مثال: `nmap -F scanme.nmap.org`")

    st.divider()
    st.caption("⚠️ الأوامر المتاحة محدودة لأسباب أمنية. بعض الأدوات تحتاج تثبيت مسبق على الخادم.")

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
                            with st.expander(
                                f"{cat_info['icon']} {tool['name']}",
                                expanded=False
                            ):
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
                        with st.expander(
                            f"{cat_info['icon']} {tool['name']}",
                            expanded=False
                        ):
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
    st.caption(f"💀 إرث إليوت v2.0")
with col2:
    st.caption(f"📊 {total_tools} أداة")
with col3:
    st.caption("💻 + طرفية حية")
with col4:
    st.caption("🛡️ تعليمي فقط")
