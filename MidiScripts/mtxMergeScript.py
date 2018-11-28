import glob
import os
import sys

# This script will merge all Quantized files into one, that will be lately cutted into batches

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "..\\files\\mtxQuantized\\*.mtx")
fileNames = glob.glob(path)
print("Mtx Files Merging: " + str(len(fileNames)) + " files")
fileCounter = 1
cut_file = ["MFile 1 1 120\n","MTrk\n"]
gap = 300 # 0.3s gap beetwin merged files
lastTick = 0
tick = 0
for fn in fileNames:
    progress = 100 * fileCounter / len(fileNames)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')

    f = open(fn, "r")
    lines = f.readlines()

    for i in range(len(lines)):
        activeNotes = [0] * 128
        if lines[i].startswith(("MTrk","MFile","TrkEnd")):
            continue
        elif len(lines[i].split()) >= 4:
            tick = int(lines[i].split()[0])
            tick += lastTick
            cut_file.append(str(tick) + ' ' + ' '.join(lines[i].split()[1:len(lines[i].split())]) + '\n')
        else:
            print("Error\n Unexpected data: \n\t" + lines[i])
    lastTick = tick + gap
    fileCounter += 1

cut_file.append("TrkEnd\n")

name = os.path.join(my_path, "..\\files\\mtxMerged\\data.mtx")
try:
    to_save = open(name, "w")
except FileNotFoundError:
    os.mkdir(os.path.join(my_path, "..\\files\\mtxMerged"))
    to_save = open(name, "w")
to_save.writelines(cut_file)



