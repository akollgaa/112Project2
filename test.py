# You can use this script to explore how your grade will
# change based on your midterm2, project2, and final exam scores.

# fill these in from your gradebook on Canvas:
hwAvg = 102   # hw avg in Canvas already includes two half-weighted
quizAvg = 96.5 # quiz avg in Canvas already drops + half-weights
midterm1Score = 100.8
project1Score = 93

# fill these in based on your best guesses:
midterm2Score = 50
project2Score = 70
finalExamScore = None  # None means "not taking"

# 1. find projectAvg:
lo, hi = min(project1Score, project2Score), max(project1Score, project2Score)
projectAvg = (hi + lo/2) / 1.5

#2. find examAvg:
if finalExamScore == None:
    lo, hi = min(midterm1Score, midterm2Score), max(midterm1Score, midterm2Score)
else:
    # final exam taken, so counts along with higher midterm:
    midtermScore = max(midterm1Score, midterm2Score)
    lo, hi = min(midtermScore, finalExamScore), max(midtermScore, finalExamScore)
examAvg = (hi + lo/2) / 1.5

#3. compute semesterAvg and semesterGrade
semesterAvg = (hwAvg*.20 + projectAvg*.20 + quizAvg*.15 + examAvg*.45)
if semesterAvg >=   89.5: semesterGrade = 'A'
elif semesterAvg >= 79.5: semesterGrade = 'B'
elif semesterAvg >= 69.5: semesterGrade = 'C'
elif semesterAvg >= 59.5: semesterGrade = 'D'
else:                     semesterGrade = 'R'

#4. print report
components = (('Homework', hwAvg,       0.20),
              ('Projects', projectAvg,  0.20),
              ('Quizzes',  quizAvg,     0.15),
              ('Exams',    examAvg,     0.45))
print('Component  Score    Weight  Contribution')
for label, avg, weight in components:
    print(f'{label:10} {avg:5.1f} {100*weight:-8}% {avg*weight:7.1f}')
print(f'Projected semester numeric grade: {semesterAvg:0.1f}')
print(f'Projected semester letter grade:  {semesterGrade}')