import pandas as pd

file = "data/students_synthetic_1000.csv"

df = pd.read_csv(file)

print("========== DATA QUALITY REPORT ==========")

# Number of records
print("\nTotal students:", len(df))

# Number of columns
print("Total columns:", len(df.columns))

# Missing values
missing_values = df.isnull().sum().sum()
print("Missing values:", missing_values)

# Duplicate rows
duplicate_rows = df.duplicated().sum()
print("Duplicate rows:", duplicate_rows)

# Duplicate student IDs
duplicate_ids = df["student_id"].duplicated().sum()
print("Duplicate student IDs:", duplicate_ids)

# Invalid attendance
invalid_attendance = (
    (df["attendance"] < 0) |
    (df["attendance"] > 100)
).sum()

print("Invalid attendance values:", invalid_attendance)

# Invalid quiz scores
invalid_quiz = (
    (df["quiz_average"] < 0) |
    (df["quiz_average"] > 100)
).sum()

print("Invalid quiz values:", invalid_quiz)

# Invalid assignment completion
invalid_assignment = (
    (df["assignment_completion"] < 0) |
    (df["assignment_completion"] > 100)
).sum()

print("Invalid assignment values:", invalid_assignment)

# Invalid final scores
invalid_final_score = (
    (df["final_score"] < 0) |
    (df["final_score"] > 100)
).sum()

print("Invalid final scores:", invalid_final_score)

# Data completeness
total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isnull().sum().sum()

completeness = (
    (total_cells - missing_cells) / total_cells
) * 100

print(f"\nData completeness: {completeness:.2f}%")

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== DATA QUALITY COMPLETE ==========")