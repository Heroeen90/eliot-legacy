import streamlit as st
from tools_data import TOOLS, CATEGORIES

st.set_page_config(page_title="إرث إليوت", page_icon="💀", layout="wide")

# إخفاء علامة Streamlit
hide = """<style>#MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}</style>"""
st.markdown(hide, unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/hacker.png", width=80)
    st.markdown("# 💀 إرث إليوت")
    st.markdown("### Eliot's Legacy")
    st.divider()
    st.markdown(f"**{len(TOOLS)}** أداة خام كاملة")
    
    selected_cat = st.radio(
        "📂 اختر الفئة",
        options=list(CATEGORIES.keys()),
        format_func=lambda x: f"{CATEGORIES[x]['icon']} {CATEGORIES[x]['label']}"
    )
    
    st.divider()
    st.caption("جميع الأدوات للأغراض التعليمية فقط")
    st.caption("Built with Streamlit by Sabriniak")

# المحتوى الرئيسي
st.title("💀 إرث إليوت | Eliot's Legacy")
st.markdown("### الأرشيف الكامل لأدوات إليوت الخام")
st.markdown("كل أداة تحتوي على الكود الكامل غير المختصر وأمر الاستخدام ومثال عملي")
st.divider()

# عرض أدوات الفئة المختارة
cat = CATEGORIES[selected_cat]
st.subheader(f"{cat['icon']} {cat['label']}")

tools_in_cat = [t for t in TOOLS if t['cat'] == selected_cat]

if tools_in_cat:
    # عرض كعدد
    cols_per_row = 2
    for i in range(0, len(tools_in_cat), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(tools_in_cat):
                tool = tools_in_cat[idx]
                with cols[j]:
                    with st.expander(f"{cat['icon']} {tool['name']}", expanded=False):
                        st.markdown(f"**{tool['desc']}**")
                        st.divider()
                        st.caption("📋 الكود الخام:")
                        st.code(tool['code'], language="bash", line_numbers=True)
                        st.caption("⚡ أمر الاستخدام:")
                        st.code(tool['usage'], language="bash")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"🚨 الخطورة: {tool['risk'].upper()}")
                        with col2:
                            st.caption(f"💉 اللقاح: {tool['vaccine']}")
else:
    st.info("لا توجد أدوات في هذه الفئة")

# تذييل
st.divider()
st.caption(f"💀 إرث إليوت | {len(TOOLS)} أداة | جميع الحقوق محفوظة © 2024")
