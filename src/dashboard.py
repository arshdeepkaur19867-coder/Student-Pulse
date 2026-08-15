"""
Student-Pulse — Student Academic Intelligence & Risk Monitoring
=================================================================
A Streamlit dashboard that analyzes student academic data, flags
at-risk students using a precomputed rule-based risk score (0-8),
and gives personalized, easy-to-read recommendations.

Data source: data/students_with_risk.csv
Run with:    streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG  (must be the very first Streamlit command)
# ============================================================

st.set_page_config(
    page_title="Student Pulse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# COLOR SYSTEM  (single source of truth for the whole app)
# ============================================================

COLORS = {
    "bg_top": "#EEF2FF",
    "bg_bottom": "#F8FAFC",
    "primary": "#4F46E5",       # indigo — main brand color
    "primary_dark": "#3730A3",
    "secondary": "#0EA5E9",     # sky blue — accents / secondary actions
    "text_main": "#1E1B4B",
    "text_muted": "#64748B",
    "card_bg": "#FFFFFF",
    "border": "#E2E8F0",
    "low": "#10B981",           # green  = safe
    "medium": "#F59E0B",        # amber  = caution
    "high": "#EF4444",          # red    = attention needed
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}

RISK_META = {
    "LOW": {"color": COLORS["low"], "icon": "🟢", "label": "Low Risk",
            "desc": "On track. Keep up the good habits."},
    "MEDIUM": {"color": COLORS["medium"], "icon": "🟡", "label": "Medium Risk",
               "desc": "A few areas need attention before they become a problem."},
    "HIGH": {"color": COLORS["high"], "icon": "🔴", "label": "High Risk",
             "desc": "Immediate support recommended across multiple areas."},
}

# ============================================================
# GLOBAL CSS
# ============================================================

def inject_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: linear-gradient(180deg, {COLORS['bg_top']} 0%, {COLORS['bg_bottom']} 55%);
        }}

        h1, h2, h3 {{
            font-family: 'Poppins', sans-serif !important;
            color: {COLORS['text_main']};
        }}

        /* ---------- Hero ---------- */
        .hero-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 800;
            font-size: 3rem;
            background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }}
        .hero-sub {{
            font-size: 1.1rem;
            color: {COLORS['text_muted']};
            font-weight: 500;
            margin-top: -6px;
        }}
        .hero-desc {{
            color: {COLORS['text_muted']};
            font-size: 0.98rem;
            max-width: 780px;
            line-height: 1.5;
        }}

        /* ---------- Metric / KPI cards ---------- */
        .metric-card {{
            background: {COLORS['card_bg']};
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 2px 10px rgba(79,70,229,0.06);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            animation: fadeIn 0.5s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 24px rgba(79,70,229,0.15);
        }}
        .metric-label {{
            color: {COLORS['text_muted']};
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .metric-value {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.9rem;
            font-weight: 700;
            color: {COLORS['text_main']};
            margin-top: 2px;
        }}
        .metric-icon {{ font-size: 1.6rem; }}

        /* ---------- Section header ---------- */
        .section-header {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 1.5rem;
            color: {COLORS['text_main']};
            border-left: 5px solid {COLORS['primary']};
            padding-left: 12px;
            margin: 18px 0 10px 0;
        }}

        /* ---------- Risk badge ---------- */
        .risk-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 999px;
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            color: white;
        }}

        /* ---------- Progress bars ---------- */
        .bar-label {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            font-weight: 600;
            color: {COLORS['text_main']};
            margin-bottom: 3px;
        }}
        .bar-track {{
            background: #E2E8F0;
            border-radius: 999px;
            height: 12px;
            width: 100%;
            overflow: hidden;
            margin-bottom: 14px;
        }}
        .bar-fill {{
            height: 100%;
            border-radius: 999px;
            transition: width 0.6s ease;
        }}

        /* ---------- Recommendation / warning cards ---------- */
        .rec-card {{
            background: {COLORS['card_bg']};
            border-left: 5px solid {COLORS['secondary']};
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(15,23,42,0.05);
            animation: fadeIn 0.5s ease;
        }}
        .rec-title {{
            font-weight: 700;
            color: {COLORS['text_main']};
            margin-bottom: 4px;
        }}
        .rec-text {{
            color: {COLORS['text_muted']};
            font-size: 0.92rem;
        }}
        .warn-card {{
            border-left: 5px solid {COLORS['warning']};
        }}
        .ok-card {{
            border-left: 5px solid {COLORS['success']};
        }}

        /* ---------- Quality check pill ---------- */
        .quality-pill {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: {COLORS['card_bg']};
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 8px;
            border: 1px solid {COLORS['border']};
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 100%);
        }}
        section[data-testid="stSidebar"] * {{
            color: #F1F5F9 !important;
        }}
        div[data-testid="stSidebarUserContent"] .stRadio > label {{
            font-weight: 600;
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


DATA_PATH = "data/students_with_risk.csv"
df = load_data(DATA_PATH)

# ============================================================
# REUSABLE COMPONENTS
# ============================================================

def get_risk_style(risk_level: str) -> dict:
    """Return color / icon / description for a given risk level."""
    return RISK_META.get(risk_level, RISK_META["LOW"])


def create_metric_card(col, label, value, icon="📊"):
    """Render a single KPI metric inside a styled card."""
    col.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def render_bar(label, value, max_value=100, unit="", color=COLORS["primary"]):
    """Render a custom HTML progress bar (e.g. Attendance: 86%)."""
    pct = 0 if max_value == 0 else max(0, min(100, (value / max_value) * 100))
    display_val = f"{value:.1f}{unit}" if isinstance(value, float) else f"{value}{unit}"
    st.markdown(f"""
        <div class="bar-label"><span>{label}</span><span>{display_val}</span></div>
        <div class="bar-track">
            <div class="bar-fill" style="width:{pct}%; background:{color};"></div>
        </div>
    """, unsafe_allow_html=True)


def render_risk_segments(score, max_score=8, color=COLORS["primary"]):
    """Render a segmented block indicator like ████░░░░ for the risk score."""
    filled = "█" * int(score)
    empty = "░" * (max_score - int(score))
    st.markdown(f"""
        <div style="font-size:1.6rem; letter-spacing:2px; color:{color};">
            {filled}<span style="color:#CBD5E1;">{empty}</span>
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# SECTION 1 — OVERVIEW
# ============================================================

