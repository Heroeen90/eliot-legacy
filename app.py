import streamlit as st
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
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("# 💀 إرث إليوت")
    st.markdown("### Eliot's Legacy")
    st.markdown("أرشيف أدوات إليوت الخام الكامل")
    st.divider()

    # إحصائية
    total_tools = len(TOOLS)
    st.markdown(f"### 📊 إحصائيات")
    st.markdown(f"- **{total_tools}** أداة خام كاملة")
    st.markdown(f"- **{len(CATEGORIES)}** فئات رئيسية")
    st.divider()

    # قائمة الفئات مع خيار "عرض الكل"
    all_categories = list(CATEGORIES.keys())
    display_categories = ["all"] + all_categories

    selected_cat = st.radio(
        "📂 اختر الفئة",
        options=display_categories,
        format_func=lambda x: "📋 عرض الكل" if x == "all" else f"{CATEGORIES[x]['icon']} {CATEGORIES[x]['label']}",
        key="category_selector"
    )

    st.divider()
    st.caption("⚡ جميع الأدوات للأغراض التعليمية فقط")
    st.caption("🛡️ Built with Streamlit by Sabriniak")
    st.caption(f"© 2024 - {total_tools} Tools")

# ==================== المحتوى الرئيسي ====================
st.title("💀 إرث إليوت | Eliot's Legacy")
st.markdown("### الأرشيف الكامل لأدوات إليوت الخام غير المختصرة")
st.markdown("كل أداة تحتوي على: الكود الخام الكامل | أمر الاستخدام | مثال عملي | مستوى الخطورة | اللقاح")
st.divider()

# ==================== عرض الأدوات ====================
if selected_cat == "all":
    # عرض كل الأدوات مصنفة حسب الفئة
    for cat_key, cat_info in CATEGORIES.items():
        tools_in_cat = [t for t in TOOLS if t['cat'] == cat_key]

        if tools_in_cat:
            st.subheader(f"{cat_info['icon']} {cat_info['label']} ({len(tools_in_cat)} أداة)")
            st.divider()

            # عرض الأدوات في صفوف من عمودين
            cols_per_row = 2
            for i in range(0, len(tools_in_cat), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < len(tools_in_cat):
                        tool = tools_in_cat[idx]
                        with cols[j]:
                            # لون الإطار حسب الخطورة
                            risk_colors = {
                                "critical": "#ff007f",
                                "high": "#ff6600",
                                "medium": "#ffbd2e",
                                "low": "#00ffcc"
                            }
                            border_color = risk_colors.get(tool.get('risk', 'low'), "#00ffcc")

                            with st.expander(
                                f"{cat_info['icon']} {tool['name']}",
                                expanded=False
                            ):
                                # وصف الأداة
                                st.markdown(f"**{tool['desc']}**")

                                # معلومات سريعة
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.caption(f"🚨 الخطورة: **{tool.get('risk', 'N/A').upper()}**")
                                with col2:
                                    st.caption(f"📂 الفئة: {cat_info['label']}")
                                with col3:
                                    st.caption(f"💉 لقاح متوفر")

                                st.divider()

                                # الكود الخام
                                st.caption("📋 **الكود الخام الكامل:**")
                                st.code(tool['code'], language="bash", line_numbers=True)

                                # أمر الاستخدام
                                st.caption("⚡ **أمر الاستخدام:**")
                                st.code(tool['usage'], language="bash")

                                # اللقاح
                                if 'vaccine' in tool:
                                    st.info(f"💉 **اللقاح:** {tool['vaccine']}")

            st.divider()
else:
    # عرض فئة محددة
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
                        risk_colors = {
                            "critical": "#ff007f",
                            "high": "#ff6600",
                            "medium": "#ffbd2e",
                            "low": "#00ffcc"
                        }
                        border_color = risk_colors.get(tool.get('risk', 'low'), "#00ffcc")

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
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"💀 إرث إليوت v1.0")
with col2:
    st.caption(f"📊 {total_tools} أداة خام كاملة")
with col3:
    st.caption("🛡️ للأغراض التعليمية فقط")
