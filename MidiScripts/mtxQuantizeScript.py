import glob
import os
import sys

# This script will quantize mtx files to certain value
# for example quantization 30 tics will give us
# 30/120 = 1/4 of quarter note is sixteenth note
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "pliki_mtx_uproszczone\\*.mtx")
fileNames = glob.glob(path)
print("Kwantyzowanie " + str(len(fileNames)) + " plików tekstowych mtx")
fileCounter = 1

for fn in fileNames:
    progress = 100 * fileCounter / len(fileNames)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')

    f = open(fn, "r")
    lines = f.readlines()

    # 15 thirtytwo note
    # 20 sixteen note triolet
    # 30 sixteen note
    # 40 eight note triolet
    # 60 eigth note
    cut_file = []
    quantization = 30
    offset = 0
    lineTickNormalized = 0
    firstEvent: bool = True
    for i in range(len(lines)):
        if lines[i].startswith(("MTrk","MFile")):
            cut_file.append(lines[i])
        elif lines[i].startswith("TrkEnd"):
            tick = int(lines[i-1].split()[0])
            cut_file.append(str(tick+1)+" Par ch=1 c=64 v=0\n")
            cut_file.append(lines[i])
        elif len(lines[i].split()) >= 4:
            # calculate offset
            if firstEvent:
                firstEvent = False
                offset = int(lines[i].split()[0])
            # quantize tick value
            lineTick = int(lines[i].split()[0])-offset
            if lineTick%quantization < quantization/2.0:
                lineTick -= lineTick%quantization
            else:
                lineTick = lineTick + quantization - lineTick%quantization
             # quantize volume
            lineVol = lines[i].split()[4]
            # if int(lineVol[2:])>0:
            #     lineVol = "v=127"
            # save line
            cut_file.append(str(lineTick )+ ' ' + ' '.join(lines[i].split()[1:len(lines[i].split())-1]) + ' ' + lineVol + '\n')
    path = os.path.join(my_path, "pliki_mtx_skwantyzowane")
    name = os.path.join(path, os.path.basename(fn))
    try:
        to_save = open(name, "w")
    except FileNotFoundError:
        os.mkdir(path)
        to_save = open(name, "w")

    to_save.writelines(cut_file)
    fileCounter += 1


