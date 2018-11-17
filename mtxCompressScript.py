import sys
import numpy as np
import png

# This script will compress big data file with merged midi files into pictures and split it into 128x128 batches

fileName = "files/mtxMerged/data.mtx"
print("Mtx Files Compressing: ")
lineCounter = 1

file = open(fileName, "r")
lines = file.readlines()

cut_file = []
savedFiles = 0

quantization = 30
length = 128
width = 128

isSustained = 0
activeNotes = [0] * width
holdNotes = [0] *width

img = np.zeros((length,width,3), np.uint8)

for i in range(len(lines)):

    progress = 100 * lineCounter / len(lines)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')
    activeNotes = [0] * 128
    if lines[i].startswith(("MTrk","MFile","TrkEnd")):
        lineCounter += 1
        continue

    elif len(lines[i].split()) >= 4:
        tick = int(int(lines[i].split()[0])/quantization)               # 0,1,2,3 etc.
        type = 0 if lines[i].split()[1].startswith("Par") else  1       # Par 0,    On 1
        value = int((lines[i].split()[3])[2:])                          # c=64 64,  n=25 25   ...
        volume = 0 if int(lines[i].split()[4][2:])==0 else 1            # v=0 0,    v=127 1

        # adding note to active notes - played at this moment
        if type == 1: # On
            activeNotes[value] = volume
        if type == 0: # Par
            isSustained = volume
        # if sustain pedal is pressed, I add activeNotes to holdNotes
        if isSustained:
            for j in range(len(activeNotes)):
                if activeNotes[j]:
                    holdNotes[j]=1
        else:
            holdNotes = [0] * 128
        # setting values of midi notes to pixels. Coded on BGR values of pixels.
        # So first line will be on Blue value of first pixel, second on Green value of first and so on.
        if tick >= (savedFiles+1)*length*3:
            # save image
            pngFile = open("files/images/img"+str(savedFiles)+".png", "wb")
            pngWriter = png.Writer(128,128)
            pngWriter.write(pngFile,np.reshape(img, (-1, 128 * 3)))
            pngFile.close()
            img = np.zeros((length, width, 3), np.uint8)
            savedFiles += 1
        for j in range(width):
            if isSustained:
                img.itemset(int(tick%(length*3)/3), j, tick%3, holdNotes[j]*255)
            else:
                img.itemset(int(tick%(length*3)/3), j, tick%3, activeNotes[j]*255)
        lineCounter += 1
# saving last file, that might be uncompleted
pngFile = open("files/images/img"+str(savedFiles)+".png", "wb")
pngWriter = png.Writer(128,128)
pngWriter.write(pngFile,np.reshape(img, (-1, 128 * 3)))
pngFile.close()