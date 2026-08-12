import pandas as pd

file = 'data/students_with_risk.csv'
df = pd.read_csv(file)

print(df['student_id'].head(10))
print(df['student_id'].dtype)

def show_student_profile(student_id):

    student = df[df['student_id'] == student_id]

    if student.empty:
        print(f"No data found for student ID: {student_id}")
        return

    student = student.iloc[0]

    risk_score = student['risk_score']
    risk_level = student['risk_level']

    print("\nProfile for Student ID:", student_id)
    print("Study Hours:", student['study_hours'])
    print("Attendance:", student['attendance'])
    print("Quiz Average:", student['quiz_average'])
    print("Assignment Completion:", student['assignment_completion'])
    print("Phone Usage:", student['phone_usage'])
    print("Sleep Hours:", student['sleep_hours'])
    print("DSA Problems:", student['dsa_problems'])
    print("Exam Days Remaining:", student['exam_days_remaining'])
    print("Final Score:", student['final_score'])
    print("Risk Score:", risk_score, "/ 4")
    print("Risk Level:", risk_level)

    print("\nAreas needing attention:")

    if student['attendance'] < 75:
        print("- Attendance")

    if student['study_hours'] < 2:
        print("- Study hours")

    if student['assignment_completion'] < 70:
        print("- Assignment completion")

    if student['quiz_average'] < 70:
        print("- Quiz performance")

    print("\nRecommendations:")

    if student['attendance'] < 75:
        print("- Try to improve your attendance above 75%.")

    if student['study_hours'] < 2:
        print("- Increase your daily study time gradually.")

    if student['assignment_completion'] < 70:
        print("- Complete more assignments and submit them on time.")

    if student['quiz_average'] < 70:
        print("- Spend more time preparing for quizzes and revise weak topics.")


show_student_profile("S0001")