def display_overview(data: pd.DataFrame):
    st.markdown('<div class="hero-title">🎓 Student Pulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Student Academic Intelligence &amp; Risk Monitoring</div>',
                unsafe_allow_html=True)
    st.markdown("""
        <p class="hero-desc">Student Pulse analyzes study habits, attendance, quiz performance and
        assignment completion for every student to flag academic risk early and turn raw numbers
        into clear, actionable recommendations.</p>
    """, unsafe_allow_html=True)
    st.write("")

    total_students = len(data)
    avg_score = data["final_score"].mean()
    avg_study_hours = data["study_hours"].mean()
    high_risk = int((data["risk_level"] == "HIGH").sum())
    medium_risk = int((data["risk_level"] == "MEDIUM").sum())
    low_risk = int((data["risk_level"] == "LOW").sum())

    row1 = st.columns(3)
    create_metric_card(row1[0], "Total Students", f"{total_students:,}", "👥")
    create_metric_card(row1[1], "Average Final Score", f"{avg_score:.1f}", "📈")
    create_metric_card(row1[2], "Average Study Hours", f"{avg_study_hours:.1f} hrs", "⏱️")

    row2 = st.columns(3)
    create_metric_card(row2[0], "High Risk Students", f"{high_risk:,}", "🔴")
    create_metric_card(row2[1], "Medium Risk Students", f"{medium_risk:,}", "🟡")
    create_metric_card(row2[2], "Low Risk Students", f"{low_risk:,}", "🟢")

    st.markdown('<div class="section-header">Risk Distribution</div>', unsafe_allow_html=True)
    risk_counts = data["risk_level"].value_counts().reindex(["LOW", "MEDIUM", "HIGH"]).fillna(0)
    fig = px.bar(
        x=risk_counts.index, y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map={"LOW": COLORS["low"], "MEDIUM": COLORS["medium"], "HIGH": COLORS["high"]},
        labels={"x": "Risk Level", "y": "Number of Students"},
        title="Students by Risk Level",
    )
    fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# SECTION 2 — STUDENT PROFILE
# ============================================================

