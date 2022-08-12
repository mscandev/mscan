import sys,os
#python3 csv-reduplication.py  a.csv test

inputfile=open(os.getcwd()+"/"+sys.argv[1],"r")
exist_size = []
outputfile=sys.argv[2]

for line in inputfile:
    try:
        http_one = line.strip().split(',')
        http_url = http_one[1]
        http_size = http_one[5]

        if http_size in exist_size or 'http' not in http_url:
            continue
        else:
            exist_size.append(http_size)
            with open(outputfile, 'a+') as f:
                f.write(http_url+'\n')
            with open(outputfile+'.csv', 'a+') as f:
                f.write(line)
    except:
        pass
