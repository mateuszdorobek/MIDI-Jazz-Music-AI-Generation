import glob
import os
import sys
import numpy as np
import png

# This script will decompress images 128x128 into mtx files, that will be lately transformed into midi files
path = "files/images/*.png"
path = "files/images/img0.png"
fileNames = glob.glob(path)
print("Images To Mtx Decompressing: " + str(len(fileNames)) + " files")

fileCounter = 0
mtxFile = []

quantization = 30
length = 128
width = 128

for fn in fileNames:
    mtxFile.append("MFile 1 1 120\n")
    mtxFile.append("MTrk\n")
    # print(os.path.basename(fn))
    fileCounter += 1
    progress = 100 * fileCounter / len(fileNames)
    # sys.stdout.write("\r" + str(round(progress, 1)) + '%')

    w, h, pixels, meta = png.Reader(filename=fn).asRGB()

    array = np.asarray(list(pixels))

    activeNotes = array[:, 0]*0

    for i in range(len(array[0,:])):
        newActiveNotes = array[:,i] #kolejny wiersz z nutami wdanym ticku
        for j in range(len(newActiveNotes)):
            if newActiveNotes[j]>0 and activeNotes[j]==0:
                # note just pressed
                print("j = "+str(j)+" i = "+str(i))
                print(str(i*quantization) + " On ch=1 n=" + str(j) + " v=127\n")
                mtxFile.append(str(i*quantization) + " On ch=1 n=" + str(length-j-1) + " v=127\n")
                activeNotes[j] = newActiveNotes[j]
            elif newActiveNotes[j]==0 and activeNotes[j]>0:
                print("j = "+str(j)+" i = "+str(i))
                print(str(i * quantization) + " On ch=1 n=" + str(j) + " v=0\n")
                mtxFile.append(str(i * quantization) + " On ch=1 n=" + str(length-j-1) + " v=0\n")
                activeNotes[j] = newActiveNotes[j]
    mtxFile.append("TrkEnd\n")

    name = os.path.join("files/mtxOutput/mtx"+str(fileCounter-1)+".mtx")
    try:
        to_save = open(name, "w")
    except FileNotFoundError:
        os.mkdir("files/mtxOutput")
        to_save = open(name, "w")
    to_save.writelines(mtxFile)