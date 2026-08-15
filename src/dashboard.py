import streamlit as st
import pandas as pd
import plotly.express as px
# Load data
file = 'data/students_with_risk.csv'
df = pd.read_csv(file)

# ============================================================
# TITLE
# ============================================================

st.title("🎓 Student Pulse")
st.subheader("Student Academic Risk Monitoring")

# ============================================================
# STUDENT SELECTION
# ============================================================

student_id = st.selectbox(
    "Select Student",
    df["student_id"].tolist()
)
student = df[df["student_id"] == student_id].iloc[0]



# ============================================================
# STUDENT PROFILE
# ============================================================

st.header("Student Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Study Hours", student["study_hours"])
    st.metric("Attendance", f"{student['attendance']:.0f}%")
    st.metric("Quiz Average", student["quiz_average"])

with col2:
    st.metric(
        "Assignment Completion",
        f"{student['assignment_completion']:.0f}%"
    )
    st.metric("Phone Usage", student["phone_usage"])
    st.metric("Sleep Hours", student["sleep_hours"])

with col3:
    st.metric("DSA Problems", int(student["dsa_problems"]))
    st.metric("Final Score", int(student["final_score"]))
    st.metric(
        "Exam Days Remaining",
        int(student["exam_days_remaining"])
    )

# ============================================================
# RISK ASSESSMENT
# ============================================================

st.header(" ⚠️ Risk Assessment")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Risk Score",
        f"{int(student['risk_score'])} / 8"
    )

with col2:
    st.metric(
        "Risk Level",
        student["risk_level"]
    )

# ============================================================
# AREAS NEEDING ATTENTION
# ============================================================

st.subheader("⚠️ Areas Needing Attention")

issues = []

if student["quiz_average"] < 70:
    issues.append("Quiz performance")

if student["assignment_completion"] < 70:
    issues.append("Assignment completion")

if student["study_hours"] < 2:
    issues.append("Study hours")

if student["attendance"] < 75:
    issues.append("Attendance")

if issues:
    for issue in issues:
        st.warning(issue)
else:
    st.success("No major areas needing attention.")

# ============================================================
# RECOMMENDATIONS
# ============================================================

st.subheader("💡 Recommendations")

if student["quiz_average"] < 70:
    st.info(
        "Spend more time preparing for quizzes "
        "and revise weak topics."
    )

if student["assignment_completion"] < 70:
    st.info(
        "Complete more assignments and submit them on time."
    )

if student["study_hours"] < 2:
    st.info(
        "Increase your daily study time gradually."
    )

if student["attendance"] < 75:
    st.info(
        "Try to improve your attendance above 75%."
    )
# ============================================================
# DATA QUALITY
# ============================================================

st.header("🔍 Data Quality")

total_students = len(df)
total_columns = len(df.columns)

missing_values = df.isnull().sum().sum()
duplicate_rows = df.duplicated().sum()
duplicate_ids = df["student_id"].duplicated().sum()

invalid_attendance = (
    (df["attendance"] < 0) |
    (df["attendance"] > 100)
).sum()

invalid_quiz = (
    (df["quiz_average"] < 0) |
    (df["quiz_average"] > 100)
).sum()

invalid_assignment = (
    (df["assignment_completion"] < 0) |
    (df["assignment_completion"] > 100)
).sum()

invalid_final_score = (
    (df["final_score"] < 0) |
    (df["final_score"] > 100)
).sum()

total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isnull().sum().sum()

completeness = (
    (total_cells - missing_cells) /
    total_cells
) * 100


# Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Students", total_students)

with col2:
    st.metric("Missing Values", missing_values)

with col3:
    st.metric("Duplicate IDs", duplicate_ids)

with col4:
    st.metric("Completeness", f"{completeness:.1f}%")


st.subheader("Validation Checks")

quality_data = pd.DataFrame({
    "Check": [
        "Missing values",
        "Duplicate rows",
        "Duplicate student IDs",
        "Invalid attendance",
        "Invalid quiz scores",
        "Invalid assignments",
        "Invalid final scores"
    ],
    "Count": [
        missing_values,
        duplicate_rows,
        duplicate_ids,
        invalid_attendance,
        invalid_quiz,
        invalid_assignment,
        invalid_final_score
    ]
})

