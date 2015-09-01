#Command Line version for running in ec2

import sys

data = [-5.68557116,0.414662507,1.147672897,2.655077936,0.486554999,0.4229043,5.685179711,2.328275625,1.018801163]


def main(argv):
    
    series = float(argv[1])
    series = int(series)

    if series == 0:
	print "XEL-CMS"
    elif series == 1:
	print "PNC-STI"
    elif series == 2:
	print "BMY-CERN"

    mean = data[series*3]
    sd = data[series*3+1]
    beta = data[series*3+2]
    print (mean,sd,beta)
        
    n1 = float(argv[2])
    n2 = float(argv[3])
    
    p1 = 0
    p2 = 0
    
    try:
        p1 = float(argv[4])
        p2 = float(argv[5])
    except:
        pass
    
    resN = n2-beta*n1
    resP = p2 - beta*p1

    temp = "Current Res: " + str(resN)
    print temp
    
    temp = "Previous Res: "
    if resP == 0:
        temp += "None"
    else:
        temp += str(resP)
    print temp

    sd1 = mean + sd
    sd2 = mean + 3*sd
    sd3 = mean + -1*sd
    sd4 = mean + -3*sd
    sd5 = mean + 0.5*sd
    sd6 = mean + -0.5*sd

    temp = "0.5: " + str(sd6) + " - " + str(sd5)
    print temp
    temp = "1.0: " + str(sd3) + " - " + str(sd1)
    print temp
    temp = "3.0: " + str(sd4) + " - " + str(sd2)
    print temp
    print ' '
    
    temp = "Result: "
    
    if resN > sd2 or resN < sd4:
        temp += "10"
    elif resN > sd1 and resN < sd2:
        temp += "1"
    elif resN > sd4 and resN < sd3:
        temp += "-1"
    elif resN > sd6 and resN < sd5:
        temp += "0"
    else:
        temp += "NIL"
    print temp
        
if __name__ == "__main__":
    main(sys.argv)
    
    
    
    
