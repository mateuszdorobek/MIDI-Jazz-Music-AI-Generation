import glob
import os
import re
import sys
import numpy as np
import png

# This script will decompress images 128x128 into mtx files, that will be lately transformed into midi files
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "..\\files\\images\\*.png")
fileNames = glob.glob(path)
print("Images To Mtx Decompressing: " + str(len(fileNames)) + " files")

fileCounter = 0

quantization = 30
length = 128
width = 128

for fn in fileNames:
    mtxFile = []
    mtxFile.append("MFile 1 1 120\n")
    mtxFile.append("MTrk\n")
    # print(os.path.basename(fn))
    fileCounter += 1
    progress = 100 * fileCounter / len(fileNames)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')

    w, h, pixels, meta = png.Reader(filename=fn).asRGB()

    array = np.asarray(list(pixels))

    activeNotes = array[:, 0]*0

    for i in range(len(array[0,:])):
        newActiveNotes = array[:,i] #kolejny wiersz z nutami wdanym ticku
        for j in range(len(newActiveNotes)):
            if newActiveNotes[j]>0 and activeNotes[j]==0:
                # note just pressed
                mtxFile.append(str(i*quantization) + " On ch=1 n=" + str(length-j-1) + " v=127\n")
                activeNotes[j] = newActiveNotes[j]
            elif newActiveNotes[j]==0 and activeNotes[j]>0:
                mtxFile.append(str(i * quantization) + " On ch=1 n=" + str(length-j-1) + " v=0\n")
                activeNotes[j] = newActiveNotes[j]
    mtxFile.append("TrkEnd\n")
    path = os.path.join(my_path, "..\\files\\mtxOutput\\mtx")
    imageNumber = re.search('img(.*).png', os.path.basename(fn)).group(1)
    name = os.path.join(path+str(imageNumber)+".mtx")
    try:
        to_save = open(name, "w")
    except FileNotFoundError:
        os.mkdir(    os.path.join(my_path, "..\\files\\mtxOutput\\"))
        to_save = open(name, "w")
    to_save.writelines(mtxFile)