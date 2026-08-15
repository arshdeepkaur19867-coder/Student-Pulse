import pandas as pd

file = "data/students_synthetic_1000.csv"

df = pd.read_csv(file)


# ============================================================
# WEIGHTED RISK SCORE
# ============================================================

df["risk_score"] = 0


# Quiz performance
df.loc[
    df["quiz_average"] < 70,
    "risk_score"
] += 3


# Assignment completion
df.loc[
    df["assignment_completion"] < 70,
    "risk_score"
] += 2


# Study hours
df.loc[
    df["study_hours"] < 2,
    "risk_score"
] += 2


# Attendance
df.loc[
    df["attendance"] < 75,
    "risk_score"
] += 1
def risk_category(score):

    if score <= 2:
        return "LOW"

    elif score <= 4:
        return "MEDIUM"

    else:
        return "HIGH"


df["risk_level"] = df["risk_score"].apply(
    risk_category
)

def get_risk_factors(student):
    factors = []

    if student["quiz_average"] < 70:
        factors.append("Low quiz performance")

    if student["assignment_completion"] < 70:
        factors.append("Low assignment completion")

    if student["study_hours"] < 2:
        factors.append("Low study hours")

    if student["attendance"] < 75:
        factors.append("Low attendance")

    return ", ".join(factors) if factors else "No major risk factors"


df["risk_factors"] = df.apply(get_risk_factors, axis=1)

df.to_csv(
    "data/students_with_risk.csv",
    index=False
)

print("Risk analysis completed!")

print(
    df[
        [
            "student_id",
            "risk_score",
            "risk_level",
            "risk_factors"
        ]
    ].head(20)
)