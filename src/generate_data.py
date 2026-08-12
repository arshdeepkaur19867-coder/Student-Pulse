import numpy as np
import pandas as pd

np.random.seed(42)

number_of_students = 1000

student_ids = [
    f"S{i:04d}" for i in range(1, number_of_students + 1)
]

study_hours = np.round(
    np.random.normal(4.5, 1.8, number_of_students).clip(0.5, 10),
    1
)

attendance = np.round(
    np.random.normal(78, 12, number_of_students).clip(30, 100),
    0
)

assignment_completion = np.round(
    np.random.normal(75, 15, number_of_students).clip(20, 100),
    0
)

quiz_average = np.round(
    np.random.normal(72, 15, number_of_students).clip(20, 100),
    0
)

sleep_hours = np.round(
    np.random.normal(7, 1.2, number_of_students).clip(3, 11),
    2
)

phone_usage = np.round(
    np.random.normal(5.5, 2.5, number_of_students).clip(0.5, 12),
    2
)

dsa_problems = np.round(
    np.random.normal(35, 20, number_of_students).clip(0, 100),
    0
)

exam_days_remaining = np.random.randint(
    1, 61, number_of_students
)
final_score = (
    0.30 * quiz_average +
    0.25 * assignment_completion +
    0.20 * study_hours * 10 +
    0.15 * attendance +
    0.10 * dsa_problems
)

final_score += np.random.normal(0, 7)

final_score = np.clip(final_score, 0, 100)
final_score = np.round(final_score).astype(int)

df = pd.DataFrame({
    'student_id': student_ids,
    'study_hours': study_hours,
    'attendance': attendance,
    'assignment_completion': assignment_completion,
    'quiz_average': quiz_average,
    'sleep_hours': sleep_hours,
    'phone_usage': phone_usage,
    'dsa_problems': dsa_problems,
    'exam_days_remaining': exam_days_remaining,
    'final_score': final_score
})
df.to_csv(
    'data/students_synthetic_1000.csv',
    index=False
)

print("Dataset created successfully!")
print("Number of students:", len(df))
print(df.head())

print(df.describe())
print("\nCorrelation with final score:")
print(
    df.corr(numeric_only=True)['final_score']
    .sort_values(ascending=False)
)

print(df['final_score'].describe())