def display_student_profile(data: pd.DataFrame):
    st.markdown('<div class="section-header">👤 Student Profile</div>', unsafe_allow_html=True)

    student_id = st.selectbox("Select Student", data["student_id"].tolist(), key="profile_select")
    student = data[data["student_id"] == student_id].iloc[0]
    st.session_state["selected_student_id"] = student_id

    st.write("")
    col1, col2, col3 = st.columns(3)
    create_metric_card(col1, "Final Score", f"{student['final_score']:.0f}", "🏆")
    create_metric_card(col2, "DSA Problems Solved", f"{int(student['dsa_problems'])}", "🧩")
    create_metric_card(col3, "Exam Days Remaining", f"{int(student['exam_days_remaining'])}", "📅")

    st.write("")
    st.markdown("##### Academic Indicators")
    b1, b2 = st.columns(2)
    with b1:
        render_bar("Attendance", float(student["attendance"]), 100, "%", COLORS["secondary"])
        render_bar("Quiz Average", float(student["quiz_average"]), 100, "%", COLORS["primary"])
        render_bar("Assignment Completion", float(student["assignment_completion"]), 100, "%", COLORS["low"])
    with b2:
        study_max = max(10.0, float(data["study_hours"].max()))
        sleep_max = max(12.0, float(data["sleep_hours"].max()))
        phone_max = max(10.0, float(data["phone_usage"].max()))
        render_bar("Study Hours / Day", float(student["study_hours"]), study_max, " hrs", COLORS["primary"])
        render_bar("Sleep Hours / Day", float(student["sleep_hours"]), sleep_max, " hrs", COLORS["secondary"])
        render_bar("Phone Usage / Day", float(student["phone_usage"]), phone_max, " hrs", COLORS["medium"])

    return student


# ============================================================
# SECTION 3 — RISK ASSESSMENT + RECOMMENDATIONS
# ============================================================

def display_risk_analysis(student: pd.Series):
    st.markdown('<div class="section-header">⚠️ Risk Assessment</div>', unsafe_allow_html=True)

    risk_level = student["risk_level"]
    risk_score = int(student["risk_score"])
    style = get_risk_style(risk_level)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Risk Level — {student['student_id']}</div>
                <span class="risk-badge" style="background:{style['color']}">
                    {style['icon']} {style['label']}
                </span>
                <p style="color:{COLORS['text_muted']}; font-size:0.88rem; margin-top:10px;">{style['desc']}</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="bar-label"><span>Risk Score</span><span>{risk_score} / 8</span></div>""",
                     unsafe_allow_html=True)
        render_risk_segments(risk_score, 8, style["color"])

    st.write("")
    st.markdown("##### ⚠️ Areas Needing Attention")

    issues = []
    if student["quiz_average"] < 70:
        issues.append(("Quiz Performance", f"Currently at {student['quiz_average']:.0f}%, below the 70% target."))
    if student["assignment_completion"] < 70:
        issues.append(("Assignment Completion", f"Currently at {student['assignment_completion']:.0f}%, below the 70% target."))
    if student["study_hours"] < 2:
        issues.append(("Study Hours", f"Only {student['study_hours']} hrs/day, below the recommended 2 hrs."))
    if student["attendance"] < 75:
        issues.append(("Attendance", f"Currently at {student['attendance']:.0f}%, below the 75% target."))

    if issues:
        for title, detail in issues:
            st.markdown(f"""
                <div class="rec-card warn-card">
                    <div class="rec-title">🔶 {title}</div>
                    <div class="rec-text">{detail}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="rec-card ok-card">
                <div class="rec-title">✅ No major areas needing attention</div>
                <div class="rec-text">This student is meeting all core academic benchmarks.</div>
            </div>
        """, unsafe_allow_html=True)

    display_recommendations(student)


def display_recommendations(student: pd.Series):
    st.markdown("##### 💡 Personalized Recommendations")

    recs = []
    if student["quiz_average"] < 70:
        recs.append(("💡 Quiz Performance", "Spend more time preparing for quizzes and revise weak topics."))
    if student["assignment_completion"] < 70:
        recs.append(("📚 Assignments", "Complete more assignments and submit them on time."))
    if student["study_hours"] < 2:
        recs.append(("⏱️ Study Time", "Increase daily study time gradually, aiming for at least 2 hours."))
    if student["attendance"] < 75:
        recs.append(("🎯 Attendance", "Try to improve attendance above 75% to stay on track."))

    if recs:
        for title, text in recs:
            st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-title">{title}</div>
                    <div class="rec-text">{text}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="rec-card ok-card">
                <div class="rec-title">🎉 Keep up the good work!</div>
                <div class="rec-text">No specific interventions needed right now.</div>
            </div>
        """, unsafe_allow_html=True)


# ============================================================
# SECTION 4 — ANALYTICS (with dynamic filters)
# ============================================================

