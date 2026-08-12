import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file='data/students_synthetic_1000.csv'
df=pd.read_csv(file)
print(df.columns)
no_of_students=df.shape[0]
avg_study_hr=df['study_hours'].mean()
avg_attendence=df['attendance'].mean()
average_quiz_score=df['quiz_average'].mean()
average_final_score=df['final_score'].mean()

highest_final_score=df['final_score'].max()
lowest_final_score=df['final_score'].min()
highest_study_hr=df['study_hours'].max()
lowest_attendance=df['attendance'].min()
low_attendance = df[df['attendance'] < 75]

print(f"Number of students: {no_of_students}")
print(f"Average study hours: {avg_study_hr:.2f}")
print(f"Average attendance: {avg_attendence:.2f}")
print(f"Average quiz score: {average_quiz_score:.2f}")
print(f"Average final score: {average_final_score:.2f}")
print(f"Highest final score: {highest_final_score}")
print(f"Lowest final score: {lowest_final_score}")
print(f"Highest study hours: {highest_study_hr}")
print(f"Lowest attendance: {lowest_attendance}")
print(f"Number of students with low attendance: {len(low_attendance)}")

high_study = df[df['study_hours'] > 5]
low_study = df[df['study_hours'] <= 5]

high_study_avg = high_study['final_score'].mean()
low_study_avg = low_study['final_score'].mean()

print("Average score of students studying >5 hours:", high_study_avg)
print(f"Average score of students studying <=5 hours: {low_study_avg:.2f}")

high_attendance=df[df['attendance']>=75]

high_attendance_avg=high_attendance['final_score'].mean()
low_attendance_avg=low_attendance['final_score'].mean()
print(f"Average score of students with attendance >=75%: {high_attendance_avg:.2f}")
print(f"Average score of students with attendance <75%: {low_attendance_avg:.2f}")


high_phone_usage=df[df['phone_usage']>5]
low_phone_usage=df[df['phone_usage']<=5]

high_phone_usage_avg=high_phone_usage['final_score'].mean()
low_phone_usage_avg=low_phone_usage['final_score'].mean()
print(f"Average score of students with high phone usage: {high_phone_usage_avg:.2f}")
print(f"Average score of students with low phone usage: {low_phone_usage_avg:.2f}")
print(f"Correlation between study hours and final score: {df['study_hours'].corr(df['final_score']):.2f}")
print("Starting correlation analysis...")

print(df.corr(numeric_only=True)['final_score'].sort_values(ascending=False))

plt.scatter(df['study_hours'], df['final_score'])
plt.title('Study Hours vs Final Score')
plt.xlabel('study_hours')
plt.ylabel('final_score')
plt.show()

plt.scatter(df['assignment_completion'], df['final_score'])
plt.xlabel('Assignment Completion')
plt.ylabel('Final Score')
plt.title('Assignment Completion vs Final Score')
plt.show()


correlation = df.corr(numeric_only=True)

sns.heatmap(correlation, annot=True)

plt.title('Student Pulse Correlation Heatmap')
plt.show()


study_hours_less_than_2=df[df['study_hours']<2]
attendance_less_than_75=df[df['attendance']<75]
assignment_completion_less_than_70=df[df['assignment_completion']<70]
quiz_average_less_than_70=df[df['quiz_average']<70]

print(f"Number of students with study hours < 2: {len(study_hours_less_than_2)}")
print(f"Number of students with attendance < 75: {len(attendance_less_than_75)}")
print(f"Number of students with assignment completion < 70: {len(assignment_completion_less_than_70)}")
print(f"Number of students with quiz average < 70: {len(quiz_average_less_than_70)}")


# df['risk_score']=0
# df.loc[df['study_hours']<2, 'risk_score']+=1
# df.loc[df['attendance']<75, 'risk_score']+=1
# df.loc[df['assignment_completion']<70, 'risk_score']+=1
# df.loc[df['quiz_average']<70, 'risk_score']+=1

# def risk_category(score):
#   if score<=1:
#     return 'LOW'
#   elif score==2:
#     return 'MEDIUM'
#   else:
#     return 'HIGH'
# df['risk_level']=df['risk_score'].apply(risk_category)
# print(df[['student_id', 'risk_score', 'risk_level']])

# risk_analysis = df.groupby('risk_level')['final_score'].agg(
#     ['count', 'mean', 'min', 'max']
# )

# print("\nRisk level Analysis:")
# print(risk_analysis)

# high_risk_students = df[df['risk_level'] == 'HIGH']

# print(high_risk_students[
#     ['student_id',
#      'study_hours',
#      'attendance',
#      'assignment_completion',
#      'quiz_average',
#      'phone_usage',
#      'final_score']
# ])

# risk_factor_analysis = df.groupby('risk_level')[
#     ['study_hours',
#      'attendance',
#      'assignment_completion',
#      'quiz_average',
#      'final_score']
# ].mean()

# print("\nAverage factors by risk level:")
# print(risk_factor_analysis)


# def show_student_profile(student_id):
#     student = df[df['student_id'] == student_id]
#     if student.empty:
#         print(f"No data found for student ID: {student_id}")
#         return
#     student = student.iloc[0]
#     risk_score = student['risk_score']
#     risk_level = student['risk_level']

#     print("Profile for Student ID:", student_id)
#     print("Study Hours:", student['study_hours'])
#     print("Attendance:", student['attendance'])
#     print("Quiz Average:", student['quiz_average'])
#     print("Assignment Completion:", student['assignment_completion'])
#     print("Phone Usage:", student['phone_usage'])
#     print("Sleep Hours:", student['sleep_hours'])
#     print("DSA Problems:", student['dsa_problems'])
#     print("Exam Days Remaining:", student['exam_days_remaining'])
#     print("Final Score:", student['final_score'])
#     print("Risk Score:", risk_score, "/ 4")
#     print("Risk Level:", risk_level)
#     print("\nAreas needing attention:")

   

#     if student['attendance'] < 75:
#       print("- Attendance")

#     if student['study_hours'] < 2:
#      print("- Study hours")

#     if student['assignment_completion'] < 70:
#      print("- Assignment completion")

#     if student['quiz_average'] < 70:
#       print("- Quiz performance")

#     print("\nRecommendations:")

#     if student['attendance'] < 75:
#      print("- Try to improve your attendance above 75%.")

#     if student['study_hours'] < 2:
#      print("- Increase your daily study time gradually.")

#     if student['assignment_completion'] < 70:
#       print("- Complete more assignments and submit them on time.")

#     if student['quiz_average'] < 70:
#       print("- Spend more time preparing for quizzes and revise weak topics.") 
# show_student_profile("S001")