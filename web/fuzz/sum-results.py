#coding=utf-8
#python reports.py "/root/hunt/test/" all.txt
import os,sys

result = []

def get_all(cwd):
    global text
    get_dir = os.listdir(cwd)
    for i in get_dir:
        sub_dir = os.path.join(cwd,i)
        if os.path.isdir(sub_dir):
            get_all(sub_dir)
        else:
            ax = os.path.basename(sub_dir)
            result.append(ax)
            f=open(sub_dir,"r")
            text=text+f.read()
if __name__ == "__main__":
    cur_path = os.getcwd()+'/'+sys.argv[1]
    text=""
    get_all(cur_path)
    rs=open(os.getcwd()+'/'+sys.argv[2],"w+")
    rs.write(text)