st.dataframe(
    quality_data,
    use_container_width=True
)

# Page configuration
st.set_page_config(
    page_title="Student Pulse",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 Student Pulse")
st.subheader("Student Performance Monitoring System")

# Basic statistics
total_students = len(df)
average_score = df['final_score'].mean()
average_attendance = df['attendance'].mean()
high_risk_students = len(df[df['risk_level'] == 'HIGH'])

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", total_students)

with col2:
    st.metric("Average Score", f"{average_score:.2f}")

with col3:
    st.metric("Average Attendance", f"{average_attendance:.2f}%")

with col4:
    st.metric("High Risk Students", high_risk_students)

# Risk distribution
st.subheader("Risk Distribution")

risk_counts = df['risk_level'].value_counts()

st.bar_chart(risk_counts)

# Student selection
st.subheader("Student Profile")

student_id = st.selectbox(
    "Select a Student",
    df['student_id'].tolist()
)

student = df[df['student_id'] == student_id].iloc[0]

st.write("### Student Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Student ID:**", student['student_id'])
    st.write("**Study Hours:**", student['study_hours'])
    st.write("**Attendance:**", student['attendance'])
    st.write("**Quiz Average:**", student['quiz_average'])
    st.write("**Assignment Completion:**", student['assignment_completion'])

with col2:
    st.write("**Phone Usage:**", student['phone_usage'])
    st.write("**Sleep Hours:**", student['sleep_hours'])
    st.write("**DSA Problems:**", student['dsa_problems'])
    st.write("**Final Score:**", student['final_score'])
    st.write("**Risk Level:**", student['risk_level'])

st.write("**Risk Level:**", student['risk_level'])
st.write("**Risk Score:**", student['risk_score'], "/ 4")
st.subheader("⚠️ Areas Needing Attention")

attention_found = False

if student['attendance'] < 75:
    st.warning("Attendance is below 75%.")
    attention_found = True

if student['study_hours'] < 2:
    st.warning("Study hours are below 2 hours.")
    attention_found = True

if student['assignment_completion'] < 70:
    st.warning("Assignment completion is below 70%.")
    attention_found = True

if student['quiz_average'] < 70:
    st.warning("Quiz performance is below 70%.")
    attention_found = True

if not attention_found:
    st.success("No major areas of concern detected.")

st.subheader("💡 Recommendations")

recommendation_found = False

if student['attendance'] < 75:
    st.info("Try to improve your attendance above 75%.")
    recommendation_found = True

if student['study_hours'] < 2:
    st.info("Increase your daily study time gradually.")
    recommendation_found = True

if student['assignment_completion'] < 70:
    st.info("Complete more assignments and submit them on time.")
    recommendation_found = True

if student['quiz_average'] < 70:
    st.info("Spend more time preparing for quizzes and revise weak topics.")
    recommendation_found = True

if not recommendation_found:
    st.success("Keep up the good work!")

# ============================================================
# ANALYTICS
# ============================================================

st.header("📊 Analytics")


# ------------------------------------------------------------
# 1. Final Score Distribution
# ------------------------------------------------------------

st.subheader("Final Score Distribution")

fig_score = px.histogram(
    df,
    x="final_score",
    nbins=20,
    title="Distribution of Final Scores",
    labels={
        "final_score": "Final Score",
        "count": "Number of Students"
    }
)

st.plotly_chart(fig_score, use_container_width=True)


# ------------------------------------------------------------
# 2. Study Hours vs Final Score
# ------------------------------------------------------------

st.subheader("Study Hours vs Final Score")

fig_study = px.scatter(
    df,
    x="study_hours",
    y="final_score",
    color="risk_level",
    hover_data=[
        "student_id",
        "attendance",
        "quiz_average",
        "assignment_completion"
    ],
    title="Relationship Between Study Hours and Final Score",
    labels={
        "study_hours": "Study Hours",
        "final_score": "Final Score"
    }
)

st.plotly_chart(fig_study, use_container_width=True)


# ------------------------------------------------------------
# 3. Risk Level vs Average Final Score
# ------------------------------------------------------------

st.subheader("Average Final Score by Risk Level")

risk_average = (
    df.groupby("risk_level", as_index=False)["final_score"]
    .mean()
)

fig_risk = px.bar(
    risk_average,
    x="risk_level",
    y="final_score",
    title="Average Final Score by Risk Level",
    labels={
        "risk_level": "Risk Level",
        "final_score": "Average Final Score"
    }
)

st.plotly_chart(fig_risk, use_container_width=True)


# ------------------------------------------------------------
# 4. Correlation Analysis
# ------------------------------------------------------------

st.subheader("Factors Related to Final Score")

correlations = (
    df.corr(numeric_only=True)["final_score"]
    .drop("final_score")
    .sort_values(ascending=False)
)

correlation_df = correlations.reset_index()

correlation_df.columns = [
    "Factor",
    "Correlation"
]

fig_corr = px.bar(
    correlation_df,
    x="Correlation",
    y="Factor",
    orientation="h",
    title="Correlation of Factors with Final Score"
)

st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================
# STUDENT FILTER
# ============================================================

st.header("🔎 Find Students")

col1, col2, col3 = st.columns(3)

with col1:
    selected_risk = st.selectbox(
        "Risk Level",
        ["ALL", "LOW", "MEDIUM", "HIGH"]
    )

with col2:
    min_score = st.slider(
        "Minimum Final Score",
        min_value=0,
        max_value=100,
        value=0
    )

with col3:
    max_score = st.slider(
        "Maximum Final Score",
        min_value=0,
        max_value=100,
        value=100
    )


# Apply filters
filtered_df = df.copy()

if selected_risk != "ALL":
    filtered_df = filtered_df[
        filtered_df["risk_level"] == selected_risk
    ]

filtered_df = filtered_df[
    (filtered_df["final_score"] >= min_score) &
    (filtered_df["final_score"] <= max_score)
]


st.write(
    f"**Students found: {len(filtered_df)}**"
)


# Display students
st.dataframe(
    filtered_df[
        [
            "student_id",
            "study_hours",
            "attendance",
            "assignment_completion",
            "quiz_average",
            "final_score",
            "risk_level"
        ]
    ],
    use_container_width=True
)

# ============================================================
# ADVANCED STUDENT FINDER
# ============================================================

st.header("🎯 Advanced Student Finder")

col1, col2 = st.columns(2)

with col1:
    min_attendance = st.slider(
        "Minimum Attendance (%)",
        0,
        100,
        0
    )

with col2:
    max_attendance = st.slider(
        "Maximum Attendance (%)",
        0,
        100,
        100
    )

col1, col2 = st.columns(2)

with col1:
    min_quiz = st.slider(
        "Minimum Quiz Average",
        0,
        100,
        0
    )

with col2:
    max_quiz = st.slider(
        "Maximum Quiz Average",
        0,
        100,
        100
    )

col1, col2 = st.columns(2)

with col1:
    min_study = st.slider(
        "Minimum Study Hours",
        0.0,
        10.0,
        0.0,
        step=0.5
    )

with col2:
    max_study = st.slider(
        "Maximum Study Hours",
        0.0,
        10.0,
        10.0,
        step=0.5
    )


# Apply advanced filters
advanced_df = df.copy()

advanced_df = advanced_df[
    (advanced_df["attendance"] >= min_attendance) &
    (advanced_df["attendance"] <= max_attendance) &
    (advanced_df["quiz_average"] >= min_quiz) &
    (advanced_df["quiz_average"] <= max_quiz) &
    (advanced_df["study_hours"] >= min_study) &
    (advanced_df["study_hours"] <= max_study)
]


st.write(f"### Students Found: {len(advanced_df)}")


# Display results
st.dataframe(
    advanced_df[
        [
            "student_id",
            "study_hours",
            "attendance",
            "quiz_average",
            "assignment_completion",
            "final_score",
            "risk_level"
        ]
    ],
    use_container_width=True
)


# Download filtered results
csv = advanced_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Students",
    data=csv,
    file_name="filtered_students.csv",
    mime="text/csv"
)