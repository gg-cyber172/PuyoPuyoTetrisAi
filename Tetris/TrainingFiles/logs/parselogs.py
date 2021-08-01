fMovesAverage = open("trainingLogMovesDoneAverage05-05-21.txt","a")
fScoresAverage = open("trainingLogScoresAverage05-05-21.txt","a")
fMoves = open("trainingLogMovesDone05-05-21.txt","r")
fScores = open("trainingLogScores05-05-21.txt","r")

LinesMoves = fMoves.readlines()
fMoves.close()
LinesScore = fScores.readlines()
fScores.close()
counter=0
temp=0
for line in LinesMoves:
    temp+=float(line.strip())
    counter+=1
    if counter==10:
        fMovesAverage.write(str(temp/10)+"\n")
        counter=0
        temp=0

if counter!=0:
    fMovesAverage.write(str(temp/counter)+"\n")
fMovesAverage.close()
temp=0
counter=0
for line in LinesScore:
    temp+=float(line.strip())
    counter+=1
    if counter>9:
        fScoresAverage.write(str(temp/10)+"\n")
        counter=0
        temp=0

if counter != 0:
    fMovesAverage.write(str(temp / counter) + "\n")
fScoresAverage.close()