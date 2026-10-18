import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Finance | Smart Money",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background:
      radial-gradient(ellipse at 0% 0%, #28134d 0%, transparent 35%),
      linear-gradient(135deg, #090914 0%, #101020 55%, #17102a 100%);
    color: #f4f0ff;
}
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #151127, #0e0e1c);
    border-right: 1px solid #34254f;
}
h1, h2, h3 {color: #f4f0ff !important;}
p, label, span {color: #ded8f0;}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #211838, #17152b);
    border: 1px solid #463365;
    padding: 20px;
    border-radius: 18px;
}
div[data-testid="stMetricLabel"] {color: #bcb0d9;}
div[data-testid="stMetricValue"] {color: #d9b8ff;}
.stButton > button {
    background: linear-gradient(90deg, #8b5cf6, #c084fc);
    color: white;
    border: 0;
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
}
.stButton > button:hover {border: 1px solid #e9d5ff;}
div[data-testid="stAlert"] {border-radius: 14px;}
hr {border-color: #35264c;}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("## 💜 AI FINANCE")
st.caption("SMART MONEY • PERSONAL FINANCE INTELLIGENCE")
st.markdown(
    "<h1 style='font-size:38px;margin-bottom:0'>Қаржыңды басқар. "
    "<span style='color:#c084fc'>Болашағыңды құр.</span></h1>",
    unsafe_allow_html=True
)
st.write("Жеке бюджетіңді талда, жинағыңды жоспарла және қаржылық кеңестер ал.")

# ---------- INPUTS ----------
with st.sidebar:
    st.markdown("## ⚙️ Бюджет параметрлері")
    st.caption("Мәліметтерді өзгерткен сайын есеп қайта жасалады.")

    income = st.number_input(
        "💰 Айлық табыс (₸)", min_value=0,
        value=250000, step=10000
    )
    housing = st.number_input(
        "🏠 Тұрғын үй (₸)", min_value=0,
        value=70000, step=5000
    )
    food = st.number_input(
        "🍜 Тамақ (₸)", min_value=0,
        value=45000, step=5000
    )
    transport = st.number_input(
        "🚕 Көлік (₸)", min_value=0,
        value=20000, step=5000
    )
    other = st.number_input(
        "🛍️ Басқа шығындар (₸)", min_value=0,
        value=35000, step=5000
    )

    st.divider()
    months = st.slider("🔮 Болжам ұзақтығы", 6, 12, 12)
    growth = st.slider(
        "📈 Айлық жинақ өзгерісі (%)",
        -10, 20, 0,
        help="Жинаққа бөлетін ақшаңның ай сайын өзгеру болжамы."
    )
    st.caption("Демо жоба: нақты банк шотына қосылмаған.")

# ---------- CALCULATIONS ----------
expenses = housing + food + transport + other
balance = income - expenses
saving_rate = (balance / income * 100) if income > 0 else 0
expense_rate = (expenses / income * 100) if income > 0 else 0

# ---------- KPI ----------
a, b, c, d = st.columns(4)
a.metric("Айлық табыс", f"{income:,.0f} ₸")
b.metric("Жалпы шығын", f"{expenses:,.0f} ₸")
c.metric("Қалған ақша", f"{balance:,.0f} ₸")
d.metric("Жинақ үлесі", f"{saving_rate:.1f}%")

st.markdown("---")

# ---------- CHARTS ----------
left, right = st.columns([1, 1.25])

with left:
    st.subheader("📊 Шығындар құрылымы")
    if expenses > 0:
        categories = pd.DataFrame({
            "Санат": ["Тұрғын үй", "Тамақ", "Көлік", "Басқа"],
            "Сома": [housing, food, transport, other]
        })
        fig = px.pie(
            categories, names="Санат", values="Сома",
            hole=0.68,
            color_discrete_sequence=[
                "#a78bfa", "#c084fc", "#818cf8", "#f0abfc"
            ]
        )
        fig.update_traces(
            textposition="inside", textinfo="percent",
            marker=dict(line=dict(color="#171327", width=3))
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#eee6ff",
            legend=dict(orientation="h", y=-0.15),
            margin=dict(t=20, b=20, l=10, r=10),
            height=340
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Диаграмманы көру үшін шығын енгіз.")

with right:
    st.subheader("💸 Табыс пен шығын")
    compare = pd.DataFrame({
        "Көрсеткіш": ["Табыс", "Шығын", "Қалған ақша"],
        "Сома": [income, expenses, max(balance, 0)]
    })
    fig2 = px.bar(
        compare, x="Көрсеткіш", y="Сома",
        color="Көрсеткіш",
        color_discrete_sequence=["#a78bfa", "#f0abfc", "#34d399"],
        text_auto=".2s"
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#eee6ff",
        showlegend=False,
        margin=dict(t=20, b=20, l=5, r=5),
        height=340,
        yaxis_title="Сома (₸)",
        xaxis_title=""
    )
    fig2.update_yaxes(gridcolor="#302744", zeroline=False)
    st.plotly_chart(fig2, use_container_width=True)

# ---------- AI ADVISOR ----------
st.markdown("---")
st.subheader("🤖 AI қаржылық кеңесші")
st.caption("Ережелерге негізделген автоматты талдау • Деректерді енгізген сайын жаңарады")

if balance < 0:
    st.error(
        f"Бюджет тапшылығы: {abs(balance):,.0f} ₸. "
        "Алдымен міндетті емес шығындарды қысқарту мүмкіндігін қарастыр."
    )
elif income == 0:
    st.warning("Талдау жасау үшін айлық табысты енгіз.")
elif saving_rate < 10:
    st.warning(
        f"Жинақ үлесі {saving_rate:.1f}%. "
        "Мақсат ретінде табыстың 10%-ын жинауға бөлуді қарастыр."
    )
else:
    st.success(
        f"Жақсы! Қазіргі есеп бойынша табыстың {saving_rate:.1f}%-ы қалады."
    )

if income > 0:
    if housing / income > 0.35:
        st.info("🏠 Тұрғын үй шығыны табыстың 35%-ынан жоғары. Бұл санатты тексер.")
    if food / income > 0.25:
        st.info("🍜 Тамақ шығыны табыстың 25%-ынан жоғары. Жоспар құру пайдалы болуы мүмкін.")
    if other / income > 0.20:
        st.info("🛍️ Басқа шығындар жоғары. Сатып алуларды санат бойынша бақыла.")
    st.write(
        f"**Ұсынылатын бастапқы жинақ мақсаты:** "
        f"{income * 0.10:,.0f} ₸ / ай (табыстың 10%-ы)."
    )

# ---------- FORECAST ----------
st.markdown("---")
st.subheader(f"🔮 Келесі {months} айға жинақ болжамы")
st.caption(
    "Бұл сценарийлік есеп: бастапқы айлық жинақ тұрақты деп алынады, "
    "ал төмендегі параметр оны ай сайын өзгертіп отырады. "
    "Нақты табысқа кепілдік бермейді."
)

monthly_saving = max(0, balance)
monthly_change = growth / 100

savings = []
total = 0.0
current_saving = monthly_saving

for m in range(1, months + 1):
    total += current_saving
    savings.append({
        "Ай": m,
        "Айлық жинақ": round(current_saving, 2),
        "Жиналған ақша": round(total, 2)
    })
    current_saving = max(0, current_saving * (1 + monthly_change))

forecast = pd.DataFrame(savings)

f1, f2 = st.columns(2)
f1.metric("Болжамды жинақ", f"{total:,.0f} ₸")
f2.metric("Мерзім соңындағы айлық жинақ", f"{current_saving / (1 + monthly_change):,.0f} ₸" if months > 0 and (1 + monthly_change) != 0 else "—")

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=forecast["Ай"],
    y=forecast["Жиналған ақша"],
    mode="lines+markers",
    name="Жинақ",
    line=dict(color="#c084fc", width=4),
    fill="tozeroy",
    fillcolor="rgba(168,85,247,0.14)"
))
fig3.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#eee6ff",
    xaxis_title="Ай",
    yaxis_title="Жиналған ақша (₸)",
    margin=dict(t=20, b=20, l=10, r=10),
    height=370
)
fig3.update_yaxes(gridcolor="#302744", zeroline=False)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("📋 Болжам кестесін көру"):
    st.dataframe(
        forecast.style.format({
            "Айлық жинақ": "{:,.0f} ₸",
            "Жиналған ақша": "{:,.0f} ₸"
        }),
        use_container_width=True,
        hide_index=True
    )

csv = forecast.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Болжамды CSV форматында жүктеу",
    data=csv,
    file_name="ai_finance_forecast.csv",
    mime="text/csv"
)

# ---------- FOOTER ----------
st.markdown("---")
st.caption(
    "💜 AI Finance • Оқу жобасы. Кеңестер автоматты ережелерге негізделген; "
    "бұл банк немесе лицензияланған қаржы кеңесшісі емес."
)