def display_analytics(data: pd.DataFrame):
    st.markdown('<div class="section-header">📊 Analytics</div>', unsafe_allow_html=True)

    with st.expander("🔎 Filters", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            risk_filter = st.multiselect(
                "Risk Level", ["LOW", "MEDIUM", "HIGH"],
                default=["LOW", "MEDIUM", "HIGH"], key="analytics_risk_filter"
            )
            score_range = st.slider(
                "Final Score Range", 0, 100, (0, 100), key="analytics_score_range"
            )
        with f2:
            study_range = st.slider(
                "Study Hours Range", 0.0, float(max(10.0, data["study_hours"].max())),
                (0.0, float(max(10.0, data["study_hours"].max()))), step=0.5, key="analytics_study_range"
            )
            attendance_range = st.slider(
                "Attendance Range (%)", 0, 100, (0, 100), key="analytics_attendance_range"
            )

        reset = st.button("🔄 Reset Filters")
        if reset:
            for k in ["analytics_risk_filter", "analytics_score_range",
                      "analytics_study_range", "analytics_attendance_range"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    filtered = data[
        (data["risk_level"].isin(risk_filter)) &
        (data["final_score"].between(score_range[0], score_range[1])) &
        (data["study_hours"].between(study_range[0], study_range[1])) &
        (data["attendance"].between(attendance_range[0], attendance_range[1]))
    ]

    st.caption(f"**{len(filtered)}** students match the current filters (out of {len(data)}).")

    if filtered.empty:
        st.warning("No students match the selected filters. Try widening the ranges.")
        return

    chart_color_map = {"LOW": COLORS["low"], "MEDIUM": COLORS["medium"], "HIGH": COLORS["high"]}

    # 1. Final score distribution
    fig_score = px.histogram(
        filtered, x="final_score", nbins=20, color_discrete_sequence=[COLORS["primary"]],
        title="Distribution of Final Scores", labels={"final_score": "Final Score", "count": "Students"}
    )
    st.plotly_chart(fig_score, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_study = px.scatter(
            filtered, x="study_hours", y="final_score", color="risk_level",
            color_discrete_map=chart_color_map,
            hover_data=["student_id", "attendance", "quiz_average", "assignment_completion"],
            title="Study Hours vs Final Score",
            labels={"study_hours": "Study Hours", "final_score": "Final Score"},
        )
        st.plotly_chart(fig_study, use_container_width=True)

        fig_assign = px.scatter(
            filtered, x="assignment_completion", y="final_score", color="risk_level",
            color_discrete_map=chart_color_map,
            hover_data=["student_id", "attendance", "quiz_average"],
            title="Assignment Completion vs Final Score",
            labels={"assignment_completion": "Assignment Completion (%)", "final_score": "Final Score"},
        )
        st.plotly_chart(fig_assign, use_container_width=True)

    with c2:
        fig_quiz = px.scatter(
            filtered, x="quiz_average", y="final_score", color="risk_level",
            color_discrete_map=chart_color_map,
            hover_data=["student_id", "attendance", "assignment_completion"],
            title="Quiz Average vs Final Score",
            labels={"quiz_average": "Quiz Average", "final_score": "Final Score"},
        )
        st.plotly_chart(fig_quiz, use_container_width=True)

        fig_att = px.scatter(
            filtered, x="attendance", y="final_score", color="risk_level",
            color_discrete_map=chart_color_map,
            hover_data=["student_id", "quiz_average", "assignment_completion"],
            title="Attendance vs Final Score",
            labels={"attendance": "Attendance (%)", "final_score": "Final Score"},
        )
        st.plotly_chart(fig_att, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        risk_counts = filtered["risk_level"].value_counts().reindex(["LOW", "MEDIUM", "HIGH"]).fillna(0)
        fig_risk_dist = px.pie(
            names=risk_counts.index, values=risk_counts.values,
            color=risk_counts.index, color_discrete_map=chart_color_map,
            title="Risk Level Distribution", hole=0.45,
        )
        st.plotly_chart(fig_risk_dist, use_container_width=True)

    with c4:
        risk_avg_score = filtered.groupby("risk_level", as_index=False)["final_score"].mean()
        fig_risk_score = px.bar(
            risk_avg_score, x="risk_level", y="final_score", color="risk_level",
            color_discrete_map=chart_color_map,
            title="Average Final Score by Risk Level",
            labels={"risk_level": "Risk Level", "final_score": "Average Final Score"},
        )
        fig_risk_score.update_layout(showlegend=False)
        st.plotly_chart(fig_risk_score, use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        risk_avg_study = filtered.groupby("risk_level", as_index=False)["study_hours"].mean()
        fig_risk_study = px.bar(
            risk_avg_study, x="risk_level", y="study_hours", color="risk_level",
            color_discrete_map=chart_color_map,
            title="Average Study Hours by Risk Level",
            labels={"risk_level": "Risk Level", "study_hours": "Average Study Hours"},
        )
        fig_risk_study.update_layout(showlegend=False)
        st.plotly_chart(fig_risk_study, use_container_width=True)

    with c6:
        correlations = (
            filtered.corr(numeric_only=True)["final_score"]
            .drop("final_score")
            .sort_values(ascending=False)
        )
        correlation_df = correlations.reset_index()
        correlation_df.columns = ["Factor", "Correlation"]
        fig_corr = px.bar(
            correlation_df, x="Correlation", y="Factor", orientation="h",
            color="Correlation", color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            title="Correlation of Factors with Final Score",
        )
        fig_corr.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("##### 📋 Matching Students")
    st.dataframe(
        filtered[["student_id", "study_hours", "attendance", "assignment_completion",
                  "quiz_average", "final_score", "risk_level"]],
        use_container_width=True, height=300,
    )

    csv = filtered.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Students",
        data=csv, file_name="filtered_students.csv", mime="text/csv",
    )


# ============================================================
# SECTION 5 — DATA QUALITY
# ============================================================

def display_data_quality(data: pd.DataFrame):
    st.markdown('<div class="section-header">🔍 Data Quality</div>', unsafe_allow_html=True)

    total_students = len(data)
    total_columns = len(data.columns)
    missing_values = int(data.isnull().sum().sum())
    duplicate_rows = int(data.duplicated().sum())
    duplicate_ids = int(data["student_id"].duplicated().sum())

    invalid_attendance = int(((data["attendance"] < 0) | (data["attendance"] > 100)).sum())
    invalid_quiz = int(((data["quiz_average"] < 0) | (data["quiz_average"] > 100)).sum())
    invalid_assignment = int(((data["assignment_completion"] < 0) | (data["assignment_completion"] > 100)).sum())
    invalid_final_score = int(((data["final_score"] < 0) | (data["final_score"] > 100)).sum())

    total_cells = data.shape[0] * data.shape[1]
    completeness = ((total_cells - missing_values) / total_cells) * 100 if total_cells else 0

    row = st.columns(4)
    create_metric_card(row[0], "Students", f"{total_students:,}", "👥")
    create_metric_card(row[1], "Missing Values", f"{missing_values}", "❓")
    create_metric_card(row[2], "Duplicate IDs", f"{duplicate_ids}", "🆔")
    create_metric_card(row[3], "Completeness", f"{completeness:.1f}%", "✅")

    st.write("")
    st.markdown("##### Validation Checks")

    checks = [
        ("Total Columns", total_columns, None),
        ("Missing values", missing_values, 0),
        ("Duplicate rows", duplicate_rows, 0),
        ("Duplicate student IDs", duplicate_ids, 0),
        ("Invalid attendance", invalid_attendance, 0),
        ("Invalid quiz scores", invalid_quiz, 0),
        ("Invalid assignments", invalid_assignment, 0),
        ("Invalid final scores", invalid_final_score, 0),
    ]

    cq1, cq2 = st.columns(2)
    for i, (label, value, good_val) in enumerate(checks):
        target = cq1 if i % 2 == 0 else cq2
        if good_val is None:
            icon, color = "ℹ️", COLORS["text_main"]
        elif value == good_val:
            icon, color = "✅", COLORS["success"]
        else:
            icon, color = "⚠️", COLORS["danger"]
        target.markdown(f"""
            <div class="quality-pill">
                <span>{icon} {label}</span>
                <span style="font-weight:700; color:{color};">{value}</span>
            </div>
        """, unsafe_allow_html=True)


# ============================================================
# APP ENTRY POINT
# ============================================================

def main():
    inject_css()

    with st.sidebar:
        st.markdown("### 🎓 Student Pulse")
        st.caption("Academic Intelligence & Risk Monitoring")
        st.write("")
        page = st.radio(
            "Navigate",
            ["🏠 Overview", "👤 Student Profile", "📊 Analytics", "⚠️ Risk Analysis", "🔍 Data Quality"],
            label_visibility="collapsed",
        )
        st.write("---")
        st.caption(f"Dataset: `{DATA_PATH}`")
        st.caption(f"{len(df):,} students loaded")

    if page == "🏠 Overview":
        display_overview(df)

    elif page == "👤 Student Profile":
        display_student_profile(df)

    elif page == "📊 Analytics":
        display_analytics(df)

    elif page == "⚠️ Risk Analysis":
        student_id = st.selectbox(
            "Select Student",
            df["student_id"].tolist(),
            key="risk_select",
            index=df["student_id"].tolist().index(st.session_state.get("selected_student_id", df["student_id"].iloc[0]))
            if st.session_state.get("selected_student_id") in df["student_id"].tolist() else 0,
        )
        student = df[df["student_id"] == student_id].iloc[0]
        display_risk_analysis(student)

    elif page == "🔍 Data Quality":
        display_data_quality(df)


if __name__ == "__main__":
    main()