
f = open("..\\trainingLog03-05-21.txt","r")
out1 = open("trainingLog03-05-21MovesAverage10.txt","a")
out2 = open("trainingLog03-05-21ScoreAverage10.txt","a")
Lines = f.readlines()
temp1=0
temp2=0
counter=0
for line in Lines:
    temp=line.split("\t")
    if len(temp)>1:
        temp1+=int(temp[0])
        temp2+=int(temp[1])
        counter+=1
        if counter>=10:

            out1.write(str(temp1/10)+"\n")
            out2.write(str(temp2/10)+"\n")
            counter=0
if counter!=0:
    out1.write(str(temp1/counter))
    out2.write(str(temp2/counter))
f.close()
out1.close()
out2.close()