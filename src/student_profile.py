import pandas as pd

file = 'data/students_with_risk.csv'
df = pd.read_csv(file)



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
    print("Risk Score:", risk_score, "/ 8")
    print("Risk Level:", risk_level)

    print("\nAreas needing attention:")
    has_issues=False

    if student["quiz_average"] < 70:
      print("- Quiz performance")
      has_issues = True

    if student["assignment_completion"] < 70:
     print("- Assignment completion")
     has_issues = True

    if student["study_hours"] < 2:
     print("- Study hours")
     has_issues = True

    if student["attendance"] < 75:
      print("- Attendance")
      has_issues = True
    if not has_issues:
        print("- No major areas of concern, keep up the good work!")
    print("\nRecommendations:")
    if not has_issues:
        print("- Maintain your current study habits and continue to perform well.")
    if student["quiz_average"] < 70:
       print("- Spend more time preparing for quizzes and revise weak topics.")

    if student["assignment_completion"] < 70:
       print("- Complete more assignments and submit them on time.")

    if student["study_hours"] < 2:
      print("- Increase your daily study time gradually.")

    if student["attendance"] < 75:
      print("- Try to improve your attendance above 75%.")
show_student_profile("S0001")