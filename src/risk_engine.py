import pandas as pd
file='data/students_synthetic_1000.csv'
df = pd.read_csv(file)

df['risk_score']=0
df.loc[df['study_hours']<2, 'risk_score']+=1
df.loc[df['attendance']<75, 'risk_score']+=1
df.loc[df['assignment_completion']<70, 'risk_score']+=1
df.loc[df['quiz_average']<70, 'risk_score']+=1

def risk_category(score):
  if score<=1:
    return 'LOW'
  elif score==2:
    return 'MEDIUM'
  else:
    return 'HIGH'
df['risk_level']=df['risk_score'].apply(risk_category)
print(df[['student_id', 'risk_score', 'risk_level']])

risk_analysis = df.groupby('risk_level')['final_score'].agg(
    ['count', 'mean', 'min', 'max']
)

print("\nRisk level Analysis:")
print(risk_analysis)

high_risk_students = df[df['risk_level'] == 'HIGH']

print(high_risk_students[
    ['student_id',
     'study_hours',
     'attendance',
     'assignment_completion',
     'quiz_average',
     'phone_usage',
     'final_score']
])

risk_factor_analysis = df.groupby('risk_level')[
    ['study_hours',
     'attendance',
     'assignment_completion',
     'quiz_average',
     'final_score']
].mean()

print("\nAverage factors by risk level:")
print(risk_factor_analysis)

# Save the dataset with risk information
df.to_csv('data/students_with_risk.csv', index=False)

print("\nRisk data saved successfully!")